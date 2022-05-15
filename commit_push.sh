#!/bin/bash

cd /home/pi/plant_repo

git add ./index.html ./plant_stills ./sensor_data

git commit -m "Mew photo + sensors $(date +%FT%T) purr"

git push
