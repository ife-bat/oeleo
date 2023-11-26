# Some notes

## Download to PC without internet access

1. create a complete requirements.txt file
    ```pip freeze > oeleo_requirements.txt```
2. download wheels (most likely you need win32 wheels)
   ```
   # inside a the folder you plan to move to disconnected PC
   
   > pip download --platform win32 --no-deps -r oeleo_requirements.txt 
   > pip download --platform win32 --no-deps oeleo=="0.4.10"
   ```
3. get the folder with all the wheels to the offline PC
4. you might also need to bring with you the appropriate python installer (python.org)
5. install
   ```
   > pip install --no-index --find-links=oeleo_wheels oeleo_wheels\oeleo-0.4.10-py3-none-any.whl
   ```
   
## List of things to improve

1. include app building in the git repository
2. include multi-threading (fix how the log rotation is done)
3. include a nice console reporter with progress bars.


## deps
    
```text
peewee, invoke, commonmark, urllib3, sspilib, six, 
python-dotenv, pygments, pycparser, 
lxml, idna, charset-normalizer, certifi, bcrypt, rich, 
requests, pathlib2, cffi, requests-toolbelt, pynacl, 
cryptography, pyspnego, paramiko, requests-ntlm, 
Fabric, SharePlum, 
```