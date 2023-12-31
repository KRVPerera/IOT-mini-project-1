#!/bin/bash

sudo docker stop server-coap_server-1
sudo docker container prune
cd app
sudo docker build . --no-cache
cd ..
sudo docker compose up --build -d