#!/bin/bash
cd "${0%/*}"

raspistill -o ./plant_stills/plant_$(date +%FT%T).jpg --annotate 12 --width 1280 --height 720 --quality 10 --shutter 5000
