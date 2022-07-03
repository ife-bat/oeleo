# oeleo
Python app for transferring files from an instrument-PC to a data server 


## Features (or limitations)
- Transferring using an ssh connection can only be used with key-pairs.
- Tracking of the "state of the duplicates" is only performed on the local side (where `oeleo` is running).
- However, `oeleo` will contain a `check` method or similar that can help you figure out if starting copying is a  
  good idea or not.
- The db that stores information about the "state of the duplicates" is stored in the same folder 
  as the `oeleo` is running. If you delete it (by accident?), `oeleo` will make a new empty one from scratch.
- Configuration is done using environmental variables.

## Next
- make connectors (`fabric`) and implement first for `worker.check()`
- make `worker.check()` update the database (using `code` or maybe I should add other columns?)
- make mover classes instead of functions
- make ssh mover class
- implement proxy for `peewee` database


## Development lead
- Jan Petter Maehlen, IFE
