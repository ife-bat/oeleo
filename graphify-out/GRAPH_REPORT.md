# Graph Report - oeleo  (2026-07-16)

## Corpus Check
- 27 files · ~17,435 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 442 nodes · 611 edges · 26 communities (23 shown, 3 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 106 edges (avg confidence: 0.71)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `142e99c7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 23|Community 23]]

## God Nodes (most connected - your core abstractions)
1. `Worker` - 32 edges
2. `LogAndTrayReporter` - 28 edges
3. `WorkerBase` - 25 edges
4. `SSHConnector` - 23 edges
5. `MockWorker` - 20 edges
6. `LocalConnector` - 19 edges
7. `Reporter` - 19 edges
8. `ReporterBase` - 18 edges
9. `Cursor issue workflow (Agent Skills)` - 17 edges
10. `simple_worker()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `chunkify()` --calls--> `Next`  [INFERRED]
  oeleo/workers.py → README.md
- `simple_worker_with_two_matching_and_one_not_matching()` --calls--> `simple_worker()`  [INFERRED]
  tests/conftest.py → oeleo/workers.py
- `check_connection()` --calls--> `LogAndTrayReporter`  [INFERRED]
  check/developers_playground.py → oeleo/reporters.py
- `example_bare_minimum()` --calls--> `simple_worker()`  [INFERRED]
  check/developers_playground.py → oeleo/workers.py
- `example_ssh_worker()` --calls--> `LogAndTrayReporter`  [INFERRED]
  check/developers_playground.py → oeleo/reporters.py

## Communities (26 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (14): DbHandler, FileList, Meta, MockDbHandler, Get or create record of the file and check if it needs to be copied., A simple db bookkeeper using sqlite3 that checks on checksum., _set_up_sqlite_db(), SimpleDbHandler (+6 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (33): check_01(), check_connection(), example_bare_minimum(), example_ssh_worker(), example_ssh_worker_with_simple_scheduler(), example_with_simple_scheduler(), Check that the database is working correctly      1. Connect to the database, Checker (+25 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (14): Exception, Connector, OeleoConnectionError, Raised when a connection cannot be established, Connectors are used to establish a connection to the directory and     provide, # TODO: check if it is best to default to TO DIR or FROM DIR or if it should bre, SharePointConnection, SharePointConnector (+6 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (10): LocalConnector, connected_mover(), Copies files using the method implemented in the connector., simple_mover(), simple_recursive_mover(), test_connected_mover_default_connector(), test_local_connector_calc_checksum(), test_local_connector_filter() (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (28): code:bash (pip install oeleo), code:python (import os), code:.env (OELEO_BASE_DIR_FROM=C:\data\local), code:python (import dotenv), code:python (import logging), code:python (import logging), code:bash (# Sync the project environment (add --all-extras when you ne), Copy files from a Windows PC to a Linux server through ssh (+20 more)

### Community 5 - "Community 5"
Cohesion: 0.1
Nodes (5): create_and_save_icon(), create_icon(), LogAndTrayReporter, Reporter with a system tray icon that also writes to the log., get_log_path()

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (10): check_log_and_tray_reporter(), check_reporter(), main(), NullProgress, progress(), # TODO: implement clearing tray, Minimal reporter that uses console for outputs., A progress tracker that does nothing at all. (+2 more)

### Community 7 - "Community 7"
Cohesion: 0.08
Nodes (23): Branch hygiene, Chat invocation (no slash), code:bash (# Either activate the environment first…), code:bash (# ❌ BAD: bare interpreter), code:bash (# Add or upgrade dependencies), code:bash (oeleo/), Command lifecycle, Designs and guides (+15 more)

### Community 8 - "Community 8"
Cohesion: 0.15
Nodes (8): The worker class is responsible for orchestrating the transfers.      A typica, Add the files that should be processed., Selects the files that should be processed through filtering., Filter for external files that correspond to local ones., Check for differences between the two directories.          Arguments:, Copy the files that needs to be copied and update the db.          Remarks:, Process a single file., Worker

### Community 9 - "Community 9"
Cohesion: 0.1
Nodes (4): LogReporter, Minimal reporter that only writes to the log., Reporter base class.      Reporters are used in the workers for communicating, ReporterBase

### Community 10 - "Community 10"
Cohesion: 0.11
Nodes (18): 0. `/iflow` — smart dispatcher (quick start), 0a. `/iflow-pick` — choose the next issue (front door), 10. `/iflow-status` — status overview of all issues (read-only), 11. `/iflow-archive` — condense the solved-issues archive (destructive, gated), 1. `/iflow-init` — capture the issue locally, 2. `/iflow-plan` — design the approach, 3. `/iflow-start` — implement the plan, 4. `/iflow-pause` — park work safely (+10 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (16): code:bash (uv run pytest), code:bash (# Tail container logs), code:bash (./start-ssh-container.sh), code:bash (docker run -d --name oeleo-ssh -p 2222:2222 \), code:bash (docker compose up -d), code:powershell ($env:OELEO_SSH_TESTS="1"), code:bash (export OELEO_SSH_TESTS=1), code:bash (source ../set-ssh-env.sh) (+8 more)

### Community 12 - "Community 12"
Cohesion: 0.17
Nodes (6): additional_filtering(), base_filter(), base_filter_old(), main(), Simple directory content filter - cannot be used for ssh, Simple directory content filter - cannot be used for ssh

### Community 13 - "Community 13"
Cohesion: 0.15
Nodes (12): Build app with pyinstaller, Checking installation, code:bash (uv sync --all-extras), code:bash (uv add --dev auto-py-to-exe), code:bash (uv run auto-py-to-exe), code:bash (pyinstaller --noconfirm --onefile --windowed --icon "<full p), code:bash (pyinstaller --noconfirm --onefile --windowed --icon "C:\scri), code:r (OELEO_BASE_DIR_FROM=C:\scripting\oeleo\check\from) (+4 more)

### Community 14 - "Community 14"
Cohesion: 0.18
Nodes (11): check_db_dumper(), dump_bookkeeper(), dump_db(), dump_worker_db_table(), Dump the contents of the database, # TODO: option to dump as csv-table, # TODO: option to dump as json, # TODO: option to dump to log (+3 more)

### Community 15 - "Community 15"
Cohesion: 0.22
Nodes (3): local_tmp_path(), create tmp dir with two .xyz files and one .txt file, simple_worker_with_two_matching_and_one_not_matching()

### Community 16 - "Community 16"
Cohesion: 0.29
Nodes (6): code:bash (uv add --dev auto-py-to-exe), code:bash (uv run auto-py-to-exe), code:bash (pyinstaller --noconfirm --onefile --windowed --icon "C:/scri), Create a win desktop app for Oeleo, Installing using pyinstaller, run the tool (dont use py3.10.0 - it has a bug)

### Community 17 - "Community 17"
Cohesion: 0.33
Nodes (5): code:pip (2. download wheels (most likely you need win32 wheels)), code:block2 (3. get the folder with all the wheels to the offline PC), code:block3, Download to PC without internet access, Some notes

### Community 18 - "Community 18"
Cohesion: 0.4
Nodes (3): # TODO: put all deps inside one folder ("dependencies"), # TODO: fix so that also py3.8, py3.10 and py3.11 is packed, # TODO: fix so that packages for win32 py3.8 and win_amd64 py3.10 and py3.11 are

## Knowledge Gaps
- **116 isolated node(s):** `# TODO: put all deps inside one folder ("dependencies")`, `# TODO: fix so that also py3.8, py3.10 and py3.11 is packed`, `# TODO: fix so that packages for win32 py3.8 and win_amd64 py3.10 and py3.11 are`, `Check that the database is working correctly      1. Connect to the database`, `Calculates checksum using method provided by the connector` (+111 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Worker` connect `Community 8` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 6`, `Community 9`?**
  _High betweenness centrality (0.146) - this node is a cross-community bridge._
- **Why does `LocalConnector` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 8`, `Community 12`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Why does `WorkerBase` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 6`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Worker` (e.g. with `ChecksumChecker` and `Connector`) actually correct?**
  _`Worker` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `LogAndTrayReporter` (e.g. with `check_connection()` and `example_ssh_worker()`) actually correct?**
  _`LogAndTrayReporter` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `WorkerBase` (e.g. with `ScheduleAborted` and `SchedulerBase`) actually correct?**
  _`WorkerBase` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SSHConnector` (e.g. with `WorkerBase` and `MockWorker`) actually correct?**
  _`SSHConnector` has 8 INFERRED edges - model-reasoned connections that need verification._