#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rich.text import TextType
from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, Static, Input, Button, Label
from textual.containers import Horizontal, Vertical
from textual.widgets._button import ButtonVariant

from ..calculations import calculate_scenario

from .help import HelpScreen1, HelpScreen2


class GoButton(Button):
    def __init__(
        self,
        label: TextType | None = "Go",
        variant: ButtonVariant = "default",
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ):
        super().__init__(
            label, variant, name=name, id=id, classes=classes, disabled=disabled
        )


class Result(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RetirementApp(App):
    CSS_PATH = "app.tcss"
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

        with Horizontal():
            yield Label("Age at retirement")
            yield Input(type="integer", placeholder="55")

        with Horizontal():
            yield Label("Amount of retirement funds at retirement")
            yield Input(type="number", placeholder="1000000")

        with Horizontal():
            yield Label("Annual withdrawl during retirement")
            yield Input(type="number", placeholder="100000")

        yield GoButton()

        yield Result()

        yield Footer()

    def on_mount(self) -> None:
        self.title = "Retirement Calculator"

    def on_key(self, event: events.Key) -> None:
        self.query_one(Result).write(event)
