# Create a win desktop app for Oeleo

Easiest way to build an app is to use the auto-py-to-exe tool.

```bash
poetry add auto-py-to-exe -G dev

# run the tool (dont use py3.10.0 - it has a bug)
poetry run auto-py-to-exe
```

There should also be a config.json file in the app folder. This is the config file for the auto-py-to-exe tool.
You can load it in the through the Settings menu in the tool.

## Installing using pyinstaller

```bash
pyinstaller --noconfirm --onefile --windowed --icon "C:/scripting/oeleo/app/oeleo.ico" --name "start" --hidden-import "pystray._win32 oa.pyw"  
```