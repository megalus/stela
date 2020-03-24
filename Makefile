install:
	@poetry install

test:
	@poetry run pytest -v -x -p no:warnings --cov-report term-missing --cov=./stela

ci:
	poetry run yamllint --no-warnings . && poetry run pytest --cov=./stela --black --mypy --pydocstyle

format:
	@poetry run black .
