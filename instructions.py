import sys
import getopt


def main(argv):
    opt = dict(getopt.getopt(argv, 'n:p:u:', ['name=', 'path=', 'url=', 'submodules='])[0])
    name = opt.get('-n', opt.get('--name', None))
    path = opt.get('-p', opt.get('--path', None))
    url = opt.get('-u', opt.get('--url', None))
    submodules = opt.get('--submodules', None)
    if name is None:
        print 'Project name is required, specify using `-n NAME` or `--name=NAME`'
        return 1
    if path is None:
        print 'Absolute project path is required, specify using `-p PATH` or `--path=PATH`'
        return 1

    out = """
#!/bin/sh
git clone -b master git@github.com:aGHz/webcore_template.git {path}
cd {path}
git remote rm origin
git mv src/__project__ src/{name}
grep -rl __project__ * | xargs sed -i '' 's|__project__|{name}|g'
grep -rl '/path/to' * | xargs sed -i '' 's|/path/to|{path}|g'
"""[1:]

    if submodules is not None:
        out += "sed -i '' 's|https://github.com/marrow|{submodules}|' .gitmodules\n".format(submodules=submodules)

    out += """
git commit -a -m 'Customized WebCore template'
git reset --soft TAIL
git commit --amend -m 'Initialized repository from WebCore template'
"""[1:]

    if url is not None:
        out += """
git remote add origin {url}
git push -u origin master
"""[1:]

    out += """
git submodule init
git submodule update
git flow init
"""[1:]

    if url is not None:
        out += """
git push -u origin develop
"""[1:]

    print out.format(name=name, path=path, url=url)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
