from __future__ import annotations
import warnings

import pygame

from src.components import InputBinder
from src.components.ui import widgethandler
from src.core import screen, screen_size
from src.core.utils import Singleton


class State:
    def __init__(self):
        self.state_manager = StateManager()
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



class StateManager(metaclass=Singleton):
    def __init__(self):
        self.state_dict = {}
        self._state_stack = []
        self._current_state = None

    @property
    def state_stack(self) -> list[State]:
        return self._state_stack

    @property
    def current_state(self) -> State | None:
        if self._state_stack:
            return self._state_stack[-1]
        return None

    def _validate(self, state_name: str) -> None:
        if state_name.lower() not in self.state_dict:
            msg = (f"No such state {state_name} in state dictionary: "
                   f"{self.state_dict}")
            raise KeyError(msg)

    def _initialise_state(self, state_name: str) -> State:
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
