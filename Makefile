dependencies:
	poetry install --with dev
	poetry run pre-commit install

.PHONY: dependencies