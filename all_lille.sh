#!/bin/bash

source /opt/riot.source
git clone https://github.com/RIOT-OS/RIOT.git -b 2020.10-branch

cd sensor_lille
make DEFAULT_CHANNEL=14
cp bin/iotlab-m3/sensor.elf ../firmware/sensor_lille.elf
cd ..

./start_lille.sh