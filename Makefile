install:
	python -m pip install --upgrade pip
	python -m pip install --upgrade poetry
	poetry install --no-root

lock:
	poetry lock --no-update

update:
	poetry update

amend:
	git commit --amend --no-edit -a

format:
	poetry run ruff format todo tests
	poetry run ruff check todo tests --fix

lint:
	poetry run ruff format todo tests --check
	poetry run ruff check todo tests
	poetry run mypy todo tests

test:
	poetry run pytest tests \
		--last-failed \
		--cov
	rm -rf tests/.flask_session

run:
	poetry run flask --app todo.app run
