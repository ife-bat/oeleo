# Some notes

## Download to PC without internet access

1. create a complete requirements.txt file
    ```pip freeze > oeleo_requirements.txt```
2. download wheels (most likely you need win32 wheels)
   ```
   # inside a the folder you plan to move to disconnected PC
   
   > pip download --platform win32 --no-deps -r oeleo_requirments.txt 
   > pip download --platform win32 --no-deps oeleo=="0.3.1"
   ```
3. get the folder with all the wheels to the offline PC
4. you might also need to bring with you the appropriate python installer (python.org)
5. install
   ```
   > pip install --no-index --find-links=oeleo_wheels oeleo_wheels\oeleo-0.3.1-py3-none-any.whl
   ```
   
## List of things to improve

1. figure out how to make tests
2. figure out how to make sure it restarts when stopped
3. add some way of viewing the db easily
   