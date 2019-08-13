# PM2.5 http Server
This repository includes http server to be run on Synology NAS, along with docker setting files.

## Requirements
Docker

## How to turn on servers and mongodb
1. ssh to the machine and sudo -i
2. navigate to volumes1/docker/server
3. docker-compose up --build --force-recreate -d

## run pylint
navigate to project directory and input pylint **/*.py

## check logs
docker-compose logs http_server
