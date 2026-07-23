# Graph Report - workspace  (2026-07-23)

## Corpus Check
- 120 files · ~55,174 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1152 nodes · 1527 edges · 126 communities (116 shown, 10 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 149 edges (avg confidence: 0.71)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `04534587`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SimpleDbHandler
- main.py
- SSHConnector
- test_oeleo.py
- oeleo
- LogAndTrayReporter
- reporters.py
- Development information
- Worker
- ReporterBase
- Cursor issue workflow (Agent Skills)
- Quick start with Docker (recommended)
- connectors.py
- Build app with pyinstaller
- utils.py
- conftest.py
- run the tool (dont use py3.10.0 - it has a bug)
- Download to PC without internet access
- Connector
- LICENSE.md
- test_connector_errors.py
- issue-flow — issue comments triage
- Code review: Dependabot / dependency security
- Grill me — relentless planning interview
- Code review: improvement backlog (issue-flow ready)
- Code review overview (entry point for agents)
- Code review: architecture & maintainability
- Findings
- issue-flow — issue close (`/iflow-close`)
- Instructions
- issue-flow — history update
- Instructions
- Plan: Issue #39 — Raise on SSH list/checksum failure (REL-02)
- Plan: Issue #17 — Stop reconnecting SSH before every file by default
- Plan: Issue #18 — Shell-safe remote path handling in SSHConnector
- developers_playground.py
- WorkerBase
- DbHandler
- register_password
- workers.py
- Reporter
- LogReporter
- Environment variables reference
- oeleo
- Usage
- Plan: Issue #8 — Ensure connection
- MockWorker
- SimpleScheduler
- issue-flow — issue cycle (`/iflow-cycle`)
- issue-flow — version bump
- Development
- Install
- test_worker_reporter_default.py
- Plan: Issue #13 — Grouped Dependabot config (DEP-03)
- Issue #19 plan
- simple_worker
- Database
- Plan: Issue #32 — Make OELEO_PASSWORD optional for key-based SSH
- Code review: correctness & reliability
- test_ssh_integration.py
- test_ssh_shell_safety.py
- issue-flow — epic planning (`/iflow-epic`)
- issue-flow — issue yolo (`/iflow-yolo`)
- Plan: Issue #11 — Dependabot / lock refresh (DEP-01)
- Plan: Issue #12 — Dependabot residuals (DEP-02)
- Issue #56 — Plan: Create proper documentation
- Code review: packaging, tooling & ops
- Code review: testing & quality gates
- oeleo
- test_ssh_optional_password.py
- Be token greedy - as a caveman
- Issue #39: Raise on SSH list/checksum failure instead of empty/False sentinels
- Issue #11: Clear Dependabot alerts: widen black/pytest pins and refresh uv.lock
- Medium severity
- issue-flow — archive solved issues (`/iflow-archive`)
- issue-flow — issue cleanup (`/iflow-cleanup`)
- issue-flow — issue pause (`/iflow-pause`)
- issue-flow — iflow smart dispatcher (`/iflow`)
- issue-flow — issue start (`/iflow-start`)
- issue-flow — issue status overview (`/iflow-status`)
- Status: Issue #12
- Issue #17: Stop reconnecting SSH before every file by default
- Issue #18: Shell-safe remote path handling in SSHConnector
- Issue #31: Materialize filter_local results to a list
- Plan: Issue #31 — Materialize filter_local results to a list
- Issue #32: Make OELEO_PASSWORD optional for key-based SSH
- Issue #33: Fix register_password to set provided password
- Plan: Issue #33 — Fix register_password to set provided password
- Issue #34: Remove broken SharePoint reconnect helper and connector __delete__ hooks
- Plan: Issue #34 — Remove broken SharePoint reconnect / `__delete__`
- Issue #35: Fix Worker.reporter default_factory and typing.Protocol import
- Plan: Issue #35 — Reporter default_factory + typing.Protocol
- Issue #36: Delete base_filter_old and unused imports
- Plan: Issue #36 — Delete base_filter_old and unused imports
- set-ssh-env.sh
- issue-flow — graph rebuild (`/iflow-graphify`)
- Status: Issue #11
- Issue #12: Document residual Dependabot cases; remove stale poetry.lock if present
- Issue #13: Add grouped Dependabot config for uv/pip
- Issue #19: Align README with uv and the actual Python version floor
- Documentation toolchain (Zensical + Read the Docs)
- noxfile.py
- datetime
- `00-tools/` — shared helper tools
- Status: Issue #39 — Raise on SSH list/checksum failure (REL-02)
- Status: Issue #13
- Status: Issue #17
- Status: Issue #18
- Issue #19 status
- Status: Issue #31
- Status: Issue #32
- Status: Issue #33
- Status: Issue #34
- Status: Issue #35
- Status: Issue #36
- Issue #56 — Status
- Status: Issue #8
- test_connector_cleanup_hooks.py
- Issue #56: Create proper documentation
- Issue #8: Ensure connection
- start-ssh-container.sh
- oeleo

## God Nodes (most connected - your core abstractions)
1. `Worker` - 44 edges
2. `SSHConnector` - 38 edges
3. `LogAndTrayReporter` - 32 edges
4. `WorkerBase` - 30 edges
5. `OeleoConnectionError` - 27 edges
6. `LocalConnector` - 25 edges
7. `simple_worker()` - 25 edges
8. `ReporterBase` - 23 edges
9. `Reporter` - 23 edges
10. `SimpleDbHandler` - 22 edges

## Surprising Connections (you probably didn't know these)
- `example_bare_minimum()` --calls--> `simple_worker()`  [INFERRED]
  check/developers_playground.py → oeleo/workers.py
- `test_ssh_connector_no_subdirs()` --calls--> `SSHConnector`  [INFERRED]
  tests/test_ssh_integration.py → oeleo/connectors.py
- `test_ssh_connector_with_subdirs()` --calls--> `SSHConnector`  [INFERRED]
  tests/test_ssh_integration.py → oeleo/connectors.py
- `test_key_auth_connect_uses_key_filename_only()` --calls--> `SSHConnector`  [INFERRED]
  tests/test_ssh_optional_password.py → oeleo/connectors.py
- `test_key_auth_init_without_password()` --calls--> `SSHConnector`  [INFERRED]
  tests/test_ssh_optional_password.py → oeleo/connectors.py

## Import Cycles
- None detected.

## Communities (126 total, 10 thin omitted)

### Community 0 - "SimpleDbHandler"
Cohesion: 0.16
Nodes (6): FileList, Meta, Get or create record of the file and check if it needs to be copied., A simple db bookkeeper using sqlite3 that checks on checksum., _set_up_sqlite_db(), SimpleDbHandler

### Community 1 - "main.py"
Cohesion: 0.27
Nodes (12): example_bare_minimum(), example_check_first_then_run(), example_check_with_ssh_connection(), example_with_sharepoint_connector(), example_with_simple_scheduler(), example_with_ssh_and_env(), example_with_tray_reporter(), load_default_environment() (+4 more)

### Community 2 - "SSHConnector"
Cohesion: 0.14
Nodes (5): Any, Quote a path/token for remote shell interpolation (SEC-01).          POSIX rem, Quote a path/token for remote shell interpolation (SEC-01).          POSIX remot, SharePointConnection, SSHConnector

### Community 3 - "test_oeleo.py"
Cohesion: 0.07
Nodes (27): LocalConnector, connected_mover(), mock_mover(), Path, Copies files using the method implemented in the connector., simple_mover(), simple_recursive_mover(), Resolve per-file reconnect: explicit kwarg, else OELEO_RECONNECT, else False. (+19 more)

### Community 4 - "oeleo"
Cohesion: 0.09
Nodes (26): code:bash (pip install oeleo), code:python (import os), code:.env (OELEO_BASE_DIR_FROM=C:\data\local), code:python (import dotenv), code:python (import logging), code:bash (# Sync the project environment (add --all-extras when you ne), Copy files from a Windows PC to a Linux server through ssh, Database (+18 more)

### Community 5 - "LogAndTrayReporter"
Cohesion: 0.10
Nodes (3): LogAndTrayReporter, Reporter with a system tray icon that also writes to the log., get_log_path()

### Community 6 - "reporters.py"
Cohesion: 0.15
Nodes (7): check_reporter(), main(), NullProgress, progress(), # TODO: implement clearing tray, A progress tracker that does nothing at all., report()

### Community 7 - "Development information"
Cohesion: 0.08
Nodes (23): Branch hygiene, Chat invocation (no slash), code:bash (# Either activate the environment first…), code:bash (# ❌ BAD: bare interpreter), code:bash (# Add or upgrade dependencies), code:bash (oeleo/), Command lifecycle, Designs and guides (+15 more)

### Community 8 - "Worker"
Cohesion: 0.07
Nodes (24): chunkify(), Path, The worker class is responsible for orchestrating the transfers.      A typica, The worker class is responsible for orchestrating the transfers.      A typical, Add the files that should be processed., Add the files that should be processed., Selects the files that should be processed through filtering., Selects the files that should be processed through filtering. (+16 more)

### Community 9 - "ReporterBase"
Cohesion: 0.18
Nodes (3): Protocol, Reporter base class.      Reporters are used in the workers for communicating to, ReporterBase

### Community 10 - "Cursor issue workflow (Agent Skills)"
Cohesion: 0.11
Nodes (18): 0. `/iflow` — smart dispatcher (quick start), 0a. `/iflow-pick` — choose the next issue (front door), 10. `/iflow-status` — status overview of all issues (read-only), 11. `/iflow-archive` — condense the solved-issues archive (destructive, gated), 1. `/iflow-init` — capture the issue locally, 2. `/iflow-plan` — design the approach, 3. `/iflow-start` — implement the plan, 4. `/iflow-pause` — park work safely (+10 more)

### Community 11 - "Quick start with Docker (recommended)"
Cohesion: 0.12
Nodes (16): code:bash (uv run pytest), code:bash (# Tail container logs), code:bash (./start-ssh-container.sh), code:bash (docker run -d --name oeleo-ssh -p 2222:2222 \), code:bash (docker compose up -d), code:powershell ($env:OELEO_SSH_TESTS="1"), code:bash (export OELEO_SSH_TESTS=1), code:bash (source ../set-ssh-env.sh) (+8 more)

### Community 12 - "connectors.py"
Cohesion: 0.21
Nodes (17): FilterTuple, # TODO: check if it is best to default to TO DIR or FROM DIR or if it should bre, additional_filtering(), base_filter(), base_filter_old(), filter_on_callable(), filter_on_contains(), filter_on_excluded() (+9 more)

### Community 13 - "Build app with pyinstaller"
Cohesion: 0.15
Nodes (12): Build app with pyinstaller, Checking installation, code:bash (uv sync --all-extras), code:bash (uv add --dev auto-py-to-exe), code:bash (uv run auto-py-to-exe), code:bash (pyinstaller --noconfirm --onefile --windowed --icon "<full p), code:bash (pyinstaller --noconfirm --onefile --windowed --icon "C:\scri), code:r (OELEO_BASE_DIR_FROM=C:\scripting\oeleo\check\from) (+4 more)

### Community 14 - "utils.py"
Cohesion: 0.20
Nodes (11): check_db_dumper(), dump_bookkeeper(), dump_db(), dump_worker_db_table(), Dump the contents of the database, # TODO: option to dump as csv-table, # TODO: option to dump as json, # TODO: option to dump to log (+3 more)

### Community 15 - "conftest.py"
Cohesion: 0.22
Nodes (3): local_tmp_path(), create tmp dir with two .xyz files and one .txt file, simple_worker_with_two_matching_and_one_not_matching()

### Community 16 - "run the tool (dont use py3.10.0 - it has a bug)"
Cohesion: 0.29
Nodes (6): code:bash (uv add --dev auto-py-to-exe), code:bash (uv run auto-py-to-exe), code:bash (pyinstaller --noconfirm --onefile --windowed --icon "C:/scri), Create a win desktop app for Oeleo, Installing using pyinstaller, run the tool (dont use py3.10.0 - it has a bug)

### Community 17 - "Download to PC without internet access"
Cohesion: 0.33
Nodes (5): code:pip (2. download wheels (most likely you need win32 wheels)), code:block2 (3. get the folder with all the wheels to the offline PC), code:block3, Download to PC without internet access, Some notes

### Community 18 - "Connector"
Cohesion: 0.11
Nodes (8): Hash, Connector, Path, Protocol, Connectors are used to establish a connection to the directory and     provide, Connectors are used to establish a connection to the directory and     provide t, Raise OeleoConnectionError if the destination is unreachable., SharePointConnector

### Community 20 - "test_connector_errors.py"
Cohesion: 0.25
Nodes (14): OeleoTransferError, _connector_with_mock_run(), Unit tests for REL-02: connector list/checksum failures raise typed errors., test_calculate_checksum_raises_on_empty_stdout(), test_calculate_checksum_raises_on_fabric_exception(), test_calculate_checksum_raises_when_result_not_ok(), test_check_aborts_and_notifies_when_external_list_fails(), test_check_continues_after_external_checksum_transfer_error() (+6 more)

### Community 21 - "issue-flow — issue comments triage"
Cohesion: 0.14
Nodes (12): Constraints, Edge cases, Inputs, issue-flow — issue comments triage, MODEL & EXECUTION DIRECTIVE, Output contract, Triage rules, Constraints (+4 more)

### Community 22 - "Code review: Dependabot / dependency security"
Cohesion: 0.14
Nodes (14): Code review: Dependabot / dependency security, Completed tracks, DEP-01 — Security dependency refresh ([#11](https://github.com/ife-bat/oeleo/issues/11)), DEP-02 — Residual / hard cases ([#12](https://github.com/ife-bat/oeleo/issues/12)), DEP-03 — Dependabot config ([#13](https://github.com/ife-bat/oeleo/issues/13)) — **Done**, Exposure notes (for prioritization), Locked versions (post-DEP-01, `main`), `paramiko` SHA-1 in `rsakey` (expected) (+6 more)

### Community 23 - "Grill me — relentless planning interview"
Cohesion: 0.17
Nodes (10): Activation, Boundaries, Grill me — relentless planning interview, How to grill, When to use, Constraints, Instructions, issue-flow — issue plan (`/iflow-plan`) (+2 more)

### Community 24 - "Code review: improvement backlog (issue-flow ready)"
Cohesion: 0.17
Nodes (12): Code review: improvement backlog (issue-flow ready), P0 — Correctness (do first / can interleave with DEP-01), P0 — Dependabot / dependency security (parallel track), P1 — Data model & identity, P1 — Security / SSH hardening, P2 — API cleanup, P2 — Errors & observability, P3 — Docs & packaging hygiene (+4 more)

### Community 25 - "Code review overview (entry point for agents)"
Cohesion: 0.17
Nodes (12): Architecture at a glance, Code review overview (entry point for agents), Critical / high (fix or decide soon), Document index, How agents should use this with issue-flow, Low / cleanup, Medium, Out of scope for this review (+4 more)

### Community 26 - "Code review: architecture & maintainability"
Cohesion: 0.18
Nodes (10): API consistency issues, Code review: architecture & maintainability, Coupling & hotspots, Cross-cutting smells, Data flow, Dead / duplicate / inconsistent code (CLEAN-*), God-ish modules, Intended design (good) (+2 more)

### Community 27 - "Findings"
Cohesion: 0.18
Nodes (11): Agent rules when touching this area, Code review: security & trust boundaries, Findings, ~~SEC-01 — Remote command construction (high)~~ (done in #18), SEC-02 — MD5 for change detection (low / informational), SEC-03 — Secrets handling (medium hygiene), SEC-04 — Least privilege & deployment (ops), SEC-05 — SharePoint auth (medium / dependency) (+3 more)

### Community 28 - "issue-flow — issue close (`/iflow-close`)"
Cohesion: 0.20
Nodes (9): Branch switch tokens (command input), Changelog update tokens (command input), Constraints, Hands-off token (command input), Instructions, issue-flow — issue close (`/iflow-close`), MODEL & EXECUTION DIRECTIVE, Optional version bump (command input) (+1 more)

### Community 29 - "Instructions"
Cohesion: 0.20
Nodes (9): Constraints, Input, Instructions, issue-flow — interactive iterative-fix session (`/iflow-fix`), MODEL & EXECUTION DIRECTIVE, Phase 1 — set up the session (once), Phase 2 — the fix loop (repeat), Phase 3 — finish (+1 more)

### Community 30 - "issue-flow — history update"
Cohesion: 0.20
Nodes (9): A. No version bump — append to `[Unreleased]`, B. Version bump happened — promote `[Unreleased]` to a new release section, Constraints, Inputs from `/iflow-close`, issue-flow — history update, MODEL & EXECUTION DIRECTIVE, Operation modes, Preconditions (+1 more)

### Community 31 - "Instructions"
Cohesion: 0.20
Nodes (9): Constraints, Input, Instructions, issue-flow — pick next issue (`/iflow-pick`), MODEL & EXECUTION DIRECTIVE, Phase 1 — choose the issue, Phase 2 — create the branch, Phase 3 — hand off (+1 more)

### Community 32 - "Plan: Issue #39 — Raise on SSH list/checksum failure (REL-02)"
Cohesion: 0.20
Nodes (9): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #39 — Raise on SSH list/checksum failure (REL-02), Prior art, Scope check (+1 more)

### Community 33 - "Plan: Issue #17 — Stop reconnecting SSH before every file by default"
Cohesion: 0.20
Nodes (9): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #17 — Stop reconnecting SSH before every file by default, Prior art, Scope check (+1 more)

### Community 34 - "Plan: Issue #18 — Shell-safe remote path handling in SSHConnector"
Cohesion: 0.20
Nodes (9): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #18 — Shell-safe remote path handling in SSHConnector, Prior art, Scope check (+1 more)

### Community 35 - "developers_playground.py"
Cohesion: 0.21
Nodes (9): check_connection(), create_and_save_icon(), example_bare_minimum(), example_ssh_worker(), example_with_ssh_connection_and_scheduler(), create_icon(), Create a Worker with SSHConnector.      Args:         base_directory_from: di, Create a Worker with SSHConnector.      Args:         base_directory_from: direc (+1 more)

### Community 36 - "WorkerBase"
Cohesion: 0.13
Nodes (5): Protocol, SchedulerBase, Protocol, WorkerBase, Protocol

### Community 37 - "DbHandler"
Cohesion: 0.17
Nodes (5): DbHandler, MockDbHandler, Any, Path, Protocol

### Community 38 - "register_password"
Cohesion: 0.36
Nodes (7): Raised when a connected file operation (e.g. checksum) fails., Helper function to export the password as an environmental variable, register_password(), Unit tests for BUG-05: register_password sets provided password., test_register_password_overwrites_existing(), test_register_password_prompts_when_none(), test_register_password_sets_provided_pwd()

### Community 39 - "workers.py"
Cohesion: 0.21
Nodes (8): Exception, OeleoConnectionError, Exception, Raised when a connection cannot be established, Raised when a connection cannot be established or remote listing fails., Exception, Raised when the user aborts the run., ScheduleAborted

### Community 40 - "Reporter"
Cohesion: 0.20
Nodes (5): example_ssh_worker_with_simple_scheduler(), check_log_and_tray_reporter(), Minimal reporter that uses console for outputs., Report status to the user., Reporter

### Community 42 - "Environment variables reference"
Cohesion: 0.22
Nodes (8): App settings (`app/oa.pyw`), code:.env (OELEO_BASE_DIR_FROM=C:\data\local), Configuration, Core transfer settings, Environment variables reference, Example `.env`, SharePoint connector settings, SSH connector settings

### Community 43 - "oeleo"
Cohesion: 0.22
Nodes (8): code:python (import logging), Documentation, Features (and limitations), Future ideas, Hints, Licence, oeleo, Status

### Community 44 - "Usage"
Cohesion: 0.22
Nodes (8): code:python (import os), code:python (import dotenv), code:python (import logging), Local folder → local folder, Run flow, Usage, Using an `oeleo` scheduler, Windows PC → Linux server (SSH)

### Community 45 - "Plan: Issue #8 — Ensure connection"
Cohesion: 0.20
Nodes (9): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #8 — Ensure connection, Prior art, Scope check (+1 more)

### Community 47 - "SimpleScheduler"
Cohesion: 0.29
Nodes (3): SimpleScheduler, test_worker_with_simple_scheduler(), test_worker_with_simple_scheduler_with_subdirs()

### Community 48 - "issue-flow — issue cycle (`/iflow-cycle`)"
Cohesion: 0.22
Nodes (8): Constraints, Input — queue spec, Instructions, issue-flow — issue cycle (`/iflow-cycle`), MODEL & EXECUTION DIRECTIVE, Parallel dispatch (experimental, opt-in), Resolve project root (multi-root workspaces), Resuming

### Community 49 - "issue-flow — version bump"
Cohesion: 0.22
Nodes (8): Bump levels (both strategies), Choosing the level, Constraints, issue-flow — version bump, MODEL & EXECUTION DIRECTIVE, Resolve the release strategy first, Strategy: git-tag derived, Strategy: static version (uv)

### Community 50 - "Development"
Cohesion: 0.33
Nodes (5): code:bash (# Sync the project environment (add --all-extras when you ne), code:bash (# Install the docs tool), Development, Development lead, Documentation (Zensical)

### Community 51 - "Install"
Cohesion: 0.33
Nodes (5): code:bash (pip install oeleo), code:bash (uv sync), Development (clone), End users (PyPI), Install

### Community 52 - "test_worker_reporter_default.py"
Cohesion: 0.14
Nodes (11): Checker, ChecksumChecker, Any, Path, Calculates checksum using method provided by the connector, calculate_checksum(), Path, test_calculate_checksum() (+3 more)

### Community 54 - "Plan: Issue #13 — Grouped Dependabot config (DEP-03)"
Cohesion: 0.22
Nodes (8): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #13 — Grouped Dependabot config (DEP-03), Prior art, Test strategy

### Community 55 - "Issue #19 plan"
Cohesion: 0.22
Nodes (8): Approach, Constraints, Files to touch, Goal, Issue #19 plan, Open questions, Prior art, Test strategy

### Community 56 - "simple_worker"
Cohesion: 0.22
Nodes (8): check_01(), example_with_simple_scheduler(), Check that the database is working correctly      1. Connect to the database, Create a Worker for copying files locally.      Args:         base_directory_, Create a Worker for copying files locally.      Args:         base_directory_fro, simple_worker(), Unit tests for REL-03: filter_local materializes file_names to a list., test_filter_local_materializes_generator()

### Community 58 - "Plan: Issue #32 — Make OELEO_PASSWORD optional for key-based SSH"
Cohesion: 0.22
Nodes (8): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #32 — Make OELEO_PASSWORD optional for key-based SSH, Prior art, Test strategy

### Community 59 - "Code review: correctness & reliability"
Cohesion: 0.22
Nodes (8): BUG-01 — Locked files (`code=2`) still copy on `run`, BUG-02 — Bookkeeping uses basename only (subdir collisions), BUG-03 — `app/oa.pyw` references missing `worker.db_path`, Code review: correctness & reliability, High severity, Lower severity / polish, Recommended test additions (pair with fixes), ~~REL-01 — Reconnect before every file~~ (done in #17)

### Community 60 - "test_ssh_integration.py"
Cohesion: 0.33
Nodes (8): _missing_env_vars(), Run a remote command with each path-like part shell-quoted., _run_quoted(), ssh_remote_dir(), test_ssh_connector_creates_missing_remote_dirs(), test_ssh_connector_handles_spaces_in_remote_path(), test_ssh_connector_no_subdirs(), test_ssh_connector_with_subdirs()

### Community 61 - "test_ssh_shell_safety.py"
Cohesion: 0.33
Nodes (7): _connector_with_mock_run(), Unit tests for SEC-01: SSHConnector remote shell quoting (no live SSH)., test_calculate_checksum_quotes_remote_path(), test_ensure_remote_dir_quotes_path(), test_list_content_quotes_directory_and_glob(), test_list_content_quotes_injection_prone_glob(), test_remote_shell_token_quotes_spaces_and_metacharacters()

### Community 62 - "issue-flow — epic planning (`/iflow-epic`)"
Cohesion: 0.25
Nodes (7): Action: publish, Constraints, Input, Instructions, issue-flow — epic planning (`/iflow-epic`), MODEL & EXECUTION DIRECTIVE, Resolve project root (multi-root workspaces)

### Community 63 - "issue-flow — issue yolo (`/iflow-yolo`)"
Cohesion: 0.25
Nodes (7): Chain, Constraints, issue-flow — issue yolo (`/iflow-yolo`), MODEL & EXECUTION DIRECTIVE, Post-run, Preflight (abort on any failure), Resolve project root (multi-root workspaces)

### Community 64 - "Plan: Issue #11 — Dependabot / lock refresh (DEP-01)"
Cohesion: 0.25
Nodes (8): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #11 — Dependabot / lock refresh (DEP-01), Prior art, Test strategy

### Community 65 - "Plan: Issue #12 — Dependabot residuals (DEP-02)"
Cohesion: 0.25
Nodes (8): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #12 — Dependabot residuals (DEP-02), Prior art, Test strategy

### Community 66 - "Issue #56 — Plan: Create proper documentation"
Cohesion: 0.25
Nodes (8): Approach, Constraints, Files to touch, Goal, Issue #56 — Plan: Create proper documentation, Open questions, Prior art, Test strategy

### Community 67 - "Code review: packaging, tooling & ops"
Cohesion: 0.25
Nodes (8): Code review: packaging, tooling & ops, Dependency health & Dependabot, DOC-01 — Docs/toolchain drift, Legacy packing (TOOL-01), Ops artifacts in repo, Packaging (library), Version & release workflow for issue-flow, Windows app / PyInstaller

### Community 68 - "Code review: testing & quality gates"
Cohesion: 0.25
Nodes (7): Code review: testing & quality gates, Current state, Flake / design risks in tests, Gaps (TEST-01), Quality tooling gaps (QUAL-01), Recommended test plan for agents, What is well tested

### Community 69 - "oeleo"
Cohesion: 0.25
Nodes (8): Conventions, Entry points, How to run / test, Non-goals / known limitations, oeleo, Release & version bump, Stack / runtime, What this project is

### Community 70 - "test_ssh_optional_password.py"
Cohesion: 0.25
Nodes (5): Unit tests for SEC-03: OELEO_PASSWORD optional when use_password=False., test_key_auth_connect_uses_key_filename_only(), test_key_auth_init_without_password(), test_password_auth_connect_uses_session_password(), test_password_auth_init_requires_password()

### Community 71 - "Be token greedy - as a caveman"
Cohesion: 0.29
Nodes (6): Auto-Clarity, Be token greedy - as a caveman, Boundaries, Intensity, Persistence, Rules

### Community 72 - "Issue #39: Raise on SSH list/checksum failure instead of empty/False sentinels"
Cohesion: 0.29
Nodes (6): Acceptance, Fix direction, Issue #39: Raise on SSH list/checksum failure instead of empty/False sentinels, Original issue text, Related, Summary

### Community 73 - "Issue #11: Clear Dependabot alerts: widen black/pytest pins and refresh uv.lock"
Cohesion: 0.29
Nodes (6): Acceptance, Issue #11: Clear Dependabot alerts: widen black/pytest pins and refresh uv.lock, Original issue text, Related, Summary, Work

### Community 74 - "Medium severity"
Cohesion: 0.29
Nodes (7): BUG-04 — Peewee default timestamp frozen at import, BUG-05 — `register_password(pwd)` ignores `pwd` — fixed (#33), BUG-06 — `SharePointConnection.reconnect` broken — fixed (#34), Medium severity, ~~REL-02 — Soft failures become silent skips~~ (list/checksum addressed in #39), REL-03 — Generator consumption / `file_names` lifecycle — fixed (#31), REL-04 — `die_if_necessary` calls `sys.exit(0)`

### Community 75 - "issue-flow — archive solved issues (`/iflow-archive`)"
Cohesion: 0.33
Nodes (5): Constraints, Input, Instructions, issue-flow — archive solved issues (`/iflow-archive`), MODEL & EXECUTION DIRECTIVE

### Community 76 - "issue-flow — issue cleanup (`/iflow-cleanup`)"
Cohesion: 0.33
Nodes (5): Constraints, Instructions, issue-flow — issue cleanup (`/iflow-cleanup`), MODEL & EXECUTION DIRECTIVE, Resolve project root (multi-root workspaces)

### Community 77 - "issue-flow — issue pause (`/iflow-pause`)"
Cohesion: 0.33
Nodes (5): Constraints, Instructions, issue-flow — issue pause (`/iflow-pause`), MODEL & EXECUTION DIRECTIVE, Resolve project root (multi-root workspaces)

### Community 78 - "issue-flow — iflow smart dispatcher (`/iflow`)"
Cohesion: 0.33
Nodes (5): Constraints, Instructions, issue-flow — iflow smart dispatcher (`/iflow`), MODEL & EXECUTION DIRECTIVE, Resolve project root (multi-root workspaces)

### Community 79 - "issue-flow — issue start (`/iflow-start`)"
Cohesion: 0.33
Nodes (5): Constraints, Instructions, issue-flow — issue start (`/iflow-start`), MODEL & EXECUTION DIRECTIVE, Resolve project root (multi-root workspaces)

### Community 80 - "issue-flow — issue status overview (`/iflow-status`)"
Cohesion: 0.33
Nodes (5): Constraints, Instructions, issue-flow — issue status overview (`/iflow-status`), MODEL & EXECUTION DIRECTIVE, Resolve project root (multi-root workspaces)

### Community 81 - "Status: Issue #12"
Cohesion: 0.33
Nodes (5): Notes, Remaining work, Status: Issue #12, Verification notes, What's done

### Community 82 - "Issue #17: Stop reconnecting SSH before every file by default"
Cohesion: 0.33
Nodes (5): Acceptance, Fix direction, Issue #17: Stop reconnecting SSH before every file by default, Original issue text, Summary

### Community 83 - "Issue #18: Shell-safe remote path handling in SSHConnector"
Cohesion: 0.33
Nodes (5): Acceptance, Fix direction, Issue #18: Shell-safe remote path handling in SSHConnector, Original issue text, Summary

### Community 84 - "Issue #31: Materialize filter_local results to a list"
Cohesion: 0.33
Nodes (5): Acceptance, Fix direction, Issue #31: Materialize filter_local results to a list, Original issue text, Summary

### Community 85 - "Plan: Issue #31 — Materialize filter_local results to a list"
Cohesion: 0.33
Nodes (5): Approach, Files to touch, Goal, Plan: Issue #31 — Materialize filter_local results to a list, Test strategy

### Community 86 - "Issue #32: Make OELEO_PASSWORD optional for key-based SSH"
Cohesion: 0.33
Nodes (5): Acceptance, Fix direction, Issue #32: Make OELEO_PASSWORD optional for key-based SSH, Original issue text, Summary

### Community 87 - "Issue #33: Fix register_password to set provided password"
Cohesion: 0.33
Nodes (5): Acceptance, Fix direction, Issue #33: Fix register_password to set provided password, Original issue text, Summary

### Community 88 - "Plan: Issue #33 — Fix register_password to set provided password"
Cohesion: 0.33
Nodes (5): Approach, Files to touch, Goal, Plan: Issue #33 — Fix register_password to set provided password, Test strategy

### Community 89 - "Issue #34: Remove broken SharePoint reconnect helper and connector __delete__ hooks"
Cohesion: 0.33
Nodes (5): Acceptance, Fix direction, Issue #34: Remove broken SharePoint reconnect helper and connector __delete__ hooks, Original issue text, Summary

### Community 90 - "Plan: Issue #34 — Remove broken SharePoint reconnect / `__delete__`"
Cohesion: 0.33
Nodes (5): Approach, Files to touch, Goal, Plan: Issue #34 — Remove broken SharePoint reconnect / `__delete__`, Test strategy

### Community 91 - "Issue #35: Fix Worker.reporter default_factory and typing.Protocol import"
Cohesion: 0.33
Nodes (5): Acceptance, Fix direction, Issue #35: Fix Worker.reporter default_factory and typing.Protocol import, Original issue text, Summary

### Community 92 - "Plan: Issue #35 — Reporter default_factory + typing.Protocol"
Cohesion: 0.33
Nodes (5): Approach, Files to touch, Goal, Plan: Issue #35 — Reporter default_factory + typing.Protocol, Test strategy

### Community 93 - "Issue #36: Delete base_filter_old and unused imports"
Cohesion: 0.33
Nodes (5): Acceptance, Fix direction, Issue #36: Delete base_filter_old and unused imports, Original issue text, Summary

### Community 94 - "Plan: Issue #36 — Delete base_filter_old and unused imports"
Cohesion: 0.33
Nodes (5): Approach, Files to touch, Goal, Plan: Issue #36 — Delete base_filter_old and unused imports, Test strategy

### Community 95 - "set-ssh-env.sh"
Cohesion: 0.33
Nodes (5): OELEO_EXTERNAL_HOST, OELEO_PASSWORD, OELEO_SSH_TESTS, OELEO_USERNAME, set-ssh-env.sh script

### Community 96 - "issue-flow — graph rebuild (`/iflow-graphify`)"
Cohesion: 0.40
Nodes (4): Constraints, Instructions, issue-flow — graph rebuild (`/iflow-graphify`), MODEL & EXECUTION DIRECTIVE

### Community 97 - "Status: Issue #11"
Cohesion: 0.40
Nodes (4): Notes, Remaining work, Status: Issue #11, What's done

### Community 98 - "Issue #12: Document residual Dependabot cases; remove stale poetry.lock if present"
Cohesion: 0.40
Nodes (4): Acceptance, Issue #12: Document residual Dependabot cases; remove stale poetry.lock if present, Original issue text, Summary

### Community 99 - "Issue #13: Add grouped Dependabot config for uv/pip"
Cohesion: 0.40
Nodes (4): Acceptance, Issue #13: Add grouped Dependabot config for uv/pip, Original issue text, Summary

### Community 100 - "Issue #19: Align README with uv and the actual Python version floor"
Cohesion: 0.40
Nodes (4): Acceptance, Issue #19: Align README with uv and the actual Python version floor, Original issue text, Summary

### Community 101 - "Documentation toolchain (Zensical + Read the Docs)"
Cohesion: 0.40
Nodes (4): Alternatives considered, Decision, Documentation toolchain (Zensical + Read the Docs), Ops note

### Community 102 - "noxfile.py"
Cohesion: 0.40
Nodes (3): # TODO: put all deps inside one folder ("dependencies"), # TODO: fix so that also py3.8, py3.10 and py3.11 is packed, # TODO: fix so that packages for win32 py3.8 and win_amd64 py3.10 and py3.11 are

### Community 104 - "`00-tools/` — shared helper tools"
Cohesion: 0.50
Nodes (3): `00-tools/` — shared helper tools, Tool index, When working an issue

### Community 105 - "Status: Issue #39 — Raise on SSH list/checksum failure (REL-02)"
Cohesion: 0.50
Nodes (3): Remaining work, Status: Issue #39 — Raise on SSH list/checksum failure (REL-02), What's done

### Community 106 - "Status: Issue #13"
Cohesion: 0.50
Nodes (3): Remaining work, Status: Issue #13, What's done

### Community 107 - "Status: Issue #17"
Cohesion: 0.50
Nodes (3): Remaining work, Status: Issue #17, What's done

### Community 108 - "Status: Issue #18"
Cohesion: 0.50
Nodes (3): Remaining work, Status: Issue #18, What's done

### Community 109 - "Issue #19 status"
Cohesion: 0.50
Nodes (3): Issue #19 status, Remaining work, What's done

### Community 110 - "Status: Issue #31"
Cohesion: 0.50
Nodes (3): Remaining work, Status: Issue #31, What's done

### Community 111 - "Status: Issue #32"
Cohesion: 0.50
Nodes (3): Remaining work, Status: Issue #32, What's done

### Community 112 - "Status: Issue #33"
Cohesion: 0.50
Nodes (3): Remaining work, Status: Issue #33, What's done

### Community 113 - "Status: Issue #34"
Cohesion: 0.50
Nodes (3): Remaining work, Status: Issue #34, What's done

### Community 114 - "Status: Issue #35"
Cohesion: 0.50
Nodes (3): Remaining work, Status: Issue #35, What's done

### Community 115 - "Status: Issue #36"
Cohesion: 0.50
Nodes (3): Remaining work, Status: Issue #36, What's done

### Community 116 - "Issue #56 — Status"
Cohesion: 0.50
Nodes (3): Issue #56 — Status, Remaining work, What's done

### Community 117 - "Status: Issue #8"
Cohesion: 0.50
Nodes (3): Remaining work, Status: Issue #8, What's done

## Knowledge Gaps
- **450 isolated node(s):** `oeleo`, `set-ssh-env.sh script`, `OELEO_SSH_TESTS`, `OELEO_USERNAME`, `OELEO_EXTERNAL_HOST` (+445 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Worker` connect `Worker` to `SimpleDbHandler`, `SSHConnector`, `developers_playground.py`, `test_oeleo.py`, `DbHandler`, `WorkerBase`, `workers.py`, `Reporter`, `ReporterBase`, `Connector`, `test_worker_reporter_default.py`, `test_connector_errors.py`, `simple_worker`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `LogAndTrayReporter` connect `LogAndTrayReporter` to `main.py`, `developers_playground.py`, `reporters.py`, `datetime`, `Reporter`, `ReporterBase`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `SSHConnector` connect `SSHConnector` to `developers_playground.py`, `WorkerBase`, `test_ssh_optional_password.py`, `workers.py`, `Worker`, `connectors.py`, `MockWorker`, `Connector`, `test_connector_errors.py`, `test_ssh_integration.py`, `test_ssh_shell_safety.py`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `Worker` (e.g. with `ChecksumChecker` and `Connector`) actually correct?**
  _`Worker` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `SSHConnector` (e.g. with `MockWorker` and `ssh_worker()`) actually correct?**
  _`SSHConnector` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `LogAndTrayReporter` (e.g. with `check_connection()` and `example_ssh_worker()`) actually correct?**
  _`LogAndTrayReporter` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `WorkerBase` (e.g. with `ScheduleAborted` and `SchedulerBase`) actually correct?**
  _`WorkerBase` has 15 INFERRED edges - model-reasoned connections that need verification._