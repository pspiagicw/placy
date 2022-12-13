init:
	poetry install
	poetry run pre-commit install
test:
	poetry run pytest
format:
	poetry run black placy tests
doc:
	poetry run pdoc -o docs placy
run:
	poetry run python -m placy
.PHONY: init test format doc
