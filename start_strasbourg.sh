#!/bin/bash

source /opt/riot.source
git clone https://github.com/RIOT-OS/RIOT.git -b 2020.10-branch

cd sensor_strasbourg
make DEFAULT_CHANNEL=14
cp bin/iotlab-m3/sensor.elf ../firmware/sensor_strasbourg.elf
cd ..

# schdeule two m3 nodes
# got help from discord channel for the subject
RES=$(iotlab-experiment submit -n project-2 -d 480 -l 2,archi=m3:at86rf231+site=strasbourg)
ID=$(echo $RES | jq '.id')

# wait for nodes to start
iotlab-experiment wait --timeout 120 --cancel-on-timeout -i "${ID}" --state Running
RES=$(iotlab-experiment get -i ${ID} -p)
declare -a mynodes
for (( i=0; i<2; i++ )); do
    node=$(echo "$RES" | jq -r ".nodes[$i]")
    number=$(echo "$node" | cut -d'-' -f2 | cut -d'.' -f1)
    mynodes+=( "$number" )
done


echo "Array Contents: ${mynodes[*]}"

iotlab-node --flash gnrc_border_router.elf -l "grenoble,m3,${mynodes[0]}"
iotlab-node --flash firmware/sensor_grenoble.elf -l "grenoble,m3,${mynodes[1]}"

echo "nc m3-2 20000"
sudo ethos_uhcpd.py m3-${mynodes[0]} tap9 2a07:2e40:fffe:00e9::1/64
echo "Script ended."
iotlab-experiment stop -i ${ID}