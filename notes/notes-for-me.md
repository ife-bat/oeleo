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

1. figure out how to make tests
2. figure out how to make sure it restarts when stopped
3. add some way of viewing the db easily
4. add OELEO_DIST_BINARIES_PATH to the config and a method for downloading the binaries from remote server
5. remove loading dotenv files within the package!!!
   r"C:\scripting\oeleo\.env"


### Error 2 (ssh connector aborts when encountering exception (permission denied))

```text
[2023-11-17 11:57:47,479 - oeleo] ||   DEBUG || Copying C:\Data_split\20220407_slt27a_02_cc_01.h5 to /mnt/data-raw/arbin05/20220407_slt27a_02_cc_01.h5
[2023-11-17 11:58:33,344 - oeleo] ||   DEBUG || GOT AN EXCEPTION DURING COPYING FILE
[2023-11-17 11:58:33,344 - oeleo] ||   DEBUG || FROM     : C:\Data_split\20220407_slt27a_02_cc_01.h5
[2023-11-17 11:58:33,344 - oeleo] ||   DEBUG || TO       : /mnt/data-raw/arbin05/20220407_slt27a_02_cc_01.h5
[2023-11-17 11:58:33,344 - oeleo] ||   DEBUG || EXCEPTION:
[2023-11-17 11:58:33,344 - oeleo] ||   DEBUG || [Errno 13] Permission denied
[2023-11-17 11:58:33,359 - oeleo] ||   DEBUG || 20220407_slt27a_02_cc_01.h5 -> /mnt/data-raw/arbin05/20220407_slt27a_02_cc_01.h5 FAILED COPY!
```


## deps
    
```text
peewee, invoke, commonmark, urllib3, sspilib, six, 
python-dotenv, pygments, pycparser, 
lxml, idna, charset-normalizer, certifi, bcrypt, rich, 
requests, pathlib2, cffi, requests-toolbelt, pynacl, 
cryptography, pyspnego, paramiko, requests-ntlm, 
Fabric, SharePlum, 
```