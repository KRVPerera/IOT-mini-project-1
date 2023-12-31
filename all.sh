#!/bin/bash
source /opt/riot.source
git clone https://github.com/RIOT-OS/RIOT.git -b 2020.10-branch

cd sensor_saclay
make DEFAULT_CHANNEL=14
cp bin/iotlab-m3/sensor.elf ../firmware/sensor_saclay.elf
cd ..


# build border router
# cd gnrc_border_router
make ETHOS_BAUDRATE=500000 DEFAULT_CHANNEL=14 BOARD=iotlab-m3
cp bin/iotlab-m3/gnrc_border_router.elf ../
cd ..

# run the system
#ping 2001:4860:4860::8888
# ping 2600:1f16:15a8:3b2:804b:8136:56a6:cb5b
#./start.sh

./start_grenoble.sh
# ./start_strasbourg.sh
# ./start_saclay.sh