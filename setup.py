import getopt
import os
import sys


def syntax():
    print """Generate setup instructions for the WebCore starter kit

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
    python setup.py -u git@github.com:me/my_project --submodules=git@github.com/me MyProject

    curl -sL http://aghz.ca/webcore.py | python - MyProject | sh

Additional information:
    https://github.com/marrow/WebCore
    https://github.com/aGHz/webcore_template
"""

def main(argv):
    opt = getopt.getopt(argv, 'hn:p:u:', [
        'name=',
        'path=',
        'url=',
        'submodules=',
        'no-flow',
        'help',
        ])
    argv = opt[1]
    opt = dict(opt[0])
    name = opt.get('-n', opt.get('--name', None))
    path = opt.get('-p', opt.get('--path', None))
    url = opt.get('-u', opt.get('--url', None))
    submodules = opt.get('--submodules', None)
    flow = '--no-flow' not in opt

    if '-h' in opt or '--help' in opt:
        syntax()
        return 1

    if name is None:
        if len(argv) == 1:
            name = argv[0]
            print '# Name option not specified, assuming project name is "{name}"'.format(name=name)
        else:
            syntax()
            return 1
    if path is None:
        path = os.path.join(os.getcwd(), name)
        print '# Path option not specified, assuming "{path}"'.format(path=path)

    out = [
        "git clone -b master https://github.com/aGHz/webcore_template.git {path}",
        "cd {path}",
        "git remote rm origin",
        "git rm setup.py",
        "echo \"{name}\\n{name_equals}\\n\\n\" > README.md",
        "git mv src/__project__ src/{name}",
        "grep -rl __project__ * | xargs sed -i '' 's|__project__|{name}|g'",
        "grep -rl '/path/to' * | xargs sed -i '' 's|/path/to|{path}|g'",
        ]

    if submodules is not None:
        out += [
            "sed -i '' 's|https://github.com/marrow|{submodules}|' .gitmodules",
            ]

    out += [
        "git commit -a -m 'Customized WebCore template'",
        "git reset --soft TAIL",
        "git commit --amend -m 'Initialized repository from WebCore template'",
        ]

    if url is not None:
        out += [
            "git remote add origin {url}",
            "git push -u origin master",
            ]

    out += [
        "git submodule update --init --recursive",
        ]

    if flow:
        out += [
            "git flow init",
            ]

    if url is not None and flow:
        out += [
            "git push -u origin develop",
            ]

    print "\n".join(out).format(name=name, path=path, url=url, submodules=submodules, name_equals='='*len(name))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
