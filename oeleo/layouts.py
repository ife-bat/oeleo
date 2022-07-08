import os
import random
import time
from math import ceil

from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

N_ROWS_NOT_BODY = 9
N_COLS_NOT_BODY = 4


def create_layout():
    e_layout = Layout()
    e_layout.split_column(
        Layout(name="header", size=4),
        Layout(Panel("...idle..."), name="body"),
        Layout(name="footer", size=3),
    )
    e_layout["header"].split_row(
        Layout(Panel("oeleo\n-----"), name="left_header", minimum_size=14),
        Layout(Panel(""), name="middle_header", ratio=3),
        Layout(Panel(""), name="right_header", ratio=3),
    )
    e_layout["footer"].split_row(
        Layout(Panel(""), name="left_footer", minimum_size=14),
        Layout(Panel(""), name="middle_footer", ratio=3),
        Layout(Panel("q: CTRL+C"), name="right_footer", minimum_size=14),
        Layout(Panel(":smiley:"), name="status_footer", size=10),
    )
    return e_layout


def confirm(layout, q="Press ENTER to continue", a=":smiley:", pause=0.2):
    whoops = random.choice(
        [
            "earthquake",
            "car crash ",
            "mother in law ",
            "farted (sorry) " "Uncle Bob ",
            "thunderstorm",
            "lost my pants ",
        ]
    )
    smiley = random.choice(
        [
            ":smiley:",
            ":worried:",
            ":smiling_imp:",
            ":smiling_face_with_halo:",
            ":sunglasses:",
            ":smirk:",
        ]
    )

    layout["middle_footer"].update(Panel(q))
    button = input()
    if button:
        return False

    layout["middle_footer"].update(Panel(f"{smiley} whoops... {whoops}..."))
    time.sleep(pause)
    layout["middle_footer"].update(Panel(a))
    return True


def add_and_trim_text_if_needed(text, old_text=""):
    if old_text:
        _lines = old_text.split("\n")
        if len(_lines) > 200:
            _lines = _lines[-100:]
        _lines.append(text)
        text = "\n".join(_lines)
    return text


def update_body_panel(s):
    number_of_columns, number_of_rows = os.get_terminal_size()
    number_of_rows -= N_ROWS_NOT_BODY
    number_of_columns -= N_COLS_NOT_BODY

    _lines = s.split("\n")

    if len(_lines) > 0:
        pass
    _lines = _lines[-number_of_rows:]

    needed_rows_due_to_wrapping = 0
    _new_lines = []
    for _line in reversed(_lines):
        needed_rows_due_to_wrapping += ceil(Text(_line).cell_len / number_of_columns)
        if needed_rows_due_to_wrapping < number_of_rows:
            _new_lines.append(_line)
        else:
            break
    _lines = reversed(_new_lines)

    s = "\n".join(_lines)

    p = Panel(s)
    return p


def example_body_that_scrolls():
    layout = create_layout()
    with Live(layout, refresh_per_second=20, screen=True):
        txt = ""
        i = 0
        iteration = 0
        jumped = False
        while True:
            i += 1
            iteration += 1
            time.sleep(0.2)
            new_txt = (
                f"{i}: grunningr unningr unning grunningr unningr unning grunningr "
                f"unningr unning grunningr unningr unning grunningr unningr unning "
                f"grunningr unningr unning grunningr unningr unning grunningr unningr "
                f"unning grunningr unningr unning "
            )
            txt = add_and_trim_text_if_needed(new_txt, old_text=txt)
            body_panel = update_body_panel(
                txt,
            )
            layout["body"].update(body_panel)
            layout["left_footer"].update(Panel(f"I:{iteration:06}"))
            if i >= 100:
                i = 0
                layout["middle_footer"].update(Panel("Press ENTER to continue"))
                button = input()
                if button:
                    break
                whoops = random.choice(
                    [
                        "earthquake",
                        "car crash ",
                        "mother in law ",
                        "farted (sorry) " "Uncle Bob ",
                        "thunderstorm",
                        "lost my pants ",
                    ]
                )
                smiley = random.choice(
                    [
                        ":smiley:",
                        ":worried:",
                        ":smiling_imp:",
                        ":smiling_face_with_halo:",
                        ":sunglasses:",
                        ":smirk:",
                    ]
                )
                layout["middle_footer"].update(Panel(f"{smiley} whoops... {whoops}..."))
                jumped = True
                jump_start = time.time()
            if jumped and time.time() - jump_start > 1:
                layout["middle_footer"].update(Panel(f":smiley:"))


if __name__ == "__main__":
    example_body_that_scrolls()
