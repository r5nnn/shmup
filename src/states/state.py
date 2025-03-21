"""Contains base classes for both states and overlays."""

from __future__ import annotations

from typing import override

import pygame

from src.components.managers import statemanager, overlaymanager
from src.components.ui import widgethandler
from src.core import Printable
from src.core.data import system_data


class Overlay(Printable):
    def __init__(self):
        self.background = None
        self.widgets = []

    def startup(self) -> None:
        widgethandler.add_widget(*self.widgets)

    def cleanup(self) -> None:
        widgethandler.remove_widget(*self.widgets)

    def update(self) -> None:
        widgethandler.update()

    def render(self) -> None:
        widgethandler.blit()

    def back(self) -> None:
        overlaymanager.pop()


class State(Overlay):
    def __init__(self):
        super().__init__()
        if len(statemanager.state_stack) >= 1:
            self.background = statemanager.current_state().background
        else:
            self.background = pygame.Surface(system_data.abs_window_rect.size)

    def render(self) -> None:
        system_data.abs_window.blit(self.background, (0, 0))
        super().render()

    @override
    def back(self) -> None:
        statemanager.pop()
