#!/bin/bash

docker-compose down
# shellcheck disable=SC2046
docker rmi -f $(docker images -aq)
docker volume rm hsequestwd_static_volume
docker-compose up -d
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py makemigrations quest --noinput
docker-compose exec web python manage.py makemigrations user --noinput
docker-compose exec web python manage.py migrate --noinput
