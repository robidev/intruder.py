#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

echo -e "\e[32m[+] starting network(s)\e[0m"
docker network create --driver bridge network_master 

echo -e "\e[32m[+] starting container(s)\e[0m"
#docker run -d -p 5000:5000 --name wolf --hostname=wolf --network network_master sandbox_wolf:latest
#docker run -dit -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock --name wolf --hostname=wolf --network network_master sandbox_wolf:latest
docker run -dit -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd)/../sandbox/levels/:/levels/ --name gamemaster --hostname=gamemaster --network network_master sandbox_gamemaster:latest


echo -e "\e[32m[+] starting browser\e[0m"
sudo -u robin xdg-open http://127.0.0.1:5000 &> /dev/null
#sudo -u robin xdg-open http://127.0.0.1:5000/?level=one &> /dev/null

echo -e "\n *** Press enter to stop gamemaster server *** \n"
read
#docker logs -f wolf

echo -e "\e[32m[+] stopping container(s)\e[0m"

#docker-compose -f ../sandbox/docker-compose.sheep.yml down
docker stop gamemaster
docker rm gamemaster

echo -e "\e[32m[+] stopping network(s)\e[0m"
docker network rm network_master 

