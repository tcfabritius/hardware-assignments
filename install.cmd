start python -m http.server
@rem Extract comport name where pico is connected
for /f "tokens=1 delims= " %%a in ('mpremote connect list ^| find "2e8a:0005"') do set comport=%%a
@rem Run mpremote
mpremote connect %comport% mip install --target / http://localhost:8000/
@rem The following line terminates all processes with "python" and "http.server" in them.
wmic process where "name like '%%python%%' and commandline like '%%http.server%%'" delete