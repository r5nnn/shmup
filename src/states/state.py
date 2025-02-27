from __future__ import annotations
from typing import override

import pygame

from src.components import InputBinder
from src.components.ui import widgethandler
from src.core import screen, screen_size
from src.states.managers import StateManager, OverlayManager


class State:
    def __init__(self):
        self.state_manager = StateManager()
        self.overlay_manager = OverlayManager()
        self.input_binder = InputBinder()
        self.background = pygame.Surface(screen_size)
        self.widgets = ()

    def add_widgets(self) -> None:
        for widget in self.widgets:
            widgethandler.add_widget(widget)

    def startup(self) -> None:
        self.input_binder.register(("keydown", pygame.K_ESCAPE),
                                   action=self.back)
        self.add_widgets()

    def clear_widgets(self) -> None:
        for widget in self.widgets:
            widgethandler.remove_widget(widget)

    def cleanup(self) -> None:
        self.input_binder.deregister(("keydown", pygame.K_ESCAPE))
        self.clear_widgets()

    def update(self, *args) -> None:
        widgethandler.update()

    def render(self) -> None:
        screen.blit(self.background, (0, 0))
        widgethandler.blit()

    def back(self) -> None:
        self.state_manager.pop()


class Overlay(State):
    def __init__(self):
        super().__init__()
        self.current_state = self.state_manager.current_state
        self.overlay_manager = OverlayManager()
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
        self.overlay_manager.pop()
