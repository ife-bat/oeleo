from contextlib import contextmanager
import logging
import os
from typing import Protocol, Any
import time
from math import ceil
import warnings
import sys
from threading import Thread

try:
    from PIL import Image, ImageDraw
    import pystray
except ImportError:
    Image = None
    ImageDraw = None
    pystray = None

from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.progress import TextColumn, SpinnerColumn
from rich.progress import Progress as RichProgress

from oeleo.layouts import N_COLS_NOT_BODY, N_ROWS_NOT_BODY
from oeleo.utils import start_logger
from oeleo.console import simple_console

# used for same_line reporting in Reporter.report
NOT_LOGGED = ["\n", "\r", "\r\n", "", " ", " .", ".", "-", "o", "v", "!"]
line_length = 0

log = logging.getLogger("oeleo")

def create_icon(width, height, color1, color2):
    if Image is None:
        return None

    image = Image.new("RGB", (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.ellipse(
        (
            (width // 6, height // 6),
            (5 * width // 6, 5 * height // 6),
        ),
        fill=color2,
    )
    dc.ellipse(
        (
            (2 * width // 6, 2 * height // 6),
            (4 * width // 6, 4 * height // 6),
        ),
        fill=color1,
    )

    return image


class NullProgress:
    """A progress tracker that does nothing at all."""

    def __init__(self, *args, **kwargs):
        ...

    def __enter__(self):
        ...

    def __exit__(self, *args, **kwargs):
        ...

    def update(self, *args, **kwargs):
        ...

    def close(self, *args, **kwargs):
        ...

    def add_task(self, *args, **kwargs):
        ...

    def remove_task(self, *args, **kwargs):
        ...


class ReporterBase(Protocol):
    """Reporter base class.

    Reporters are used in the workers for communicating to the user. Schedulers can tap
    into the workers reporter and both modify the output or send additional output to the user.
    """

    layout = None
    lines: list = None

    Progress: Any = NullProgress

    def report(self, status, events=None, same_line=False, replace_line=False):
        ...

    def status(self, status: str):
        ...

    def clear(self):
        ...

    def close(self):
        ...

    def should_die(self) -> bool:
        ...

    def notify(self, status: str, title: str = None):
        pass

    @contextmanager
    def progress(self, *args, **kwargs):

        p = self.Progress(*args, **kwargs)
        try:
            yield p
        finally:
            p.__exit__(None, None, None)


class LogReporter(ReporterBase):
    """Minimal reporter that only writes to the log."""

    @staticmethod
    def report(status, *args, **kwargs):
        """Report status."""

        if status not in NOT_LOGGED:
            log.info(status)

    def clear(self):
        pass

    def status(self, status: str):
        pass

    def notify(self, status: str, title: str = None):
        pass

    def close(self):
        pass


class LogAndTrayReporter(ReporterBase):
    """Reporter with a system tray icon that also writes to the log."""

    def __init__(self):
        self.status_message = ""
        self.icon_state = False
        self.icon_image = None
        self.icon_state = False
        self.icon = None
        self.icon_thread = None
        self.icon_update_thread = None
        self.kill_me = False
        self.create_tray_icon("oeleo")

    def _on_action_clicked(self, icon, item):
        # insert code here, e.g.
        log.debug(f"ACTION: {item}-{icon}@{time.ctime()}")
        log.debug(f"STATUS: {self.status_message}@{time.ctime()}")

    def _on_quit_clicked(self, icon, item):
        self.kill_me = True

    def _update_icon(self):
        while True:
            self.icon.icon = (
                self.icon_image.get(self.status_message) or self.icon_image["oeleo"]
            )
            time.sleep(0.1)

    def _make_all_icons(self):
        self.icon_image = {
            "oeleo": create_icon(64, 64, "black", "white"),
            "run": create_icon(64, 64, "black", "red"),
            "check": create_icon(64, 64, "white", "green"),
            "finished": create_icon(64, 64, "black", "white"),
        }

    @staticmethod
    def _left_click_action(icon, item):
        pass

    def create_tray_icon(self, name="oeleo"):
        logging.debug("Creating tray icon")
        if pystray is None:
            self.icon = None
            return
        self._make_all_icons()
        self.icon = pystray.Icon(
            name,
            self.icon_image["oeleo"],
            menu=pystray.Menu(
                pystray.MenuItem(
                    text=name, action=None, default=True
                ),
                pystray.MenuItem(
                    "Action",
                    pystray.Menu(
                        pystray.MenuItem(
                            "[to be implemented]", self._on_action_clicked, checked=None,
                        ),
                    ),
                ),
                pystray.MenuItem(
                    "Quit",
                    pystray.Menu(
                        pystray.MenuItem(
                            "No", None, checked=None, default=True,
                        ),
                        pystray.MenuItem(
                            "Yes - shut down oeleo!", self._on_quit_clicked, checked=None
                        ),

                    ),
                ),
            ),
        )
        self.icon_thread = Thread(target=self.icon.run)
        self.icon_thread.daemon = True
        self.icon_thread.start()
        self.icon_update_thread = Thread(target=self._update_icon)
        self.icon_update_thread.daemon = True
        self.icon_update_thread.start()

    @staticmethod
    def report(status, *args, **kwargs):
        """Report status."""

        if status not in NOT_LOGGED:
            log.info(status)

    def notify(self, status, title=None):
        if self.icon is not None:
            self.icon.notify(status)
            time.sleep(0.1)

    def status(self, status: str):
        if status:
            message = f"{status}"
        else:
            message = "oeleo"
        self.status_message = message

    def clear(self):
        # TODO: implement clearing tray
        pass

    def close(self, silent=False):
        if self.icon is None:
            return
        if not silent:
            self.icon.notify("oeleo finished for now.")
            time.sleep(4)
            self.icon.remove_notification()
        self.icon.stop()

    def should_die(self) -> bool:
        return self.kill_me


class Reporter(ReporterBase):
    """Minimal reporter that uses console for outputs."""
    max_line_length = 80

    layout = None
    lines = []

    Progress = RichProgress

    @staticmethod
    def report(status, same_line=False, **kwargs):
        """Report status to the user."""
        global line_length

        if same_line:
            new_line_length = line_length + len(status)
            if new_line_length > self.max_line_length:
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

    @contextmanager
    def progress(self, *args, **kwargs):
        p = self.Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        try:
            yield p
        finally:
            p.__exit__(None, None, None)

    def close(self):
        pass

    def status(self, status: str):
        pass

    def notify(self, status: str, title: str = None):
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

    def close(self):
        pass

    def status(self, status: str):
        pass

    def notify(self, status: str, title: str = None):
        pass


def main():
    print("main in reporter.py")
    reporter = LogAndTrayReporter()
    reporter.report("test")
    reporter.report("test2", same_line=True)
    reporter.report("test3", same_line=True)
    time.sleep(1)
    reporter.status("run")
    reporter.notify("oeleo started")
    time.sleep(1)
    reporter.status("check")
    time.sleep(2)
    reporter.status("run")
    time.sleep(2)
    reporter.status("none")

    while reporter.kill_me is False:
        print(".", end="")
        time.sleep(0.5)

    reporter.close(silent=False)


if __name__ == "__main__":
    main()
