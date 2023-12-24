#!/usr/bin/bash

RES=$(iotlab-experiment submit -n project-1 -d 120 -l 2,archi=m3:at86rf231+site=grenoble
ID=$(echo $RES | jq '.id')
iotlab-ssh --verbose wait-for-boot
iotlab-experiment wait --timeout 80 --cancel-on-timeout -i "${ID}" --state Running
RES=$(iotlab-experiment get -i ${ID} -p)

mynodes=()

for (( i=0; i<2; i++ )); do
    node=$(echo "$RES" | jq -r ".nodes[$i]")
    number=$(echo "$node" | cut -d'-' -f2 | cut -d'.' -f1)
    mynodes+=( "$number" )
done

