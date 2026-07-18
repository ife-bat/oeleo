# Graph Report - oeleo  (2026-07-18)

## Corpus Check
- 40 files · ~38,461 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 945 nodes · 2108 edges · 63 communities (50 shown, 13 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 180 edges (avg confidence: 0.74)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `163f09ad`
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
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]

## God Nodes (most connected - your core abstractions)
1. `e()` - 58 edges
2. `D()` - 57 edges
3. `K()` - 43 edges
4. `j()` - 42 edges
5. `y()` - 40 edges
6. `Worker` - 37 edges
7. `r()` - 34 edges
8. `SSHConnector` - 32 edges
9. `LogAndTrayReporter` - 28 edges
10. `u()` - 28 edges

## Surprising Connections (you probably didn't know these)
- `chunkify()` --calls--> `Next`  [INFERRED]
  oeleo/workers.py → README.md
- `simple_worker_with_two_matching_and_one_not_matching()` --calls--> `simple_worker()`  [INFERRED]
  tests/conftest.py → oeleo/workers.py
- `test_filter_local_materializes_generator()` --calls--> `simple_worker()`  [INFERRED]
  tests/test_filter_local_materialize.py → oeleo/workers.py
- `check_connection()` --calls--> `ssh_worker()`  [INFERRED]
  check/developers_playground.py → oeleo/workers.py
- `check_connection()` --calls--> `LogAndTrayReporter`  [INFERRED]
  check/developers_playground.py → oeleo/reporters.py

## Communities (63 total, 13 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.15
Nodes (6): FileList, Meta, Get or create record of the file and check if it needs to be copied., A simple db bookkeeper using sqlite3 that checks on checksum., _set_up_sqlite_db(), SimpleDbHandler

### Community 1 - "Community 1"
Cohesion: 0.23
Nodes (13): example_bare_minimum(), example_check_first_then_run(), example_check_with_ssh_connection(), example_with_simple_scheduler(), example_with_ssh_and_env(), example_with_tray_reporter(), load_default_environment(), Load the default environment variables. (+5 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (30): Connector, Quote a path/token for remote shell interpolation (SEC-01).          POSIX rem, Connectors are used to establish a connection to the directory and     provide, Connectors are used to establish a connection to the directory and     provide, # TODO: check if it is best to default to TO DIR or FROM DIR or if it should bre, Raise OeleoConnectionError if the destination is unreachable., # TODO: check if it is best to default to TO DIR or FROM DIR or if it should bre, SharePointConnection (+22 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (27): Exception, LocalConnector, OeleoConnectionError, Raised when a connection cannot be established, Raised when a connection cannot be established, connected_mover(), Copies files using the method implemented in the connector., simple_mover() (+19 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (30): code:bash (pip install oeleo), code:python (import os), code:.env (OELEO_BASE_DIR_FROM=C:\data\local), code:python (import dotenv), code:python (import logging), code:python (import logging), code:bash (# Sync the project environment (add --all-extras when you ne), Copy files from a Windows PC to a Linux server through ssh (+22 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (4): create_and_save_icon(), create_icon(), LogAndTrayReporter, Reporter with a system tray icon that also writes to the log.

### Community 6 - "Community 6"
Cohesion: 0.17
Nodes (7): check_reporter(), main(), NullProgress, progress(), # TODO: implement clearing tray, A progress tracker that does nothing at all., report()

### Community 7 - "Community 7"
Cohesion: 0.08
Nodes (23): Branch hygiene, Chat invocation (no slash), code:bash (# Either activate the environment first…), code:bash (# ❌ BAD: bare interpreter), code:bash (# Add or upgrade dependencies), code:bash (oeleo/), Command lifecycle, Designs and guides (+15 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (14): The worker class is responsible for orchestrating the transfers.      A typica, The worker class is responsible for orchestrating the transfers.      A typica, Selects the files that should be processed through filtering., Selects the files that should be processed through filtering., Filter for external files that correspond to local ones., Filter for external files that correspond to local ones., Check for differences between the two directories.          Arguments:, Check for differences between the two directories.          Arguments: (+6 more)

### Community 10 - "Community 10"
Cohesion: 0.11
Nodes (18): 0. `/iflow` — smart dispatcher (quick start), 0a. `/iflow-pick` — choose the next issue (front door), 10. `/iflow-status` — status overview of all issues (read-only), 11. `/iflow-archive` — condense the solved-issues archive (destructive, gated), 1. `/iflow-init` — capture the issue locally, 2. `/iflow-plan` — design the approach, 3. `/iflow-start` — implement the plan, 4. `/iflow-pause` — park work safely (+10 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (16): code:bash (uv run pytest), code:bash (# Tail container logs), code:bash (./start-ssh-container.sh), code:bash (docker run -d --name oeleo-ssh -p 2222:2222 \), code:bash (docker compose up -d), code:powershell ($env:OELEO_SSH_TESTS="1"), code:bash (export OELEO_SSH_TESTS=1), code:bash (source ../set-ssh-env.sh) (+8 more)

### Community 12 - "Community 12"
Cohesion: 0.18
Nodes (7): additional_filtering(), base_filter(), base_filter_old(), filter_on_callable(), main(), Simple directory content filter - cannot be used for ssh, Simple directory content filter - cannot be used for ssh

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

### Community 26 - "Community 26"
Cohesion: 0.06
Nodes (69): f(), ku(), ln(), Ma(), _n(), onHighlight(), onText(), rp() (+61 more)

### Community 27 - "Community 27"
Cohesion: 0.11
Nodes (47): $(), an(), bs(), cc(), cp(), D(), dc(), ec() (+39 more)

### Community 28 - "Community 28"
Cohesion: 0.09
Nodes (42): ac(), bc(), bi(), bp(), C(), ce(), cn(), cr() (+34 more)

### Community 29 - "Community 29"
Cohesion: 0.11
Nodes (37): ae(), Da(), dn(), e(), er(), Fe(), Ft(), Jn() (+29 more)

### Community 30 - "Community 30"
Cohesion: 0.09
Nodes (35): al(), di(), fi(), Ge(), Go(), gs(), he(), hi() (+27 more)

### Community 31 - "Community 31"
Cohesion: 0.07
Nodes (5): constructor(), Iu(), uu(), vs(), wl()

### Community 32 - "Community 32"
Cohesion: 0.1
Nodes (32): ap(), At(), Au(), bu(), Ca(), cu(), Eu(), Fa() (+24 more)

### Community 33 - "Community 33"
Cohesion: 0.11
Nodes (27): Ai(), b(), Br(), ds(), eo(), fn(), gl(), hu() (+19 more)

### Community 34 - "Community 34"
Cohesion: 0.14
Nodes (20): Bo(), cs(), dl(), Ea(), en(), Fl(), gi(), gn() (+12 more)

### Community 35 - "Community 35"
Cohesion: 0.16
Nodes (11): check_01(), check_connection(), example_bare_minimum(), example_ssh_worker(), example_with_simple_scheduler(), Check that the database is working correctly      1. Connect to the database, Create a Worker for copying files locally.      Args:         base_directory_, Create a Worker for copying files locally.      Args:         base_directory_ (+3 more)

### Community 36 - "Community 36"
Cohesion: 0.15
Nodes (3): SchedulerBase, WorkerBase, Protocol

### Community 38 - "Community 38"
Cohesion: 0.24
Nodes (9): Helper function to export the password as an environmental variable, Helper function to export the password as an environmental variable, register_password(), example_with_ssh_connection_and_scheduler(), simple_multi_dir(), Unit tests for BUG-05: register_password sets provided password., test_register_password_overwrites_existing(), test_register_password_prompts_when_none() (+1 more)

### Community 39 - "Community 39"
Cohesion: 0.22
Nodes (7): example_with_sharepoint_connector(), Resolve per-file reconnect: explicit kwarg, else OELEO_RECONNECT, else False., Create a Worker with SharePointConnector.      Args:         base_directory_f, Create a Worker with SharePointConnector.      Args:         base_directory_f, resolve_reconnect(), sharepoint_worker(), test_resolve_reconnect_defaults_and_env()

### Community 40 - "Community 40"
Cohesion: 0.22
Nodes (3): check_log_and_tray_reporter(), Minimal reporter that uses console for outputs., Reporter

### Community 42 - "Community 42"
Cohesion: 0.22
Nodes (8): App settings (`app/oa.pyw`), code:.env (OELEO_BASE_DIR_FROM=C:\data\local), Configuration, Core transfer settings, Environment variables reference, Example `.env`, SharePoint connector settings, SSH connector settings

### Community 43 - "Community 43"
Cohesion: 0.22
Nodes (8): code:python (import logging), Documentation, Features (and limitations), Future ideas, Hints, Licence, oeleo, Status

### Community 44 - "Community 44"
Cohesion: 0.22
Nodes (8): code:python (import os), code:python (import dotenv), code:python (import logging), Local folder → local folder, Run flow, Usage, Using an `oeleo` scheduler, Windows PC → Linux server (SSH)

### Community 45 - "Community 45"
Cohesion: 0.22
Nodes (9): a(), ao(), As(), Ci(), es(), fs(), ks(), Or() (+1 more)

### Community 47 - "Community 47"
Cohesion: 0.29
Nodes (3): example_ssh_worker_with_simple_scheduler(), SimpleScheduler, test_worker_with_simple_scheduler()

### Community 48 - "Community 48"
Cohesion: 0.25
Nodes (8): be(), Bt(), ef(), get(), pn(), tf(), Ts(), we()

### Community 49 - "Community 49"
Cohesion: 0.29
Nodes (7): ee(), Fo(), mc(), nf(), of(), rf(), ue()

### Community 50 - "Community 50"
Cohesion: 0.33
Nodes (5): code:bash (# Sync the project environment (add --all-extras when you ne), code:bash (# Install the docs tool), Development, Development lead, Documentation (Zensical)

### Community 51 - "Community 51"
Cohesion: 0.33
Nodes (5): code:bash (pip install oeleo), code:bash (uv sync), Development (clone), End users (PyPI), Install

### Community 54 - "Community 54"
Cohesion: 0.4
Nodes (3): _make_worker(), Unit tests for ARCH-02/03: Worker reporter default_factory and Protocol import., test_workers_do_not_share_default_reporter()

### Community 55 - "Community 55"
Cohesion: 0.5
Nodes (4): de(), lt(), tt(), Yt()

### Community 58 - "Community 58"
Cohesion: 0.67
Nodes (3): Bl(), forEach(), Pa()

### Community 59 - "Community 59"
Cohesion: 0.67
Nodes (3): ei(), Gr(), Yr()

### Community 60 - "Community 60"
Cohesion: 0.67
Nodes (3): Qo(), Wn(), Zo()

## Knowledge Gaps
- **161 isolated node(s):** `# TODO: put all deps inside one folder ("dependencies")`, `# TODO: fix so that also py3.8, py3.10 and py3.11 is packed`, `# TODO: fix so that packages for win32 py3.8 and win_amd64 py3.10 and py3.11 are`, `Check that the database is working correctly      1. Connect to the database`, `Calculates checksum using method provided by the connector` (+156 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LocalConnector` connect `Community 3` to `Community 1`, `Community 2`, `Community 35`, `Community 36`, `Community 39`, `Community 8`, `Community 12`, `Community 46`, `Community 54`?**
  _High betweenness centrality (0.380) - this node is a cross-community bridge._
- **Why does `f()` connect `Community 26` to `Community 32`, `Community 12`, `Community 28`, `Community 30`, `Community 31`?**
  _High betweenness centrality (0.363) - this node is a cross-community bridge._
- **Why does `filter_on_callable()` connect `Community 12` to `Community 26`?**
  _High betweenness centrality (0.362) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `e()` (e.g. with `H()` and `$()`) actually correct?**
  _`e()` has 12 INFERRED edges - model-reasoned connections that need verification._
- **What connects `# TODO: put all deps inside one folder ("dependencies")`, `# TODO: fix so that also py3.8, py3.10 and py3.11 is packed`, `# TODO: fix so that packages for win32 py3.8 and win_amd64 py3.10 and py3.11 are` to the rest of the system?**
  _161 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._