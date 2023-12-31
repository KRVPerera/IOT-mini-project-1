#!/bin/bash

sudo docker stop server-grafana-1
sudo docker stop server-coap_server-1
sudo docker stop server-influxdb-1
sudo docker container prune
sudo docker system prune -a
cd app
sudo docker build . --no-cache
cd ..
sudo docker compose up --build -d