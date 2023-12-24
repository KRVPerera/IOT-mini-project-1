#!/usr/bin/bash

git clone https://github.com/RIOT-OS/RIOT.git -b 2020.10-branch

cd sensor
make

cp bin/iotlab-m3/sensor.elf ../