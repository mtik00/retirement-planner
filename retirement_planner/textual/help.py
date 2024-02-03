#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Markdown


HELP1 = """\
# Retirement Calculator

## Features

Markdown syntax and extensions are supported.

- Typography *emphasis*, **strong**, `inline code` etc.
- Headers
- Lists (bullet and ordered)
- Syntax highlighted code blocks
- Tables!
"""

HELP2 = """\
# Calculations
"""


class HelpScreen2(Screen):
    BINDINGS = [
        Binding(key="escape", action="app.pop_screen"),
        Binding(key="left", action="app.pop_screen"),
    ]

    def compose(self) -> ComposeResult:
        yield Markdown(HELP2)
        return super().compose()


class HelpScreen1(Screen):
    BINDINGS = [
        Binding(key="escape", action="app.pop_screen"),
        Binding(key="right", action="push_screen('help2')"),
    ]

    def compose(self) -> ComposeResult:
        yield Markdown(HELP1)
