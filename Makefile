.PHONY: init init-migration build run db-migrate test tox clean deploy

clean:
	rm -rf build
	rm -rf dist

init:  build run
	docker-compose exec web flask db init
	docker-compose exec web flask db migrate
	docker-compose exec web flask db upgrade
	docker-compose exec web flask init
	@echo "Init done, containers running"

build:  clean
	python setup.py bdist_wheel

deploy: $(wildcard dist/*.whl)
	scp $? root@urbangirlyarns.site:/root/incoming

run:
	@mkdir -p db
	docker-compose up -d

db-init:
	docker-compose exec web flask db init

db-migrate:
	docker-compose exec web flask db migrate

db-upgrade:
	docker-compose exec web flask db upgrade

test:
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e test

tox:
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e py38
