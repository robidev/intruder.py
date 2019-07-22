#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

cd ../sandbox/

echo -e "\e[32m[+] build gamemaster container(s)\e[0m"
docker build -t sandbox_gamemaster:latest -f Dockerfile.gamemaster .

echo -e "\e[32m[+] build sheep container(s)\e[0m"
docker-compose -f levels/docker-compose.sheep.yml build

cd ../tools/