import os
import paste.fixture
import paste.registry
from paste.deploy import loadapp, appconfig
import paste.deploy.config
from paste.script.command import Command, BadCommand
import sys


class AdminCommand(Command):
    """Run the __project__ admin shell"""
    summary = __doc__.splitlines()[0]
    group_name = '__project__'

    parser = Command.standard_parser(verbose=True)
    parser.add_option('-c', '--config', action='store', dest='config_file', type='string',
                      default='./etc/development.ini', help='Paste deploy config file')
    parser.add_option('-f', '--file', action='store', dest='script_file', type='string',
                      help='Python file to run')
    parser.add_option('--no-ipython', action='store_true', dest='disable_ipython',
                      help='Do not use the IPython shell')
    def command(self):
        self._load_app()
        try:
            self.run_shell(*self.args)
        finally:
            self._close_app()

    def run_shell(self, *args):
        locs = dict(__name__="__project__-admin", wsgiapp=self.wsgiapp, app=self.app)

        admin_boot = os.path.join(os.path.dirname(__file__), 'admin_boot.py')
        execfile(admin_boot, {}, locs)

        if self.options.script_file:
            execfile(self.options.script_file, {}, locs)
            return

        try:
            # try to use IPython if possible
            if self.options.disable_ipython:
                raise ImportError()
            from IPython.frontend.terminal.embed import InteractiveShellEmbed
            if self.options.verbose:
                shell = InteractiveShellEmbed()
                print ''
            else:
                shell = InteractiveShellEmbed(banner1='')
            shell(local_ns=locs, global_ns={})

        except ImportError:
            import code
            shell = code.InteractiveConsole(locals=locs)
            if self.options.verbose:
                banner = 'Python %s\n\n' % sys.version
            else:
                banner = ''

            try:
                import readline
            except ImportError:
                pass

            print ''
            shell.interact(banner)

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
        self.wsgiapp = loadapp(config_name, relative_to=here_dir)
        self.app = paste.fixture.TestApp(self.wsgiapp)

        # Query the test app to setup the environment
        tresponse = self.app.get('/_test_vars')
        request_id = int(tresponse.body)

        # Disable restoration during app requests
        self.app.pre_request_hook = lambda self: paste.registry.restorer.restoration_end()
        self.app.post_request_hook = lambda self: paste.registry.restorer.restoration_begin(request_id)

        paste.registry.restorer.restoration_begin(request_id)

    def _close_app(self):
        paste.registry.restorer.restoration_end()


