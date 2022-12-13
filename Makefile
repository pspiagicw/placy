init:
	poetry install
	poetry run pre-commit install
	pre-commit
test:
	poetry run pytest
format:
	poetry run black placy tests
doc:
	pydocstyle
	poetry run pdoc -o docs placy
run:
	poetry run python -m placy
.PHONY: init test format doc
