all: fmt lint migrations test

fmt:
	poetry run black src
	poetry run isort src

lint:
	poetry run dotenv-linter .env.example
	poetry run ruff check .
	poetry run mypy .
	poetry run poetry check

migrations:
	poetry run alembic check

test:
	poetry run pytest --numprocesses logical --dist worksteal
