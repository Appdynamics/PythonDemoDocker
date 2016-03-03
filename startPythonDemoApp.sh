#/bin/bash

#!/bin/bash

# This is a script to start Python on Docker

# Set variables
CONTROLLER=
APPD_PORT=
SSL=off
ACCOUNT_NAME=
ACCESS_KEY= 
APP_NAME=
TIER_NAME_1=Flask
NODE_NAME_1=Flask-Node
CONFIG_FILE_1=appdynamics.cfg
APP_FILE_1=pythonapp.py
TIER_NAME_2=Flask2
NODE_NAME_2=Flask-Node2
CONFIG_FILE_2=appdynamics2.cfg
APP_FILE_2=pythonapp2.py
VERSION=latest
PYTHON_APP=
PYTHON_HOST=
BUNDY_APP=

# Start containers
docker run -d --name pythondemo-elasticsearch -p 9200:9200 -p 9300:9300 appdynamics/pythondemo-elasticsearch

sleep 5

docker run -d --name pythondemo-redis -p 6379:6379 appdynamics/pythondemo-redis

sleep 5

docker run -d --name pythondemo-postgres -p 5432:5432 appdynamics/pythondemo-postgres

sleep 5

docker run -d --name pythondemo-mysql -p 3306:3306 appdynamics/pythondemo-mysql

sleep 5

docker run -d --name pythondemo-app1 -e CONTROLLER=${CONTROLLER} -e APPD_PORT=${APPD_PORT} -e SSL=${SSL} -e ACCOUNT_NAME=${ACCOUNT_NAME} -e ACCESS_KEY=${ACCESS_KEY} -e APP_NAME=${APP_NAME} -e TIER_NAME=${TIER_NAME_1} -e NODE_NAME=${NODE_NAME_1} -e CONFIG_FILE=${CONFIG_FILE_1} -e APP_FILE=${APP_FILE_1} -e PYTHON_APP=${PYTHON_APP} -e BUNDY_APP=${BUNDY_APP} -p 5000:5000 --link pythondemo-elasticsearch:pythondemo-elasticsearch --link pythondemo-redis:pythondemo-redis --link pythondemo-postgres:pythondemo-postgres --link pythondemo-mysql:pythondemo-mysql appdynamics/pythondemo-app:${VERSION}

docker run -d --name pythondemo-app2 -e CONTROLLER=${CONTROLLER} -e APPD_PORT=${APPD_PORT} -e SSL=${SSL} -e ACCOUNT_NAME=${ACCOUNT_NAME} -e ACCESS_KEY=${ACCESS_KEY} -e APP_NAME=${APP_NAME} -e TIER_NAME=${TIER_NAME_2} -e NODE_NAME=${NODE_NAME_2} -e CONFIG_FILE=${CONFIG_FILE_2} -e APP_FILE=${APP_FILE_2} -e PYTHON_APP=${PYTHON_APP} -e BUNDY_APP=${BUNDY_APP} -p 1080:1080 --link pythondemo-elasticsearch:pythondemo-elasticsearch --link pythondemo-redis:pythondemo-redis --link pythondemo-postgres:pythondemo-postgres --link pythondemo-mysql:pythondemo-mysql appdynamics/pythondemo-app:${VERSION}

docker run -d --name pythondemo-load -e PYTHON_HOST=${PYTHON_HOST} --link pythondemo-app1:pythondemo-app1 --link pythondemo-app2:pythondemo-app2 appdynamics/pythondemo-load

exit 0
