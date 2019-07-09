#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

cd ../sandbox/
echo -e "\e[32m[+] stopping any running container\e[0m"
docker-compose down

echo -e "\e[32m[+] copying files to sandbox\e[0m"
if ! cp -a ../dev/server/* wolf/; then
  echo -e "\e[31m[-] copying server files to sandbox failed\e[0m"
  exit 1
fi

if ! cp -a ../dev/payload/logger.py sheep/; then
  echo -e "\e[31m[-] copying logger files to sandbox failed\e[0m"
  exit 1
fi

echo -e "\e[32m[+] (re)building container(s)\e[0m"
if ! docker-compose build; then
  echo -e "\e[31m[-] building container(s) failed\e[0m"
  exit 1
fi

echo -e "\e[32m[+] starting container(s)\e[0m"
if ! docker-compose up -d; then
  echo -e "\e[31m[-] starting container(s) failed\e[0m"
  exit 1
fi

echo -e "\e[32m[+] starting browser\e[0m"
sudo -u robin xdg-open http://127.0.0.1:5000 &> /dev/null

echo -e "\n *** Press enter to stop server *** \n"
read

echo -e "\e[32m[+] stopping container(s)\e[0m"
docker-compose down

cd ../dev/