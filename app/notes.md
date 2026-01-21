# Create a win desktop app for Oeleo

Easiest way to build an app is to use the auto-py-to-exe tool.

```bash
uv add --dev auto-py-to-exe

```

# run the tool (dont use py3.10.0 - it has a bug)
```bash
uv run auto-py-to-exe

```

There should also be a config.json file in the app folder. This is the config file for the auto-py-to-exe tool.
You can load it in the through the Settings menu in the tool.

## Installing using pyinstaller

You can run pyinstaller through auto-py-to-exe after all the settings are inserted (for example by loading config.json).
The pyinstaller command should be something like this:

```bash
pyinstaller --noconfirm --onefile --windowed --icon "C:/scripting/oeleo/app/oeleo.ico" --name "start" --hidden-import "pystray._win32 oa.pyw"  
```