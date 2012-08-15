#!/bin/python

import getopt
import os
import subprocess
import sys

def syntax():
    print """Deploy this new installation of __project__

Syntax:
    python deploy.py [restart] [options]

Options:
    --flow      Initializes git-flow and pulls branch develop if remote is set
    --venv      Sets up a new virtualenv, installs packages
    --nginx=    The path to Nginx sites-enabled, will symlink app's nginx.conf
                Leave blank for a sensible default, i.e. '--nginx='
    --auto      Start the production app on system boot
                Will also start the app right after deployment
                Probably pointless without --nginx

    restart     Reconfigures the app and restarts it
    --nginx     When used after restart, will also restart Nginx
                Only needed when the Nginx configuration changed

Examples:
    Typical activation of a fresh WebCore template install
    python deploy.py --venv

    Typical for development, running builtin server without Nginx our autostart
    python deploy.py --flow --venv

    Typical for production environments
    python deploy.py --flow --venv --auto --nginx=/etc/nginx/sites-enabled

    python deploy.py restart --nginx

"""


def restart(nginx):
    pass


def flow():
    try:
        branches = subprocess.check_output(['git', 'branch'], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return [
            "", "# " + '-' * 72,
            "# WARNING: This is not a git repository",
            "# " + '-' * 72,
            "",
            ]
    if 'develop' in branches:
        return [
            "", "# " + '-' * 72,
            "# WARNING: --flow requested but git-flow already installed",
            "# " + '-' * 72,
            "",
            ]

    out = [
        "", "# " + '-' * 72,
        "# Initialize git-flow",
        "# " + '-' * 72,
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
        "", "# " + '-' * 72,
        "# Initialize virtualenv",
        "# " + '-' * 72,
        "virtualenv --no-site-packages --distribute .",
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
            "", "# " + '-' * 72,
            "# ERROR: Nginx config not found: {0}".format(path),
            "# " + '-' * 72,
            "",
            ]
    out += [
        "", "# " + '-' * 72,
        "# Sym-link to the Nginx config from the proper location",
        "# " + '-' * 72,
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


def auto(linux):
    if linux:
        out = [
            "", "# " + '-' * 72,
            "# Sym-link to the init.d script from the proper location",
            "# " + '-' * 72,
            "sudo ln -s /path/to/bin/initd.sh /etc/init.d/__project__",
            "sudo update-rc.d __project__ defaults",
            "",
            "# To no longer start on boot, run:",
            "#    sudo update-rc.d -f __project__ remove",
            "",
            ]
    else:
        out = [
            "", "# " + '-' * 72,
            "# TODO: Darwin autostart", # TODO
            "# " + '-' * 72,
            "",
            ]
    return out


def start(opt, linux):
    out = []

    if '--auto' in opt and '--nginx' not in opt:
        out += [
            "", "# " + '-' * 72,
            "# WARNING: --auto set without --nginx",
            "# The production server will start but the FCGI will not be served by Nginx",
            "# This is potentially okay if it was specifically intended",
            "# " + '-' * 72,
            "",
            ]

    if '--auto' in opt:
        out += [
            "", "# " + '-' * 72,
            "# Start the production server",
            "# " + '-' * 72,
            "echo",
            "echo " + '-' * 80,
            "echo Starting production server",
            ]
        if linux:
            out += [
                "echo '    sudo /etc/init.d/__project__ start'",
                "sudo /etc/init.d/__project__ start",
                ]
        else:
            out += [
                "echo '    ./etc/production.ini start'",
                "./etc/production.ini start",
                ]
        out += [
            "echo " + '-' * 80,
            "",
            ]

    out += [
        "", "# " + '-' * 72,
        "# Local server instructions",
        "# " + '-' * 72,
        "echo",
        "echo " + '-' * 80,
        "echo '    To run the local development server:'",
        "echo '    ./etc/local.ini'",
        "echo " + '-' * 80,
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
        'auto',
        'nginx=',
        'help',
        ])
    argv = opt[1]
    opt = dict(opt[0])

    if '-h' in opt or '--help' in opt or (len(opt) == 0 and len(argv) == 0):
        syntax()
        return 1

    if 'restart' in argv:
        restart('--nginx' in argv)
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
        out += auto(linux)

    out += start(opt, linux)

    out += [
        "",
        "# " + '-' * 72,
        "# ",
        "#    If the script is correct, run the following to deploy:",
        "# ",
        "#    python {0}".format(' '.join(sys.argv) + ' | sh'),
        "# ",
        "# " + '-' * 72,
        "",
        ]

    print "\n".join(out)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
