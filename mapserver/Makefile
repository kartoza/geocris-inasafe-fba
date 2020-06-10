
build:
	@docker build django -t project_uwsgi
	@docker-compose build django-uwsgi-dev

up-docker:
	@docker-compose up -d

up: up-docker django-migrate django-collectstatic
	@docker-compose up -d

down:
	@docker-compose down

ps:
	@docker-compose ps

logs:
	@docker-compose logs -f --tail=30 mapserver

shell:
	@docker-compose exec mapserver bash

wait-mapserver-ready:
	@docker-compose exec mapserver bash -c 'until wget -qO- localhost:80 &> /dev/null; do echo "Mapserver not ready. Waiting."; sleep 10; done; echo "Mapserver ready"'

django-shell:
	@docker-compose exec django-uwsgi bash

django-dev-shell:
	@docker-compose exec django-uwsgi-dev bash

django-migrate:
	@docker-compose exec django-uwsgi python manage.py migrate

django-collectstatic:
	@docker-compose exec django-uwsgi python manage.py collectstatic --noinput

django-create-superuser:
	@docker-compose exec django-uwsgi python manage.py createsuperuser
