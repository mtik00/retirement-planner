#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header


from .help import HelpScreen1, HelpScreen2


class RetirementApp(App):
    SCREENS = {"help": HelpScreen1(), "help2": HelpScreen2()}
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="question_mark",
            action="push_screen('help')",
            description="Show help screen",
            key_display="?",
        ),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Retirement Calculator"
