test: format
	poetry run pytest
init:
	poetry install
	poetry run pre-commit install
	poetry run pre-commit
format:
	poetry run black authentication tests
doc:
	poetry run pydocstyle
	poetry run pdoc -o docs/authentication src/authenticatoin
run: format
	poetry run python -m authentication
.PHONY: init test format doc
