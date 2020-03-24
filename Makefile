install:
	@poetry install
	rm -rf ./src

test:
	@poetry run pytest -v -x -p no:warnings --cov-report term-missing --cov=./stela

ci:
	@yamllint --no-warnings . && @poetry run pytest --cov=./stela --black --mypy --pydocstyle

format:
	@poetry run black .
