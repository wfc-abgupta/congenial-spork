.PHONY: deps run migrate run-ui deps-ui

deps:
	pip install -r requirements.txt

deps-ui:
	cd frontend && npm i

run: deps migrate
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

test:
	python manage.py test -v2

run-ui: deps-ui
	cd frontend && ./node_modules/webpack-cli/bin/cli.js --watch