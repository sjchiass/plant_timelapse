#!/bin/bash
cd "${0%/*}"

git add ./plant_stills ./sensor_data

git commit -m "Mew photo + sensors $(date +%FT%T) purr"

git push
