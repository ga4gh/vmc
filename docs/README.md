# Tips for editing documentation


## Setup up the environment

```
cd vrs-python
make devready
source bin/venv/3.8/activate
```


## Build the docs once

```
cd submodules/vrs/docs
make html

xdg-open build/html/index.html
```

## Watch the docs and rebuild when necessary

```
make watch &
```

You will need `entr` installed for this to work.

## Edit!

As you make changes, sphinx will be automatically invoked whenever any
file is changed.

N.B. Certain kinds of changes, like deletions, do NOT trigger a
rebuild. In those cases, kill the background job, type `make clean`,
then `make watch &` again.
