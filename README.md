Web app template
================
A useful starter kit for web applications using
[WebCore](https://github.com/marrow/WebCore),
[Paste](http://pythonpaste.org/),
[Flup](http://trac.saddi.com/flup) and
[Nginx](http://wiki.nginx.org/Main)


tl;dr
-----

    cd ~/src
    curl -sL http://aghz.ca/webcore.py | python - MyProject | sh


Setting up a new project
------------------------

A [script](https://github.com/aGHz/webcore_template/blob/master/setup.py) is provided
to automate the installation and customization of the template, also mirrored at the more convenient URL
[http://aghz.ca/webcore.py](http://aghz.ca/webcore.py). Piping it through Python will
output a series of documented, customized instructions which can be run manually or, after proper inspection,
piped further through `sh`. To find help on the command line usage:

    curl -sL http://aghz.ca/webcore.py | python -

- - -

    Generate setup instructions for the WebCore starter kit
    After review, the output can be run manually or piped through sh

    Syntax:
        python setup.py <options>
        python setup.py [options] <name>

    Options:
        -n/--name        The name of the project. Can be specified without -n, after option list
        -p/--path        Absolute path for the project. Defaults to `pwd`/<name>
        -u/--url         Git repository url for remote origin. Skip remote-related commands if omitted
        --submodules     Submodule root, e.g. git@github.com/marrow, https://github.com/fork
                         Must expose the repositories: WebCore, marrow.templating, marrow.util
        --no-flow        Skip git-flow commands. Not recommended, install git-flow instead!

    Examples:
        python setup.py MyProject
        python setup.py -n MyProject -p /home/me/src/my_project
        python setup.py -u git@github.com:me/my_project --submodules=git@github.com:me MyProject


Use the `--submodules` option to change the location where the template's submodules are cloned from.
This is useful if you wish to use a fork, or enable write access to the submodules. By default, the
template uses the
[WebCore](https://github.com/marrow/WebCore),
[marrow.templating](https://github.com/marrow/marrow.templating) and
[marrow.util](https://github.com/marrow/marrow.util) public, read-only GitHub repositories
provided by [marrow](https://github.com/marrow/). If you use this option, the given URL must contain
all these repositories with the exact same name.


Activating a project
--------------------

The setup will only clone the template, customize the files and reset the git repository.
The code is complete, but not ready to run. The script 
[deploy.py](https://github.com/aGHz/webcore_template/blob/master/deploy.py)
will generate instructions to prepare the virtualenv, git-flow (if not already done by the setup script)
hook up the Nginx config and make the app start on boot. Again, these instructions can be run
manually, or reviewed and then piped through `sh`.

If you just finished the setup instructions above, chances are good all you need is:

    python develop.py --venv


Deploying a project
-------------------

The template is prepared with a `.gitignore` file that will keep all the local-specific files out
of the repository. This means every time the project is cloned in a new location, it must be deployed,
i.e. activated again. Generally there are two situations:

__Development server__: This will use git-flow to check out the develop branch and setup the virtualenv.
The app is served directly via paste using `./etc/local.ini`.

    python develop.py --flow --venv
    
__Production server__: This will stay on the master branch, setup the virtualenv, make the app start
on boot and run under the current user and group, and finally hook the app up into the Nginx config.

    python deploy.py --venv --auto=`id -nu`:`id -ng` --nginx
    

Directory structure
-------------------

You may have already noticed the non-standard directory structure. This template is prepared to encapsulate
absolutely everything about the app in its root dirctory. Where files are provided for external systems,
they remain in the app directory and are only sym-linked to from the proper locations. Similarly with log files,
UNIX sockets and pid files.

These are the prescribed directories:

    bin/             - Executable scripts, also where virtualenv puts its stuff
    etc/             - Configuration files, including the Paste Deploy ini files
    src/             - Source code for the app package
    usr/src/         - Third-party source code, preferably in the form of git submodules
    usr/share/       - Static files served by your app. Configured into nginx.conf
    usr/templates/   - Template files, if you prefer to keep them outside your app package
    var/log/         - Log files for nginx, paste and management commands (see bin/manage.sh)
    var/run/         - Socket and pid files
    
