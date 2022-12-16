test: format
	poetry run pytest
init:
	poetry install
	poetry run pre-commit install
	poetry run pre-commit
format:
	poetry run black backend tests
doc:
	poetry run pydocstyle
	poetry run pdoc -o docs/backend backend
run: format
	poetry run python -m backend
.PHONY: init test format doc
