#!/bin/bash

# schdeule two m3 nodes
# got help from discord channel for the subject
RES=$(iotlab-experiment submit -n project-2 -d 480 -l 3,archi=m3:at86rf231+site=lille)
ID=$(echo $RES | jq '.id')

# wait for nodes to start
iotlab-experiment wait --timeout 120 --cancel-on-timeout -i "${ID}" --state Running
RES=$(iotlab-experiment get -i ${ID} -p)
declare -a mynodes
for (( i=0; i<3; i++ )); do
    node=$(echo "$RES" | jq -r ".nodes[$i]")
    number=$(echo "$node" | cut -d'-' -f2 | cut -d'.' -f1)
    mynodes+=( "$number" )
done

iotlab-node --flash gnrc_border_router.elf -l "lille,m3,${mynodes[1]}" -i "${ID}"
iotlab-node --flash firmware/sensor_lille.elf -l "lille,m3,${mynodes[2]}" -i "${ID}"
sudo ethos_uhcpd.py m3-${mynodes[0]} tap9 2001:660:4403:0489::1/64
iotlab-experiment stop -i ${ID}