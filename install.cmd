start python -m http.server
mpremote mip install --target / http://localhost:8000/
@rem The following line terminates all processes with "python" and "http.server" in them.
wmic process where "name like '%%python%%' and commandline like '%%http.server%%'" delete