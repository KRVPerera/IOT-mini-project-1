#!/bin/bash
cd app
sudo docker build . --no-cache
cd ..
sudo docker compose up --build -d

sudo docker logs -f server-coap_server-1