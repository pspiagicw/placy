# `placy`

This is the backend repository for `placy`.


This README will be elaborated later.

## Initalize the environment

For doing this you need few applications installed.

- `make`
- `poetry`


You can install make using your package manager, or using other on windows.

`poetry` can be installed using `pip`/`pipx` just like any other module.

After doing this simply Run

```sh
make init
```
This would do multiple things
- Setup a virtual environment automatically.
- Install all dependencies within the virtual environment.
- Install multiple tools like formatters, test-runners and documentation tools.
- Install `pre-commit` and initialize the git-hooks.


## Format code

```sh
make format
```


## Run the application

Simple
```sh
make run
```

API documentation can be found after starting the application using `make run`, and then accessing `localhost:5000/docs` or `localhost:5000/redocs`.

## Generate documentation

```sh
make doc
```

Documentation would be at `docs/authentication`. A temporary location, serve it using a simple http server `python -m http.server` and then view on your browser.

## Git Hooks

Through `pre-commit`. Git Hooks are installed, you will not be allowed to commit any file without running documentation check and formatting check. If the tools don't pass, YOU NEED TO ADD THE CHANGED FILES AGAIN. Use `git status` to view which files were changed after the git-hooks pipeline.

The tools configured for git-hooks are

- `black` A simple formatter
- `pydocstyle`. Makes documentation compulsory. If possible integrate into the editor for maximum efficiency.
- `basic`. This includes end-of-line fixers and other utilities.
