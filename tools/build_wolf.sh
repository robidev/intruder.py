#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

#docker network connect bridge wolf
#sudo docker exec -ti wolf /bin/ash
echo -e "\e[32m[+] build wolf container(s)\e[0m"
docker build -t sandbox_wolf:latest -f Dockerfile.wolf .

echo -e "\e[32m[+] build sheep container(s)\e[0m"
docker-compose -f docker-compose.sheep.yml build