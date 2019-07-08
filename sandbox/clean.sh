#!/bin/bash
#docker-compose down -v --rmi all --remove-orphans
#docker container prune
#docker network prune
#docker volume prune
#docker image prune
#docker builder prune
docker system prune

docker image prune -a
