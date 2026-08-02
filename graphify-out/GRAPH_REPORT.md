# Graph Report - workspace  (2026-08-02)

## Corpus Check
- 131 files · ~65,508 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1159 nodes · 1533 edges · 119 communities (109 shown, 10 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 55 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2d9c6deb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SimpleDbHandler
- main.py
- SSHConnector
- test_oeleo.py
- Development information
- LogAndTrayReporter
- check_reporter
- Plan: Issue #39 — Raise on SSH list/checksum failure (REL-02)
- Worker
- ReporterBase
- Cursor issue workflow (Agent Skills)
- SSH integration tests
- filters.py
- Build app with pyinstaller
- workers.py
- conftest.py
- notes.md
- Some notes
- WorkerBase
- issue-flow — create a normal issue (`/iflow-issue`)
- Plan: Issue #40 — catchable shutdown instead of `sys.exit`
- issue-flow — issue comments triage
- Code review: Dependabot / dependency security
- issue-flow — issue plan (`/iflow-plan`)
- Code review: improvement backlog (issue-flow ready)
- Code review overview (entry point for agents)
- Code review: architecture & maintainability
- Findings
- issue-flow — issue close (`/iflow-close`)
- Instructions
- issue-flow — history update
- Instructions
- issue-flow — review and label issues (`/iflow-review`)
- Plan: Issue #17 — Stop reconnecting SSH before every file by default
- Plan: Issue #18 — Shell-safe remote path handling in SSHConnector
- developers_playground.py
- Protocol
- issue-flow — advanced auto (`/iflow-auto`)
- issue-flow — issue build (`/iflow-build`)
- Issue #39: Raise on SSH list/checksum failure instead of empty/False sentinels
- Reporter
- LogReporter
- oeleo
- Essential tests (pytest)
- gh-ci — wait on GitHub CI with `gh`
- Plan: Issue #8 — Ensure connection
- issue-flow — doctor (`.issueflows/` health) (`/iflow-doctor`)
- Issue #40: Replace sys.exit in die_if_necessary with a catchable exception
- issue-flow — issue cycle (`/iflow-cycle`)
- issue-flow — version bump
- Status: Issue #40
- test_worker_reporter_default.py
- Plan: Issue #13 — Grouped Dependabot config (DEP-03)
- Issue #19 plan
- simple_worker
- Status: Issue #39 — Raise on SSH list/checksum failure (REL-02)
- Plan: Issue #32 — Make OELEO_PASSWORD optional for key-based SSH
- Medium severity
- LICENSE.md
- issue-flow — epic planning (`/iflow-epic`)
- issue-flow — issue yolo (`/iflow-yolo`)
- Plan: Issue #11 — Dependabot / lock refresh (DEP-01)
- Plan: Issue #12 — Dependabot residuals (DEP-02)
- Issue #56 — Plan: Create proper documentation
- Code review: packaging, tooling & ops
- Code review: testing & quality gates
- oeleo
- Be token greedy - as a caveman
- Issue #11: Clear Dependabot alerts: widen black/pytest pins and refresh uv.lock
- issue-flow — archive solved issues (`/iflow-archive`)
- issue-flow — issue cleanup (`/iflow-cleanup`)
- issue-flow — issue pause (`/iflow-pause`)
- issue-flow — iflow smart dispatcher (`/iflow`)
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
- Issue #56: Create proper documentation
- Issue #8: Ensure connection
- start-ssh-container.sh
- oeleo

## God Nodes (most connected - your core abstractions)
1. `Worker` - 46 edges
2. `SSHConnector` - 37 edges
3. `LogAndTrayReporter` - 32 edges
4. `WorkerBase` - 29 edges
5. `LocalConnector` - 25 edges
6. `simple_worker()` - 24 edges
7. `Reporter` - 23 edges
8. `SimpleScheduler` - 23 edges
9. `MockWorker` - 23 edges
10. `SimpleDbHandler` - 22 edges

## Surprising Connections (you probably didn't know these)
- `test_worker_with_simple_scheduler()` --calls--> `SimpleScheduler`  [EXTRACTED]
  tests/test_oeleo.py → oeleo/schedulers.py
- `test_calculate_checksum()` --calls--> `calculate_checksum()`  [EXTRACTED]
  tests/test_oeleo.py → oeleo/utils.py
- `test_logger()` --calls--> `start_logger()`  [EXTRACTED]
  tests/test_oeleo.py → oeleo/utils.py
- `test_resolve_reconnect_defaults_and_env()` --calls--> `resolve_reconnect()`  [EXTRACTED]
  tests/test_oeleo.py → oeleo/workers.py
- `test_simple_worker_reconnect_from_env()` --calls--> `simple_worker()`  [EXTRACTED]
  tests/test_oeleo.py → oeleo/workers.py

## Import Cycles
- None detected.

## Communities (119 total, 10 thin omitted)

### Community 0 - "SimpleDbHandler"
Cohesion: 0.11
Nodes (15): check_db_dumper(), FileList, Meta, deleter, setter, A simple db bookkeeper using sqlite3 that checks on checksum., SimpleDbHandler, dump_bookkeeper() (+7 more)

### Community 1 - "main.py"
Cohesion: 0.23
Nodes (14): example_bare_minimum(), example_check_first_then_run(), example_check_with_ssh_connection(), example_with_sharepoint_connector(), example_with_simple_scheduler(), example_with_ssh_and_env(), example_with_tray_reporter(), load_default_environment() (+6 more)

### Community 2 - "SSHConnector"
Cohesion: 0.05
Nodes (46): OeleoTransferError, Quote a path/token for remote shell interpolation (SEC-01). POSIX remotes use…, Raised when a connected file operation (e.g. checksum) fails., SharePointConnection, SSHConnector, ssh, _connector_with_mock_run(), fixture (+38 more)

### Community 3 - "test_oeleo.py"
Cohesion: 0.05
Nodes (37): LocalConnector, OeleoConnectionError, Raised when a connection cannot be established or remote listing fails., Helper function to export the password as an environmental variable, # TODO: check if it is best to default to TO DIR or FROM DIR or if it should…, register_password(), connected_mover(), mock_mover() (+29 more)

### Community 4 - "Development information"
Cohesion: 0.10
Nodes (20): Branch hygiene, Chat invocation (no slash), CI via GitHub CLI, Command lifecycle, Designs and guides, Development information, Folder hygiene for `.issueflows/01-current-issues`, If the project uses conda (+12 more)

### Community 6 - "check_reporter"
Cohesion: 0.18
Nodes (4): check_reporter(), main(), NullProgress, A progress tracker that does nothing at all.

### Community 7 - "Plan: Issue #39 — Raise on SSH list/checksum failure (REL-02)"
Cohesion: 0.20
Nodes (9): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #39 — Raise on SSH list/checksum failure (REL-02), Prior art, Scope check (+1 more)

### Community 8 - "Worker"
Cohesion: 0.05
Nodes (29): Exception, OeleoShutdown, Raised when the operator requests a clean shutdown (e.g. tray quit)., DbHandler, MockDbHandler, Any, Path, Protocol (+21 more)

### Community 9 - "ReporterBase"
Cohesion: 0.18
Nodes (3): Protocol, Reporter base class. Reporters are used in the workers for communicating to the…, ReporterBase

### Community 10 - "Cursor issue workflow (Agent Skills)"
Cohesion: 0.09
Nodes (22): 0. `/iflow` — smart dispatcher (quick start), 0a. `/iflow-pick` — choose the next issue (front door), 10. `/iflow-issue` — create a normal (non-epic) issue, 11. `/iflow-status` — status overview of all issues (read-only), 12. `/iflow-review` — review open issues and apply labels, 13. `/iflow-epic` — plan a large change as staged issues, 14. `/iflow-cycle` — batch-process a queue of yolo-fit issues, 15. `/iflow-auto` — unattended large-change orchestration (+14 more)

### Community 11 - "SSH integration tests"
Cohesion: 0.29
Nodes (6): How to test oeleo, Notes, Quick start with Docker (recommended), SSH integration tests, Unit tests, Useful Docker commands

### Community 12 - "filters.py"
Cohesion: 0.24
Nodes (15): FilterTuple, additional_filtering(), base_filter(), filter_on_callable(), filter_on_contains(), filter_on_excluded(), filter_on_not_after(), filter_on_not_before() (+7 more)

### Community 13 - "Build app with pyinstaller"
Cohesion: 0.29
Nodes (6): Build app with pyinstaller, Checking installation, Create a win desktop app for Oeleo, Installing using pyinstaller, oeleo app, run the tool (dont use py3.10.0 - it has a bug)

### Community 14 - "workers.py"
Cohesion: 0.24
Nodes (8): # TODO: implement clearing tray, Convert a value to a boolean, to_bool(), Path, Resolve per-file reconnect: explicit kwarg, else OELEO_RECONNECT, else False., Create a Worker with SharePointConnector. Args: base_directory_from: directory…, resolve_reconnect(), sharepoint_worker()

### Community 15 - "conftest.py"
Cohesion: 0.31
Nodes (8): db_tmp_path(), external_tmp_path(), local_file_tmp_path(), local_tmp_path(), local_tmp_path_with_subdirs(), fixture, create tmp dir with two .xyz files and one .txt file, simple_worker_with_two_matching_and_one_not_matching()

### Community 16 - "notes.md"
Cohesion: 0.50
Nodes (3): Create a win desktop app for Oeleo, Installing using pyinstaller, run the tool (dont use py3.10.0 - it has a bug)

### Community 18 - "WorkerBase"
Cohesion: 0.05
Nodes (13): Hash, Connector, Any, Path, Protocol, Connectors are used to establish a connection to the directory and provide the…, Raise OeleoConnectionError if the destination is unreachable., SharePointConnector (+5 more)

### Community 19 - "issue-flow — create a normal issue (`/iflow-issue`)"
Cohesion: 0.22
Nodes (8): Constraints, Input, Instructions, issue-flow — create a normal issue (`/iflow-issue`), MODEL & EXECUTION DIRECTIVE, Phase 1 — draft and create, Phase 2 — optional lifecycle setup, Resolve project root (multi-root workspaces)

### Community 20 - "Plan: Issue #40 — catchable shutdown instead of `sys.exit`"
Cohesion: 0.22
Nodes (8): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #40 — catchable shutdown instead of `sys.exit`, Prior art, Test strategy

### Community 21 - "issue-flow — issue comments triage"
Cohesion: 0.14
Nodes (12): Constraints, Edge cases, Inputs, issue-flow — issue comments triage, MODEL & EXECUTION DIRECTIVE, Output contract, Triage rules, Constraints (+4 more)

### Community 22 - "Code review: Dependabot / dependency security"
Cohesion: 0.14
Nodes (14): Code review: Dependabot / dependency security, Completed tracks, DEP-01 — Security dependency refresh ([#11](https://github.com/ife-bat/oeleo/issues/11)), DEP-02 — Residual / hard cases ([#12](https://github.com/ife-bat/oeleo/issues/12)), DEP-03 — Dependabot config ([#13](https://github.com/ife-bat/oeleo/issues/13)) — **Done**, Exposure notes (for prioritization), Locked versions (post-DEP-01, `main`), `paramiko` SHA-1 in `rsakey` (expected) (+6 more)

### Community 23 - "issue-flow — issue plan (`/iflow-plan`)"
Cohesion: 0.15
Nodes (11): Activation, Boundaries, Grill me — relentless planning interview, How to grill, When to use, Constraints, Instructions, issue-flow — issue plan (`/iflow-plan`) (+3 more)

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
Cohesion: 0.18
Nodes (10): Branch switch tokens (command input), Changelog update tokens (command input), Constraints, Draft PR token (command input), Hands-off token (command input), Instructions, issue-flow — issue close (`/iflow-close`), MODEL & EXECUTION DIRECTIVE (+2 more)

### Community 29 - "Instructions"
Cohesion: 0.20
Nodes (9): Constraints, Input, Instructions, issue-flow — interactive iterative-fix session (`/iflow-fix`), MODEL & EXECUTION DIRECTIVE, Phase 1 — set up the session (once), Phase 2 — the fix loop (repeat), Phase 3 — finish (+1 more)

### Community 30 - "issue-flow — history update"
Cohesion: 0.20
Nodes (9): A. No version bump — append to `[Unreleased]`, B. Version bump happened — promote `[Unreleased]` to a new release section, Constraints, Inputs from `/iflow-close`, issue-flow — history update, MODEL & EXECUTION DIRECTIVE, Operation modes, Preconditions (+1 more)

### Community 31 - "Instructions"
Cohesion: 0.20
Nodes (9): Constraints, Input, Instructions, issue-flow — pick next issue (`/iflow-pick`), MODEL & EXECUTION DIRECTIVE, Phase 1 — choose the issue, Phase 2 — create the branch, Phase 3 — hand off (+1 more)

### Community 32 - "issue-flow — review and label issues (`/iflow-review`)"
Cohesion: 0.25
Nodes (7): Constraints, Input, Instructions, issue-flow — review and label issues (`/iflow-review`), MODEL & EXECUTION DIRECTIVE, Resolve project root (multi-root workspaces), Review kinds (extendable)

### Community 33 - "Plan: Issue #17 — Stop reconnecting SSH before every file by default"
Cohesion: 0.20
Nodes (9): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #17 — Stop reconnecting SSH before every file by default, Prior art, Scope check (+1 more)

### Community 34 - "Plan: Issue #18 — Shell-safe remote path handling in SSHConnector"
Cohesion: 0.20
Nodes (9): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #18 — Shell-safe remote path handling in SSHConnector, Prior art, Scope check (+1 more)

### Community 35 - "developers_playground.py"
Cohesion: 0.16
Nodes (10): check_connection(), create_and_save_icon(), example_ssh_worker(), example_ssh_worker_with_simple_scheduler(), example_with_ssh_connection_and_scheduler(), create_icon(), SimpleScheduler, Create a Worker with SSHConnector. Args: base_directory_from: directory to copy… (+2 more)

### Community 37 - "issue-flow — advanced auto (`/iflow-auto`)"
Cohesion: 0.29
Nodes (6): Constraints, Input, Instructions, issue-flow — advanced auto (`/iflow-auto`), MODEL & EXECUTION DIRECTIVE, Resolve project root (multi-root workspaces)

### Community 38 - "issue-flow — issue build (`/iflow-build`)"
Cohesion: 0.29
Nodes (6): Constraints, Early PR tokens (command input), Instructions, issue-flow — issue build (`/iflow-build`), MODEL & EXECUTION DIRECTIVE, Resolve project root (multi-root workspaces)

### Community 39 - "Issue #39: Raise on SSH list/checksum failure instead of empty/False sentinels"
Cohesion: 0.29
Nodes (6): Acceptance, Fix direction, Issue #39: Raise on SSH list/checksum failure instead of empty/False sentinels, Original issue text, Related, Summary

### Community 40 - "Reporter"
Cohesion: 0.22
Nodes (4): check_log_and_tray_reporter(), Minimal reporter that uses console for outputs., Report status to the user., Reporter

### Community 42 - "oeleo"
Cohesion: 0.06
Nodes (32): App settings (`app/oa.pyw`), Configuration, Core transfer settings, Environment variables reference, Example `.env`, SharePoint connector settings, SSH connector settings, Database (+24 more)

### Community 43 - "Essential tests (pytest)"
Cohesion: 0.29
Nodes (5): CI recipe (copy-paste), Contract, Essential tests (pytest), Non-goals (v1), Test registry

### Community 44 - "gh-ci — wait on GitHub CI with `gh`"
Cohesion: 0.33
Nodes (5): Fallback (workflow runs), gh-ci — wait on GitHub CI with `gh`, Primary (PR-attached checks), Semantics, Where this fits

### Community 45 - "Plan: Issue #8 — Ensure connection"
Cohesion: 0.20
Nodes (9): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #8 — Ensure connection, Prior art, Scope check (+1 more)

### Community 46 - "issue-flow — doctor (`.issueflows/` health) (`/iflow-doctor`)"
Cohesion: 0.33
Nodes (5): Constraints, Instructions, issue-flow — doctor (`.issueflows/` health) (`/iflow-doctor`), MODEL & EXECUTION DIRECTIVE, Resolve project root (multi-root workspaces)

### Community 47 - "Issue #40: Replace sys.exit in die_if_necessary with a catchable exception"
Cohesion: 0.33
Nodes (5): Acceptance, Fix direction, Issue #40: Replace sys.exit in die_if_necessary with a catchable exception, Original issue text, Summary

### Community 48 - "issue-flow — issue cycle (`/iflow-cycle`)"
Cohesion: 0.20
Nodes (9): All yolo issues + merge conflicts, Constraints, Input — queue spec, Instructions, issue-flow — issue cycle (`/iflow-cycle`), MODEL & EXECUTION DIRECTIVE, Parallel dispatch (experimental, opt-in), Resolve project root (multi-root workspaces) (+1 more)

### Community 49 - "issue-flow — version bump"
Cohesion: 0.22
Nodes (8): Bump levels (both strategies), Choosing the level, Constraints, issue-flow — version bump, MODEL & EXECUTION DIRECTIVE, Resolve the release strategy first, Strategy: git-tag derived, Strategy: static version (uv)

### Community 51 - "Status: Issue #40"
Cohesion: 0.50
Nodes (3): Remaining work, Status: Issue #40, What's done

### Community 52 - "test_worker_reporter_default.py"
Cohesion: 0.17
Nodes (9): Checker, ChecksumChecker, Any, Path, Calculates checksum using method provided by the connector, calculate_checksum(), _make_worker(), Unit tests for ARCH-02/03: Worker reporter default_factory and Protocol import. (+1 more)

### Community 54 - "Plan: Issue #13 — Grouped Dependabot config (DEP-03)"
Cohesion: 0.22
Nodes (8): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #13 — Grouped Dependabot config (DEP-03), Prior art, Test strategy

### Community 55 - "Issue #19 plan"
Cohesion: 0.22
Nodes (8): Approach, Constraints, Files to touch, Goal, Issue #19 plan, Open questions, Prior art, Test strategy

### Community 56 - "simple_worker"
Cohesion: 0.22
Nodes (8): check_01(), example_bare_minimum(), example_with_simple_scheduler(), Check that the database is working correctly 1. Connect to the database 2. Dump…, Create a Worker for copying files locally. Args: base_directory_from: directory…, simple_worker(), Unit tests for REL-03: filter_local materializes file_names to a list., test_filter_local_materializes_generator()

### Community 57 - "Status: Issue #39 — Raise on SSH list/checksum failure (REL-02)"
Cohesion: 0.50
Nodes (3): Remaining work, Status: Issue #39 — Raise on SSH list/checksum failure (REL-02), What's done

### Community 58 - "Plan: Issue #32 — Make OELEO_PASSWORD optional for key-based SSH"
Cohesion: 0.22
Nodes (8): Approach, Constraints, Files to touch, Goal, Open questions, Plan: Issue #32 — Make OELEO_PASSWORD optional for key-based SSH, Prior art, Test strategy

### Community 59 - "Medium severity"
Cohesion: 0.12
Nodes (15): BUG-01 — Locked files (`code=2`) still copy on `run`, BUG-02 — Bookkeeping uses basename only (subdir collisions), BUG-03 — `app/oa.pyw` references missing `worker.db_path`, BUG-04 — Peewee default timestamp frozen at import, BUG-05 — `register_password(pwd)` ignores `pwd` — fixed (#33), BUG-06 — `SharePointConnection.reconnect` broken — fixed (#34), Code review: correctness & reliability, High severity (+7 more)

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
Cohesion: 0.29
Nodes (7): Code review: testing & quality gates, Current state, Flake / design risks in tests, Gaps (TEST-01), Quality tooling gaps (QUAL-01), Recommended test plan for agents, What is well tested

### Community 69 - "oeleo"
Cohesion: 0.25
Nodes (8): Conventions, Entry points, How to run / test, Non-goals / known limitations, oeleo, Release & version bump, Stack / runtime, What this project is

### Community 71 - "Be token greedy - as a caveman"
Cohesion: 0.29
Nodes (6): Auto-Clarity, Be token greedy - as a caveman, Boundaries, Intensity, Persistence, Rules

### Community 73 - "Issue #11: Clear Dependabot alerts: widen black/pytest pins and refresh uv.lock"
Cohesion: 0.29
Nodes (6): Acceptance, Issue #11: Clear Dependabot alerts: widen black/pytest pins and refresh uv.lock, Original issue text, Related, Summary, Work

### Community 75 - "issue-flow — archive solved issues (`/iflow-archive`)"
Cohesion: 0.33
Nodes (5): Constraints, Input, Instructions, issue-flow — archive solved issues (`/iflow-archive`), MODEL & EXECUTION DIRECTIVE

### Community 76 - "issue-flow — issue cleanup (`/iflow-cleanup`)"
Cohesion: 0.29
Nodes (6): Constraints, Input, Instructions, issue-flow — issue cleanup (`/iflow-cleanup`), MODEL & EXECUTION DIRECTIVE, Resolve project root (multi-root workspaces)

### Community 77 - "issue-flow — issue pause (`/iflow-pause`)"
Cohesion: 0.33
Nodes (5): Constraints, Instructions, issue-flow — issue pause (`/iflow-pause`), MODEL & EXECUTION DIRECTIVE, Resolve project root (multi-root workspaces)

### Community 78 - "issue-flow — iflow smart dispatcher (`/iflow`)"
Cohesion: 0.33
Nodes (5): Constraints, Instructions, issue-flow — iflow smart dispatcher (`/iflow`), MODEL & EXECUTION DIRECTIVE, Resolve project root (multi-root workspaces)

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
Cohesion: 0.33
Nodes (5): pack(), # TODO: put all deps inside one folder ("dependencies"), # TODO: fix so that also py3.8, py3.10 and py3.11 is packed, # TODO: fix so that packages for win32 py3.8 and win_amd64 py3.10 and py3.11…, session

### Community 104 - "`00-tools/` — shared helper tools"
Cohesion: 0.50
Nodes (3): `00-tools/` — shared helper tools, Tool index, When working an issue

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
- **478 isolated node(s):** `Meta`, `oeleo`, `set-ssh-env.sh script`, `OELEO_SSH_TESTS`, `OELEO_USERNAME` (+473 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Worker` connect `Worker` to `SimpleDbHandler`, `SSHConnector`, `developers_playground.py`, `test_oeleo.py`, `Reporter`, `ReporterBase`, `workers.py`, `WorkerBase`, `test_worker_reporter_default.py`, `simple_worker`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `SSHConnector` connect `SSHConnector` to `developers_playground.py`, `test_oeleo.py`, `Worker`, `workers.py`, `WorkerBase`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `ReporterBase` connect `ReporterBase` to `developers_playground.py`, `LogAndTrayReporter`, `check_reporter`, `datetime`, `Reporter`, `LogReporter`, `Worker`, `workers.py`, `WorkerBase`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `Worker` (e.g. with `ChecksumChecker` and `Connector`) actually correct?**
  _`Worker` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `SSHConnector` (e.g. with `MockWorker` and `Worker`) actually correct?**
  _`SSHConnector` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `WorkerBase` (e.g. with `SchedulerBase` and `SimpleScheduler`) actually correct?**
  _`WorkerBase` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `LocalConnector` (e.g. with `MockWorker` and `Worker`) actually correct?**
  _`LocalConnector` has 3 INFERRED edges - model-reasoned connections that need verification._