#!/bin/bash

source /opt/riot.source
git clone https://github.com/RIOT-OS/RIOT.git -b 2020.10-branch

# build sensor
cd sensor_grenoble
make DEFAULT_CHANNEL=14
cp bin/iotlab-m3/sensor.elf ../firmware/sensor_grenoble.elf
cd ..

./start_grenoble.sh