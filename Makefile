test_be: 
	cd backend && export ENVIRONMENT=testing && python -m pytest -vv 

test_be_single: 
	cd backend && export ENVIRONMENT=testing && python -m pytest -vv -k $t

format_be: 
	isort backend
	ruff format backend
	ruff check --fix backend

test_fe:
	cd frontend && yarn test

test_fe_single:
	cd frontend && node_modules/.bin/jest -t $t

format_fe:
	cd frontend && yarn format

format: format_be format_fe

run_be:
	cd backend && export ENVIRONMENT=development && python pre_start.py && python main.py

run_fe:
	cd frontend && yarn dev

test: test_be test_fe
