#!/bin/bash
# OSX and Linux have python3 with different names. Comment out the line that doesn't work for your system
#for OSX use python
python -m http.server &
#for Linux use python3
python3 -m http.server &
comport=`mpremote connect list | grep 2e8a:0005 | cut -d' ' -f1`
mpremote connect $comport mip install --target / http://localhost:8000/
pkill -f http.server
