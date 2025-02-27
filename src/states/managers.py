import warnings

import pygame
from typing import TYPE_CHECKING

from src.core import Singleton

if TYPE_CHECKING:
    from src.states.state import State, Overlay


class StateManager(metaclass=Singleton):
    def __init__(self):
        self.state_dict = {}
        self._state_stack = []
        self._current_state = None

    @property
    def state_stack(self) -> list["State"]:
        return self._state_stack

    @property
    def current_state(self) -> "State":
        if self._state_stack:
            return self._state_stack[-1]
        return None

    def _validate(self, state_name: str) -> None:
        if state_name.lower() not in self.state_dict:
            msg = (f"No such state {state_name} in state dictionary: "
                   f"{self.state_dict}")
            raise KeyError(msg)

    def _initialise_state(self, state_name: str) -> "State":
        self._validate(state_name)
        state_class = self.state_dict[state_name.lower()]
        return state_class()

    def append(self, state_name: str) -> None:
        if self.current_state:
            self.current_state.cleanup()
        self._state_stack.append(self._initialise_state(state_name))
        self.current_state.startup()

    def pop(self) -> None:
        if not self.current_state:
            msg = "No states to pop."
            raise AttributeError(msg)
        self.current_state.cleanup()
        self._state_stack.pop()
        if self.current_state:
            self.current_state.startup()

    def switch(self, state_name: str) -> None:
        if self.current_state:
            self.current_state.clear_widgets()
            self.current_state.cleanup()
            self._state_stack.pop()
        else:
            warnings.warn("Attempted to switch state while no state was "
                          "present in the state stack.", stacklevel=2)
        self._state_stack.append(self._initialise_state(state_name))
        self.current_state.startup()

    def back_to(self, state_name: str) -> None:
        if self.current_state:
            self.current_state.cleanup()
        else:
            warnings.warn("Attempted to go back to a state when no state was "
                          "present in the state stack.", stacklevel=2)

        while self._state_stack and self.current_state != state_name:
            self._state_stack.pop()

        if self.current_state:
            self.current_state.startup()
        else:
            warnings.warn(f"State {state_name} not found in the state stack.",
                          stacklevel=2)

    def quit(self) -> None:
        if self.current_state:
            self.current_state.cleanup()
        pygame.event.post(pygame.event.Event(pygame.QUIT))


class OverlayManager(metaclass=Singleton):
    def __init__(self):
        self._current_overlay = None
        self._overlay_stack = []

    @property
    def overlay_stack(self) -> list["Overlay"]:
        return self._overlay_stack

    @property
    def current_overlay(self) -> "Overlay":
        if self._overlay_stack:
            return self._overlay_stack[-1]
        return None

    def append(self, overlay: type["Overlay"]) -> None:
        self._overlay_stack.append(overlay())
        self.current_overlay.startup()

    def pop(self) -> None:
        if not self.current_overlay:
            msg = "No overlay to pop."
            raise AttributeError(msg)
        self.current_overlay.cleanup()
        self._overlay_stack.pop()

    def remove(self, overlay: type["Overlay"]) -> bool:
        for obj in self._overlay_stack:
            if isinstance(obj, overlay):
                obj.cleanup()
                self.overlay_stack.remove(obj)
                return True
        return False
