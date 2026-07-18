# oeleo

Python package / app for transferring files from an instrument PC to a data server.

`oeleo` (“one-eyed”) tracks transfer state only on the **local** side via a SQLite bookkeeping database keyed by checksum changes. Destination files are not the source of truth.

## Features (and limitations)

- SSH transfers should preferably use key-pairs. That may require ACL setup on the server so the `oeleo` user only has access to the data folder.
- Password-based SSH is supported if key-based ownership setup is impractical.
- Tracking of duplicate state is local-only. A `check` method can help decide whether copying is safe and optionally populate the database.
- The bookkeeping DB is stored relative to the folder `oeleo` is running from. If deleted, `oeleo` creates a new empty one on the next run.
- Configuration is done with environment variables (see [Configuration](configuration.md)).

## Documentation

- [Install](install.md)
- [Usage](usage.md)
- [Configuration](configuration.md)
- [Database](database.md)
- [Development](development.md)

Full docs also live in this repository under `docs/`. Once Read the Docs is connected, the published site will be the primary reference.

## Status

- Works PC → PC, PC → server, instrument PC → server
- Deployable; published on PyPI
- Fairly easy to use; easier debugging of runs (e.g. editing SQL) still open

## Future ideas

No promises — just notes:

- nicer printing and logging
- CLI
- executable (partly done — see the `app/` folder)
- web app
- GUI (unlikely)

## Licence

MIT

## Hints

Silence noisy paramiko / Fabric / Invoke logs:

```python
import logging

for name in ("paramiko", "fabric", "invoke"):
    logging.getLogger(name).setLevel(logging.WARNING)
```
