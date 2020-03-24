install:
	@poetry install
	rm -rf ./src

test:
	@poetry run pytest -v -x -p no:warnings --cov-report term-missing --cov=./stela

pre-ci:
	@poetry export --without-hashes -f requirements.txt -o ./requirements.txt
	@pip install -r requirements.txt

ci:
	@yamllint --no-warnings . && @poetry run pytest --cov=./stela --black --mypy --pydocstyle

format:
	@poetry run black .
