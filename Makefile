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
	poetry run ruff format intranet tests
	poetry run ruff check intranet tests --fix

lint:
	poetry run ruff format intranet tests --check
	poetry run ruff check intranet tests
	poetry run mypy intranet tests

test:
	poetry run pytest tests/unit \
		--last-failed \
		--cov

run:
	python -m intranet.runner --host localhost --port 5000
