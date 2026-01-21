# oeleo app

This app example uses the `oeleo` `ssh_worker` (see the script `oa.py` for details.)

## Build app with pyinstaller

### Installing using pyinstaller

You need the full path to the oeleo.ico file. This is located in the app directory.

```bash
pyinstaller --noconfirm --onefile --windowed --icon "full path to oeleo.ico" --name "start" --hidden-import "pystray._win32 oa.pyw"  
```

### Checking installation

Move the "start.exe" file to the check folder. Make sure you have a valid ".env" file (use the "example.env" file as "template") in the same folder as "start.exe"

The ".env" must contain enough information so that it can succesfully connect to your server:

```r
OELEO_BASE_DIR_FROM=C:\scripting\oeleo\check\from
OELEO_BASE_DIR_TO=/somewher_in_myserver
OELEO_FILTER_EXTENSION=.xyz
OELEO_DB_NAME=test_app.db
OELEO_LOG_DIR=log
OELEO_EXTERNAL_HOST=A-IP-NUMBER
OELEO_USERNAME=coolkid
OELEO_PASSWORD=
OELEO_KEY_FILENAME=C:\Users\coolkid\.ssh\id_myserver

# oeleo app config:
OA_SINGLE_RUN=false
OA_MAX_RUN_INTERVALS=200
OA_HOURS_SLEEP=1.0
OA_FROM_YEAR=2023
OA_FROM_MONTH=1
OA_FROM_DAY=1
OA_STARTSWITH=2023;2024
OA_ADD_CHECK=true
```