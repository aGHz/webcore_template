Web app template using WebCore, Paste, Flup and Nginx
=====================================================

Setting up a new project
------------------------

Replace `PROJECT` with the name of your project,
`PROJ_PATH` with the absolute path to the directory where you cloned this repository
and `PROJ_URL` with the url of the git repository for your new project.

# `git clone git@github.com:aGHz/webcore_template.git PROJ_PATH -b master`
# `cd PROJ_PATH`
# `git remote rm origin`

# `git mv src/__project__ src/PROJECT`
# `grep -rl __project__ * | xargs sed -i '' 's|__project__|PROJECT|g'`
# `grep -rl '/path/to' * | xargs sed -i '' 's|/path/to|PROJ_PATH|g'`
# `vim .gitmodules` -- update submodule repo URLs as needed
# `git commit -a -m 'Customized WebCore template'`

# `git reset --soft TAIL`
# `git commit --amend -m 'Initialized repository from WebCore template'`

# `git remote add origin PROJ_URL`
# `git push -u origin master`
# `git submodule init`
# `git submodule update`

# `git flow init`
# `git push -u origin develop`

