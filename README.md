Web app template
================
using WebCore, Paste, Flup and Nginx
 
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

Semi-automatic setup
--------------------

