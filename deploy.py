#!/bin/python

import getopt
import os
import subprocess
import sys

def syntax():
    print """Generate instructions to deploy this new installation of __project__
After review, the output can be run manually or piped through sh

Syntax:
    python deploy.py [restart] [options]

Options:
    --flow      Initializes git-flow and pulls branch develop if remote is set
    --venv      Sets up a new virtualenv, installs packages
    --nginx=    The path to Nginx sites-enabled, will symlink app's nginx.conf
                Leave blank for a sensible default, i.e. '--nginx='
    --auto=     user[:group] under which the Paste process should run at boot
                If absent, app will not be set up for starting on boot
                If group is absent, it is assumed to match the user
                Will also start the app right after deployment
                Probably pointless without --nginx

    restart     Reconfigures the app and restarts it
    --nginx     When used after restart, will also restart Nginx
                Only needed when the Nginx configuration changed

Examples:
    Typical activation of a fresh WebCore template setup
    python deploy.py --venv

    Typical for development, running builtin server without Nginx our autostart
    python deploy.py --flow --venv

    Typical for production environments
    python deploy.py --venv --auto=`id -nu`:`id -ng` --nginx

    After making changes to the Python code
    python deploy.py restart

"""

COMMENT = "# " + '-' * 72
ECHO_COMMENT = '-' * 80


def restart(nginx, linux):
    out = []

    if linux:
        if nginx:
            out += [
                "echo 'sudo /etc/init.d/__project__ restart'",
                "sudo /etc/init.d/__project__ restart",
                ]

    return out


def flow():
    try:
        branches = subprocess.check_output(['git', 'branch'], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return [
            "",
            COMMENT,
            "# WARNING: This is not a git repository",
            COMMENT,
            "",
            ]
    if 'develop' in branches:
        return [
            "",
            COMMENT,
            "# WARNING: --flow requested but git-flow already installed",
            COMMENT,
            "",
            ]

    out = [
        "",
        COMMENT,
        "# Initialize git-flow",
        COMMENT,
        "git flow init",
        "git checkout develop", # Possibly redundant
        "",
        ]

    try:
        remotes = subprocess.check_output(['git', 'remote'], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        remotes = ''
    if 'origin' in remotes:
        out += [
            "# Set the proper upstream for branch develop",
            "git branch --set-upstream develop origin/develop",
            "git pull",
            "git submodule update --init --recursive", # Possibly redundant
            "",
            ]

    return out


def venv():
    out = [
        "",
        COMMENT,
        "# Initialize virtualenv",
        COMMENT,
        "virtualenv --no-site-packages .",
        ". bin/activate",
        "",
        "# Install dependencies",
        "pip install -r etc/packages.pip",
        "python src/setup.py develop",
        "cd src && python setup.py develop && cd ..",
        "",
        ]
    return out


def nginx(path, linux):
    out = []
    if not path:
        if linux:
            path = '/etc/nginx/sites-enabled'
        else:
            path = '/usr/local/etc/nginx/sites-enabled'
    if not os.path.isdir(path):
        out = [
            "",
            COMMENT,
            "# ERROR: Nginx config not found: {0}".format(path),
            COMMENT,
            "",
            ]
    out += [
        "",
        COMMENT,
        "# Sym-link to the Nginx config from the proper location",
        COMMENT,
        "{0}ln -s /path/to/etc/nginx.conf {1}".format('sudo ' if linux else '', os.path.join(path, '__project__')),
        "",
        ]

    out += ["# Reload the Nginx config"]
    if linux:
        out += ["sudo /etc/init.d/nginx reload"]
    else:
        out += ["nginx -s reload"]
    out += [""]

    return out


def auto(user_group, linux):
    [user, group] = (user_group + ':' + user_group).split(':')[:2] # trick to make group=user if absent
    sed_inplace_separator = '' if linux else ' '

    out = [
        "",
        COMMENT,
        "# Configure initd.sh with user {user}:{group}".format(user=user, group=group),
        COMMENT,
        "sed -i{i_sep}'' 's|__user__|{user}|' bin/initd.sh".format(user=user, i_sep=sed_inplace_separator),
        "sed -i{i_sep}'' 's|__group__|{group}|' bin/initd.sh".format(group=group, i_sep=sed_inplace_separator),
        "",
        ]

    if linux:
        out += [
            "# Sym-link to the init.d script from the proper location",
            "sudo ln -s /path/to/bin/initd.sh /etc/init.d/__project__",
            "sudo update-rc.d __project__ defaults",
            "",
            "echo",
            "echo " + ECHO_COMMENT,
            "echo '    To no longer start on boot, run:'",
            "echo '        sudo /etc/init.d/__project__ stop'",
            "echo '        sudo update-rc.d -f __project__ remove'",
            "echo " + ECHO_COMMENT,
            "echo",
            "",
            ]
    else:
        out += [
            "# Sym-link to the LaunchAgent plist from the proper location",
            "ln -s /path/to/bin/launchAgent.plist ~/Library/LaunchAgents/com.__project__.__logged_user__.production.plist",
            "launchctl load ~/Library/LaunchAgents/com.__project__.__logged_user__.production.plist",
            "echo",
            "echo " + ECHO_COMMENT,
            "echo '    To no longer start on boot, run:'",
            "echo '        launchctl stop com.__project__.__logged_user__.production'",
            "echo '        launchctl remove com.__project__.__logged_user__.production'",
            "echo '        rm ~/Library/LaunchAgents/com.__project__.__logged_user__.production.plist'",
            "echo " + ECHO_COMMENT,
            "echo",
            "",
            ]

    return out


def start(opt, linux):
    out = []

    if '--auto' in opt and '--nginx' not in opt:
        out += [
            "",
            COMMENT,
            "# WARNING: --auto set without --nginx",
            "# The production server will start but FastCGI will not be served by Nginx",
            "# This is potentially okay if it was specifically intended",
            COMMENT,
            "",
            ]

    if '--auto' in opt:
        out += [
            "",
            COMMENT,
            "# Start the production server",
            COMMENT,
            "echo",
            "echo " + ECHO_COMMENT,
            "echo '    Starting production server'",
            ]
        if linux:
            out += [
                "echo '        sudo /etc/init.d/__project__ start'",
                "sudo /etc/init.d/__project__ start",
                ]
        else:
            out += [
                "echo '        launchctl start com.__project__.__logged_user__.production'",
                "launchctl start com.__project__.__logged_user__.production",
                ]
        out += [
            "echo " + ECHO_COMMENT,
            "",
            ]

    out += [
        "",
        COMMENT,
        "# Server instructions",
        COMMENT,
        "echo",
        "echo " + ECHO_COMMENT,
        "echo '    To run the local development server:'",
        "echo '    ./etc/local.ini'",
        ]
    if '--auto' in opt:
        out += [
            "echo " + ECHO_COMMENT,
            "echo '    To control the local production server:'",
            ]
        if linux:
            out += ["echo '    sudo /etc/init.d/__project__ start|stop|restart'"]
        else:
            out += ["echo '    launchctl start|stop com.__project__.__logged_user__.production'"]
    out += [
        "echo " + ECHO_COMMENT,
        "echo",
        "",
        ]

    return out


def main(argv):
    linux = sys.platform.startswith('linux')

    if '--nginx' in argv:
        # Silly getopt fix for potentially empty option
        argv[argv.index('--nginx')] = '--nginx='

    opt = getopt.getopt(argv, 'h', [
        'venv',
        'flow',
        'auto=',
        'nginx=',
        'help',
        ])
    argv = opt[1]
    opt = dict(opt[0])

    if '-h' in opt or '--help' in opt or (len(opt) == 0 and len(argv) == 0):
        syntax()
        return 1

    if 'restart' in argv:
        restart('--nginx' in argv, linux)
        return 1

    out = [
        "",
        "cd /path/to",
        ]

    if '--flow' in opt:
        out += flow()

    if '--venv' in opt:
        out += venv()

    if '--nginx' in opt:
        out += nginx(opt['--nginx'], linux)

    if '--auto' in opt:
        out += auto(opt['--auto'], linux)

    out += start(opt, linux)

    out += [
        "",
        COMMENT,
        "# ",
        "#    If the script is correct, run the following to deploy:",
        "# ",
        "#    python {0}".format(' '.join(sys.argv) + ' | sh'),
        "# ",
        COMMENT,
        "",
        ]

    print "\n".join(out)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
