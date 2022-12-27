# `placy`

This is the backend repository for `placy`.


This README will be elaborated later.

## Initalize the environment

For doing this you need few applications installed.

- `poethepoet`
- `poetry`


You can install make using your package manager, or using other on windows.

`poetry` can be installed using `pip`/`pipx` just like any other module.
`poethepoet` can be installed using `pip`/`pipx` just like any other module.

For installing those.
```sh
pip install poetry poethepoet.
```

After doing this simply Run

```sh
poe init
```
This would do multiple things
- Setup a virtual environment automatically.
- Install all dependencies within the virtual environment.
- Install multiple tools like formatters, test-runners and documentation tools.
- Install `pre-commit` and initialize the git-hooks.


## Format code

```sh
poe format
```


## Run the application

Simple
```sh
poe run
```


## Generate documentation

```sh
poe doc
```

Documentation would be at `docs/authentication`. A temporary location, serve it using a simple http server `python -m http.server` and then view on your browser.

## Git Hooks

Through `pre-commit`. Git Hooks are installed, you will not be allowed to commit any file without running documentation check and formatting check. If the tools don't pass, YOU NEED TO ADD THE CHANGED FILES AGAIN. Use `git status` to view which files were changed after the git-hooks pipeline.

The tools configured for git-hooks are

- `black` A simple formatter
- `pydocstyle`. Makes documentation compulsory. If possible integrate into the editor for maximum efficiency.
- `basic`. This includes end-of-line fixers and other utilities.
