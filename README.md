# oeleo
Python app for transferring files from an instrument-PC to a data server 


## Features (or limitations)
- Transferring using an ssh connection should preferably be used with key-pairs. This might involve some
  setting up on your server (ACL) to prevent security issues (the `oeleo` user should only have access to
  the data folder on your server).
- Accessing ssh can be done using password if you are not able to figure out how to set proper ownerships 
  on your server.
- Tracking of the "state of the duplicates" is only performed on the local side (where `oeleo` is running).
- However, `oeleo` will contain a `check` method or similar that can help you figure out if starting copying is a  
  good idea or not.
- The db that stores information about the "state of the duplicates" is stored in the same folder 
  as the `oeleo` is running. If you delete it (by accident?), `oeleo` will make a new empty one from scratch.
- Configuration is done using environmental variables. 

## Next
- make `worker.check()` update the database (using `code` or maybe I should add other columns?)
- make mover classes instead of functions
- implement proxy for `peewee` database

## Status
- [x] Works on my PC &rarr; PC
- [x] Works on my PC &rarr; my server
- [ ] Works on my server &rarr; my server
- [ ] Works on my instrument PC &rarr; my instrument PC
- [ ] Works on my instrument PC &rarr; my server
- [ ] Works OK
- [ ] Deployable

## Licence
MIT

Read more [here](./LICENSE.md).

## Development lead
- Jan Petter Maehlen, IFE
