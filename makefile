SHELL=/bin/bash -euo pipefail

COMPOSE_ARGS=-f ./local/compose/docker-compose.yml

.PHONY: build up upbuild down clean ps shell install remove_pyc update_virtualenv remove_db create_db


build:
	docker-compose ${COMPOSE_ARGS} build

up:
	docker-compose ${COMPOSE_ARGS} up

upbuild:
	docker-compose ${COMPOSE_ARGS} up --build

down:
	docker-compose ${COMPOSE_ARGS} down

clean:
	docker-compose ${COMPOSE_ARGS} down --remove-orphans -v

shell:
	docker exec -it --user root compose_django_1 bash

install: remove_pyc update_virtualenv remove_db create_db load_fixtures

remove_pyc:
	-find . -type f -name "*.pyc" -delete

update_virtualenv:
	pip install -r www/deploy/requirements.txt

remove_db:
	python www/manage.py reset_db --router=default --noinput

create_db:
	python www/manage.py syncdb --noinput
	python www/manage.py migrate

load_fixtures:

test:
	www/runtests.sh

ci: install test
