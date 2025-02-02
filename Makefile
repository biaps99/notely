test_be:
	cd backend && \
	export ENVIRONMENT=testing && \
    uv run pytest -vv

test_be_single:
	cd backend && \
	export ENVIRONMENT=testing && \
	uv run pytest -vv -k $$t

format_be:
	cd backend && \
	uv run ruff format . && \
	uv run ruff check --fix .
	
test_fe:
	cd frontend && yarn test

test_fe_single:
	cd frontend && node_modules/.bin/jest -t $$t

format_fe:
	cd frontend && yarn format

format: format_be format_fe

run_be:
	cd backend && export ENVIRONMENT=development && uv run pre_start.py && uv run main.py

run_fe:
	cd frontend && yarn dev
