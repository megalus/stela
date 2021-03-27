install:
	@poetry install
	@poetry run pre-commit install -f

test:
	@poetry run pytest -v -x -p no:warnings --cov-report term-missing --cov=./stela

ci:
	@poetry run pytest --cov=./stela

format:
	@poetry run black .

pre-commit:
	@poetry run pre-commit run --all
