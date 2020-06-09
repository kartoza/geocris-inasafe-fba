PROJECT_ID := fbf-mapserver
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

wait-geoserver-ready:
	@docker-compose exec mapserver bash -c 'until wget -qO- localhost:8080/geoserver &> /dev/null; do echo "Geoserver not ready. Waiting."; done; echo "Geoserver ready"'

django-migrate:
	@docker exec -t -i $(PROJECT_ID)_django-uwsgi_1 python manage.py migrate

django-collectstatic:
	@docker exec -t -i $(PROJECT_ID)_django-uwsgi_1 python manage.py collectstatic --noinput

django-create-superuser:
	@docker exec -t -i $(PROJECT_ID)_django-uwsgi_1 python manage.py createsuperuser