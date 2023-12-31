#!/bin/bash

sudo docker stop server-grafana-1
sudo docker container prune
sudo docker compose up --build -d