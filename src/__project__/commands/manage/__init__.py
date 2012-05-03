import os
import paste.fixture
import paste.registry
import paste.deploy.config
from paste.deploy import loadapp, appconfig
from paste.script.command import Command, BadCommand
import sys
from web.core import config

from __project__.commands.manage import example


COMMANDS = ['show_config', 'show_commands', # system commands
            'example', # application commands
            ]

class ManageCommand(Command):
    """Run __project__ management commands"""
    summary = __doc__.splitlines()[0]
    group_name = '__project__'

    parser = Command.standard_parser(verbose=True)
    parser.add_option('-c', '--config', action='store', dest='config_file', type='string',
                      default='./etc/manage.ini', help='Paste deploy config file')
    def command(self):
        command = self.args.pop(0) if self.args else 'show_commands'
        if command in COMMANDS and hasattr(self, command)\
                               and hasattr(getattr(self, command), '__call__'):
            self._load_app()
            try:
                getattr(self, command)(*self.args)
            finally:
                self._close_app()

    def show_config(self, *args):
        """Print the WebCore configuration"""
        for k in config:
            print '{k}: {v}'.format(k=k, v=config[k])

    def show_commands(self, *args):
        """Print a list of available management commands"""
        print self.__doc__
        print ''
        print 'Available commands:'
        for c in COMMANDS:
            print '    %s - %s' % (c, getattr(self, c).__doc__)
        print ''

    def example(self, *args):
        """This is an example command. Options:
                     example-option        This options makes the example more examplier
                     examples=id,id,...    Makes only certain examples examplier
        """
        example_option = False
        examples = None
        for arg in args:
            if arg.startswith('example-option') or arg.startswith('example_option'):
                example_option = True
            elif arg.startswith('examples='):
                examples = arg[len('examples='):].split(',')
        example.perform_example(example_option, examples)


    def _load_app(self):
        config_file = self.options.config_file
        if not os.path.isfile(config_file):
            raise BadCommand('Error: CONFIG_FILE not found at: %s\nPlease specify a CONFIG_FILE' % config_file)

        config_name = 'config:%s' % config_file
        here_dir = os.getcwd()

        if self.options.verbose:
            # Configure logging from the config file
            self.logging_file_config(config_file)

        self.config = appconfig(config_name, relative_to=here_dir)
        self.config.update({'app_conf': self.config.local_conf,
                            'global_conf': self.config.global_conf})
        paste.deploy.config.CONFIG.push_thread_config(self.config)

        # Load locals and populate with objects for use in shell
        sys.path.insert(0, here_dir)

        # Load the wsgi app first so that everything is initialized right
        wsgiapp = loadapp(config_name, relative_to=here_dir)
        self.app = paste.fixture.TestApp(wsgiapp)

        # Query the test app to setup the environment
        tresponse = self.app.get('/_test_vars')
        request_id = int(tresponse.body)

        # Disable restoration during app requests
        self.app.pre_request_hook = lambda self: paste.registry.restorer.restoration_end()
        self.app.post_request_hook = lambda self: paste.registry.restorer.restoration_begin(request_id)

        paste.registry.restorer.restoration_begin(request_id)

    def _close_app(self):
        paste.registry.restorer.restoration_end()

