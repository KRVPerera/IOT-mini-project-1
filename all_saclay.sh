#!/bin/bash

source /opt/riot.source
git clone https://github.com/RIOT-OS/RIOT.git -b 2020.10-branch

cd sensor_saclay
make DEFAULT_CHANNEL=14
cp bin/iotlab-m3/sensor.elf ../firmware/sensor_saclay.elf
cd ..

./start_saclay.sh