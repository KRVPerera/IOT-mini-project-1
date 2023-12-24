#!/bin/bash

## installing docker
sudo yum update
sudo yum search docker
sudo yum info docker
sudo yum install docker
sudo usermod -a -G docker ec2-user
id ec2-user
newgrp docker

sudo yum install python3-pip
pip3 install --user docker-compose


sudo systemctl enable docker.service
sudo systemctl start docker.service
sudo systemctl status docker.service

#sudo systemctl start docker.service #<-- start the service
#sudo systemctl stop docker.service #<-- stop the service
#sudo systemctl restart docker.service #<-- restart the service
#sudo systemctl status docker.service #<-- get the service status