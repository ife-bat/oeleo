# Configuration

Configuration is done with environment variables, typically via a `.env` file loaded with `python-dotenv`.

## Example `.env`

```.env
OELEO_BASE_DIR_FROM=C:\data\local
OELEO_BASE_DIR_TO=C:\data\pub
OELEO_FILTER_EXTENSION=.csv
OELEO_DB_NAME=local2pub.db
OELEO_LOG_DIR=C:\oeleo\logs
# OELEO_RECONNECT=true

## only needed for advanced connectors:
# OELEO_DB_HOST=<db host>
# OELEO_DB_PORT=<db port>
# OELEO_DB_USER=<db user>
# OELEO_DB_PASSWORD=<db user>
# OELEO_EXTERNAL_HOST=<ssh hostname>
# OELEO_USERNAME=<ssh username>
# OELEO_PASSWORD=<ssh password>
# OELEO_KEY_FILENAME=<ssh key-pair filename>

## only needed for SharePointConnector:
# OELEO_SHAREPOINT_USERNAME=<sharepoint username (fallbacks to ssh username if missing)>
# OELEO_SHAREPOINT_URL=<url to sharepoint>
# OELEO_SHAREPOINT_SITENAME=<name of sharepoint site>
# OELEO_SHAREPOINT_DOC_LIBRARY=<name of sharepoint library>
```

Never commit a real `.env` file. See `.env_example` in the repository for a template.

## Environment variables reference

### Core transfer settings

- `OELEO_BASE_DIR_FROM`: local source directory.
- `OELEO_BASE_DIR_TO`: destination directory (local or remote, depending on connector).
- `OELEO_FILTER_EXTENSION`: file extension filter (include the dot, e.g. `.csv`).
- `OELEO_DB_NAME`: sqlite database filename used for bookkeeping.
- `OELEO_LOG_DIR`: directory for log files; defaults to the current working directory.
- `OELEO_RECONNECT`: when `true` / `1` / `yes`, reconnect the destination connector before each changed file (useful on flaky networks). Default is off so SSH runs keep one session across files. A failed copy still reconnects once and retries regardless of this setting. Factories also accept a `reconnect=` kwarg that overrides the env var.
- **Destination connection checks:** before each `Worker.run` (and again after a copy fails even with reconnect-retry), oeleo probes the destination via `Connector.ensure_connection()`. If the target directory/host/SharePoint library is gone, the current run aborts with `OeleoConnectionError` instead of marking every remaining file as failed. `SimpleScheduler` catches that error, reports it, and waits for the next interval so a temporary VPN/mount outage does not kill the process.

### SSH connector settings

- `OELEO_EXTERNAL_HOST`: SSH host (optionally with port, e.g. `host:2222`).
- `OELEO_USERNAME`: SSH username.
- `OELEO_PASSWORD`: SSH password (used when connecting with password).
- `OELEO_KEY_FILENAME`: SSH private key path (used when connecting with key-pair).

### SharePoint connector settings

- `OELEO_SHAREPOINT_URL`: SharePoint base URL (e.g. `https://yourcompany.sharepoint.com`).
- `OELEO_SHAREPOINT_SITENAME`: SharePoint site name.
- `OELEO_SHAREPOINT_DOC_LIBRARY`: SharePoint document library name.
- `OELEO_SHAREPOINT_USERNAME`: SharePoint username; falls back to `OELEO_USERNAME` if unset.

### App settings (`app/oa.pyw`)

- `OA_SINGLE_RUN`: run once and exit when `true`.
- `OA_ADD_CHECK`: run the check step before copying when `true`.
- `OA_MAX_RUN_INTERVALS`: number of scheduler runs before stopping.
- `OA_HOURS_SLEEP`: hours to sleep between runs.
- `OA_FROM_YEAR`: filter out files older than this year.
- `OA_FROM_MONTH`: filter out files older than this month.
- `OA_FROM_DAY`: filter out files older than this day.
- `OA_STARTS_WITH`: only include files starting with any of these prefixes; delimit with `;`.
- `OA_INCLUDE_SUBDIRS`: include subdirectories in local search when `true`.
- `OA_EXTERNAL_SUBDIRS`: include subdirectories on the destination when `true`.
