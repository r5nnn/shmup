"""Contains base classes for both states and overlays."""
from __future__ import annotations

from typing import override

import pygame

from src.components import events
from src.components.managers import statemanager, overlaymanager
from src.components.ui import widgethandler
from src.core import screen, screen_size


class State:
    def __init__(self):
        self.background = pygame.Surface(screen_size)
        self.widgets = ()

    def add_widgets(self) -> None:
        for widget in self.widgets:
            widgethandler.add_widget(widget)

    def startup(self) -> None:
        events.eventbinder.register(("keydown", pygame.K_ESCAPE),
                                   action=self.back)
        self.add_widgets()

    def clear_widgets(self) -> None:
        for widget in self.widgets:
            widgethandler.remove_widget(widget)

    def cleanup(self) -> None:
        events.eventbinder.deregister(("keydown", pygame.K_ESCAPE))
        self.clear_widgets()

    def update(self, *args) -> None:
        widgethandler.update()

    def render(self) -> None:
        screen.blit(self.background, (0, 0))
        widgethandler.blit()

    def back(self) -> None:
        statemanager.pop()


class Overlay(State):
    def __init__(self):
        super().__init__()
        self.background = None

    @override
    def render(self) -> None:
        widgethandler.blit()

    @override
    def startup(self) -> None:
        self.add_widgets()

    @override
    def cleanup(self) -> None:
        self.clear_widgets()

    @override
    def back(self) -> None:
        overlaymanager.pop()
