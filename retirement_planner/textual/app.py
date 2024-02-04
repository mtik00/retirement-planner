#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rich.text import TextType
from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, Static, Input, Button, Label
from textual.containers import Horizontal, Vertical, Container
from textual.widgets._button import ButtonVariant

from ..calculations import calculate_scenario
from .modals.help import HelpScreen


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
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="?", action="help", description="Show Help"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="app-grid"):
            with Vertical():
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

    def action_help(self):
        self.push_screen(HelpScreen())
