import getopt
import os
import sys


def syntax():
    print """Generate setup instructions for the WebCore starter kit at https://github.com/aGHz/webcore_template/

Syntax:
    python setup.py [options] PROJECT
    python setup.py -n PROJECT [-p PROJ_PATH] [-u PROJ_URL] [--submodules=<...>] [--no-flow]

Options:
    -n/--name=       The name of the project (can be specified without -n)
    -p/--path=       Absolute path for the project, defaults to `pwd`/PROJECT
    -u/--url=        Git repository url for remote origin
                     Skip remote-related commands if omitted
    --submodules=    Submodule root, e.g. git@github.com/marrow, https://github.com/fork
                     Must expose the repositories: WebCore, marrow.templating, marrow.util
    --no-flow        Skip git-flow commands. Not recommended.

Examples:
    python setup.py Project
    python setup.py -n Project -p /home/me/src/Project
    python setup.py -u git@github.com:me/myproject --submodules=git@github.com/me Project

    curl http://aghz.ca/webcore.py | python - MyProject | sh

Additional information at http://aghz.ca/webcore.readme
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
        out.extend([
            "sed -i '' 's|https://github.com/marrow|{submodules}|' .gitmodules",
            ])

    out.extend([
        "git commit -a -m 'Customized WebCore template'",
        "git reset --soft TAIL",
        "git commit --amend -m 'Initialized repository from WebCore template'",
        ])

    if url is not None:
        out.extend([
            "git remote add origin {url}",
            "git push -u origin master",
            ])

    out.extend([
        "git submodule init",
        "git submodule update",
        ])

    if flow:
        out.extend([
            "git flow init",
            ])

    if url is not None and flow:
        out.extend([
            "git push -u origin develop",
            ])

    print "\n".join(out).format(name=name, path=path, url=url, submodules=submodules, name_equals='='*len(name))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
