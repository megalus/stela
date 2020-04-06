install:
	@poetry install

test:
	@poetry run pytest -v -x -p no:warnings --cov-report term-missing --cov=./stela

ci:
	@poetry run pytest --cov=./stela --black --mypy --pydocstyle --ignore=venv36 --ignore=venv37 --ignore=venv38

format:
	@poetry run black .
