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

#docker network create -d bridge intranet
db:
	docker run --network=intranet -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Pass12345" -p 1433:1433 --name intranet-mssql --hostname intranet-mssql -d mcr.microsoft.com/mssql/server:2022-latest
