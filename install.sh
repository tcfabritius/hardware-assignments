#!/bin/bash
# OSX and Linux have python3 with different names.
case "$(uname)" in

   Darwin*)
     #for OSX use python
     python -m http.server &
     ;;

   MINGW*)
     #for MINGW use python launcher
     py -m http.server &
     ;;

   Linux*)
     #for Linux use python3
     python3 -m http.server &
     ;;
esac

comport=`mpremote connect list | grep 2e8a:0005 | cut -d' ' -f1`
mpremote connect $comport mip install --target / http://localhost:8000/
kill $!
#pkill -f http.server
