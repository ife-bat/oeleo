"""Tests for REL-04 / #40 — catchable shutdown instead of sys.exit."""

from unittest.mock import MagicMock

import pytest

from oeleo.connectors import OeleoShutdown
from oeleo.schedulers import ScheduleAborted, SimpleScheduler
from oeleo.workers import Worker


def _minimal_worker(tmp_path, should_die=False):
    local = MagicMock()
    local.directory = tmp_path / "from"
    local.directory.mkdir(exist_ok=True)

    external = MagicMock()
    external.directory = tmp_path / "to"
    external.directory.mkdir(exist_ok=True)
    external.move_func.return_value = True

    bookkeeper = MagicMock()
    bookkeeper.is_changed.return_value = True

    checker = MagicMock()
    checker.check.return_value = {"checksum": "abc"}

    reporter = MagicMock()
    reporter.should_die.return_value = should_die

    worker = Worker(
        checker=checker,
        bookkeeper=bookkeeper,
        local_connector=local,
        external_connector=external,
        reporter=reporter,
        reconnect=False,
    )
    return worker, reporter


def test_die_if_necessary_raises_oeleo_shutdown(tmp_path):
    worker, reporter = _minimal_worker(tmp_path, should_die=True)

    with pytest.raises(OeleoShutdown, match="Shutdown requested"):
        worker.die_if_necessary()

    reporter.report.assert_any_call("You told me to die! Dying...")
    reporter.close.assert_called()
    worker.external_connector.close.assert_called()


def test_die_if_necessary_does_not_raise_system_exit(tmp_path):
    worker, _ = _minimal_worker(tmp_path, should_die=True)

    with pytest.raises(OeleoShutdown):
        worker.die_if_necessary()


def test_die_if_necessary_noop_when_not_requested(tmp_path):
    worker, reporter = _minimal_worker(tmp_path, should_die=False)

    worker.die_if_necessary()

    reporter.close.assert_not_called()


def test_schedule_aborted_is_oeleo_shutdown_alias():
    assert ScheduleAborted is OeleoShutdown


def test_scheduler_stops_cleanly_on_sleep_poll_shutdown(tmp_path, monkeypatch):
    worker, reporter = _minimal_worker(tmp_path, should_die=False)
    worker.file_names = []

    # run() polls once (False), then the sleep loop polls once (True).
    reporter.should_die.side_effect = [False, True]
    reporter.consume_force_run.return_value = False

    monkeypatch.setattr("oeleo.schedulers.time.sleep", lambda _: None)

    scheduler = SimpleScheduler(
        worker,
        run_interval_time=0.05,
        max_run_intervals=10,
    )
    scheduler.start()

    assert reporter.close.called
