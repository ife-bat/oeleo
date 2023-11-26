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

from rich.progress import TextColumn, SpinnerColumn
from rich.progress import Progress as RichProgress

from oeleo.utils import start_logger
from oeleo.console import simple_console

# used for same_line reporting in Reporter.report
NOT_LOGGED = ["\n", "\r", "\r\n", "", " ", " .", ".", "-", "o", "v", "!"]

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
        log.debug(f"STATUS: {status}")

    def notify(self, status: str, title: str = None):
        log.debug(f"NOTIFICATION: {status}")

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

    layout = None

    Progress = RichProgress

    @staticmethod
    def report(status, same_line=False, **kwargs):
        """Report status to the user."""

        if same_line:
            simple_console.print(status, end="")
            if status not in NOT_LOGGED:
                log.info(status)
        else:
            simple_console.print(status)
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
        except Exception as e:
            print(f"*")
        finally:
            p.__exit__(None, None, None)

    def close(self):
        pass

    def status(self, status: str):
        pass

    def notify(self, status: str, title: str = None):
        pass


def check_reporter():
    reporter = Reporter()
    reporter.report("test")
    reporter.report("test2")
    reporter.report("-> test2", same_line=True)
    reporter.report("test3", same_line=False)
    reporter.status("run")
    reporter.notify("oeleo started")
    reporter.report("check")
    with reporter.progress() as progress:
        task = progress.add_task("task", total=None)
        for i in range(20):
            time.sleep(0.1)
        progress.remove_task(task)


def check_log_and_tray_reporter():
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


def main():
    check_reporter()
    # check_log_and_tray_reporter()


if __name__ == "__main__":
    main()
