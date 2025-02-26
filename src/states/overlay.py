from __future__ import annotations
from typing import override

from src.components.ui import widgethandler
from src.core import Singleton
from src.states.state import State


class Overlay(State):
    def __init__(self):
        super().__init__()
        del self.state_manager
        self.overlay_manager = OverlayManager()
        self.background = None

    @override
    def render(self) -> None:
        widgethandler.blit()


class OverlayManager(metaclass=Singleton):
    def __init__(self):
        self._current_overlay = None
        self._overlay_stack = []

    @property
    def overlay_stack(self) -> list[Overlay]:
        return self._overlay_stack

    @property
    def current_overlay(self) -> Overlay | None:
        if self._overlay_stack:
            return self._overlay_stack[-1]
        return None

    def append(self, overlay: type[Overlay]) -> None:
        self._overlay_stack.append(overlay())
        self._current_overlay.startup()

    def pop(self) -> None:
        if not self.current_overlay:
            msg = "No overlay to pop."
            raise AttributeError(msg)
        self.current_overlay.cleanup()
        self._overlay_stack.pop()
