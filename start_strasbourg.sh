#!/bin/bash

# schdeule two m3 nodes
# got help from discord channel for the subject
RES=$(iotlab-experiment submit -n project-2 -d 480 -l 3,archi=m3:at86rf231+site=strasbourg)
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

iotlab-node --flash gnrc_border_router.elf -l "strasbourg,m3,${mynodes[1]}" -i "${ID}"
iotlab-node --flash firmware/sensor_strasbourg.elf -l "strasbourg,m3,${mynodes[2]}" -i "${ID}"
sleep 30
sudo ethos_uhcpd.py m3-${mynodes[1]} tap9 2a07:2e40:fffe:00e9::1/64
iotlab-experiment stop -i ${ID}