import logging
import os
from typing import Protocol
from math import ceil
import warnings

from rich.panel import Panel
from rich.text import Text
from rich.console import Console

from oeleo.layouts import N_COLS_NOT_BODY, N_ROWS_NOT_BODY
from oeleo.utils import start_logger
from oeleo.console import simple_console

# used for same_line reporting in Reporter.report
NOT_LOGGED = ["\n", "\r", "\r\n", "", " ", " .", ".", "-", "o", "v", "!"]
line_length = 0
try:
    max_line_length = os.get_terminal_size().columns
except OSError:
    max_line_length = 80

log = logging.getLogger("oeleo")


class ReporterBase(Protocol):
    """Reporter base class.

    Reporters are used in the workers for communicating to the user. Schedulers can tap
    into the workers reporter and both modify the output or send additional output to the user.
    """

    layout = None
    lines: list = None

    def report(self, status, events=None, same_line=False, replace_line=False):
        ...

    def clear(self):
        ...


class Reporter(ReporterBase):
    """Minimal reporter that uses console for outputs."""

    layout = None
    lines = []

    @staticmethod
    def report(status, same_line=False, **kwargs):
        """Report status to the user."""
        global line_length

        if same_line:
            new_line_length = line_length + len(status)
            if new_line_length > max_line_length:
                simple_console.print()
                line_length = 0

            simple_console.print(status, end="")
            line_length += len(status)
            if status not in NOT_LOGGED:
                log.info(status)
        else:
            simple_console.print(status)
            line_length = 0
            log.info(status)

    def clear(self):
        pass


class LayoutReporter(ReporterBase):
    """A relatively advanced reporter that outputs through a `Rich.layout.Layout`.

    This reporter is used by `oeleo.schedulers.RichScheduler`.
    The reporter sends output as a string within a `Rich.panel.Panel` by issuing the `update` method
    on the layout[sub_pane] instance.

    Update: This reporter together with `oeleo.schedulers.RichScheduler`
        will be removed in the next major release.
    """

    def __init__(
        self,
        layout,
        max_lines=1000,
        min_lines=500,
        sub_pane: str = "body",
        n_rows_not_body: int = N_ROWS_NOT_BODY,
        n_cols_not_body: int = N_COLS_NOT_BODY,
    ):
        """Reporter using a layout.

        This reporter is used by `oeleo.schedulers.RichScheduler`.

        Args:
            layout: the layout the scheduler communicates through.
            max_lines: does not store more lines than this.
            min_lines: amount of lines it keeps when "chopping" off
                the excess lines when passing the `max_lines` threshold.
            sub_pane: the name of the sub-pane in the layout.
            n_rows_not_body: rows occupied by other items of the layout, used for calculating how
                many lines that should be sent to the layout during update.
            n_cols_not_body: columns occupied by other items of the layout, used for calculating
                how many lines that should be sent to the layout during update.
        """
        self.layout = layout
        self.lines = []
        self.max_lines: int = max_lines
        self.min_lines: int = min_lines
        self.sub_pane = sub_pane
        self.n_rows_not_body = n_rows_not_body
        self.n_cols_not_body = n_cols_not_body
        warnings.warn(
            "LayoutReporter together with RichScheduler will be removed in the next major release."
        )

    def report(self, status, events=None, same_line=False, replace_line=False):
        if same_line and len(self.lines):
            self.lines[-1] = f"{self.lines[-1]}{status}"
        elif replace_line and len(self.lines):
            self.lines[-1] = f"{status}"
        else:
            self.lines.append(status)
        if events:
            log.debug(
                f"Events ({events}) given - however, events are not implemented yet."
            )

        self._trim_if_needed()
        body_panel = self._update_body_panel()
        self.layout[self.sub_pane].update(body_panel)
        log.info(status)

    def clear(self):
        self.lines = []

    def _trim_if_needed(self):
        if len(self.lines) > self.max_lines:
            self.lines = self.lines[-self.min_lines :]

    @staticmethod
    def _get_terminal_size():
        try:
            nc, nr = os.get_terminal_size()
        except OSError:
            nc, nr = 300, 300
            log.debug("Could not get terminal size, setting it to 300 x 300")
        return nc, nr

    def _update_body_panel(self):
        number_of_columns, number_of_rows = self._get_terminal_size()
        number_of_rows -= self.n_rows_not_body
        number_of_columns -= self.n_cols_not_body

        _lines = self.lines[-number_of_rows:]
        needed_rows_due_to_wrapping = 0
        _new_lines = []
        for _line in reversed(_lines):
            needed_rows_due_to_wrapping += ceil(
                Text(_line).cell_len / number_of_columns
            )
            if needed_rows_due_to_wrapping < number_of_rows:
                _new_lines.append(_line)
            else:
                break
        _lines = reversed(_new_lines)

        s = "\n".join(_lines)

        p = Panel(s)
        return p
