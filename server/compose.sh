#!/bin/bash

docker exec -it 8bcff95d78f9 /bin/bash

influx -username miniproject1_user -password miniproject1_pass 
## installing docker
INSERT temperature,place=testbed_sensor1 value=25.5

docker compose build --no-cache

docker exec server-coap_server-1 cat /etc/hosts
docker inspect server-coap_server-1
docker exec -it server-coap_server-1 /bin/bash

docker logs server-coap_server-1
docker stop server-coap_server-1
docker container prune
