Web app template
================
A useful starter kit for web applications using
[WebCore](https://github.com/marrow/WebCore),
[Paste](http://pythonpaste.org/),
[Flup](http://trac.saddi.com/flup) and
[Nginx](http://wiki.nginx.org/Main)
 
tl;dr
-----

    curl -sL http://aghz.ca/webcore.py | python -

Setting up a new project
------------------------

Replace `PROJECT` with the name of your project,
`PROJ_PATH` with the absolute path to the directory where you cloned this repository
and `PROJ_URL` with the url of the git repository for your new project.

1. `git clone -b master git@github.com:aGHz/webcore_template.git PROJ_PATH`
2. `cd PROJ_PATH`
3. `git remote rm origin`
4. `git mv src/__project__ src/PROJECT`
5. `grep -rl __project__ * | xargs sed -i '' 's|__project__|PROJECT|g'`
6. `grep -rl '/path/to' * | xargs sed -i '' 's|/path/to|PROJ_PATH|g'`
7. `vim .gitmodules` -- update submodule repo URLs as needed
8. `git commit -a -m 'Customized WebCore template'`
9. `git reset --soft TAIL`
10. `git commit --amend -m 'Initialized repository from WebCore template'`
11. `git remote add origin PROJ_URL`
12. `git push -u origin master`
13. `git submodule init`
14. `git submodule update`
15. `git flow init`
16. `git push -u origin develop`


Customized setup instructions script
------------------------------------

A [script](https://github.com/aGHz/webcore_template/blob/master/setup.py) is provided
to generate customized setup instructions.

    python setup.py -n PROJECT -p PROJ_PATH [-u PROJ_URL]
    python setup.py --name=PROJECT --path=PROJ_PATH [--url=PROJ_URL]

Omitting `-u/--url` will not generate instructions related to uploading to a new remote (11, 12 and 16).

To alter the submodules URL for step 7 above, use the `--submodules` option.
Without it, the vanilla .gitmodules provided in this repository is used,
which downloads from the read-only repositories provided by [marrow](http://github.com/marrow/) on GitHub.
If instead you want to enable read-write access or use a fork, specify

    python setup.py ... --submodules=git@github:marrow
    python setup.py ... --submodules=https://github.com/fork

If you don't want to use [git-flow](https://github.com/nvie/gitflow/) (even though you [should](http://nvie.com/posts/a-successful-git-branching-model/)),
specify `--no-flow`.

Semi-automatic and automatic setup
----------------------------------

The raw script is available for direct download from
[GitHub](https://raw.github.com/aGHz/webcore_template/master/setup.py)
or from the shorter URL [http://aghz.ca/webcore.py](http://aghz.ca/webcore.py).
The script can be grabbed via `curl` and piped to `python` to very easily generate
a working set of instructions.

    curl -sL http://aghz.ca/webcore.py | python - -n PROJECT -p PROJ_PATH

If you don't have any special needs and you fully trust the script, you can also pipe the output
directly to `sh` for an automatic setup:

    curl -sL http://aghz.ca/webcore.py | python - -n PROJECT -p PROJ_PATH | sh

If you go the parent directory of your new project (e.g. `cd ~/src`), this is even nicer:

    curl -sL http://aghz.ca/webcore.py | python - PROJECT | sh

