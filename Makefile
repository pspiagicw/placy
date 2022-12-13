init:
	poetry install
	poetry run pre-commit
test:
	poetry run pytest
format:
	poetry run black placy tests
