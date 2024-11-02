import warnings
from abc import ABC, abstractmethod

import pygame

from data.components import InputBinder
from data.core import screen, screen_size
from data.core.utils import Singleton


class State(ABC):
    def __init__(self):
        self.state_manager = state_manager
        self.background = pygame.Surface(screen_size)

    @abstractmethod
    def startup(self):
        InputBinder.register(('keydown', pygame.K_ESCAPE),
                             action=self.back)

    @abstractmethod
    def cleanup(self):
        InputBinder.deregister(('keydown', pygame.K_ESCAPE))

    @abstractmethod
    def update(self, *args):
        ...

    @abstractmethod
    def render(self):
        screen.blit(self.background, (0, 0))

    def back(self):
        self.state_manager.pop()


class StateManager(metaclass=Singleton):
    def __init__(self):
        self.state_dict = {}
        self._state_stack = []
        self._current_state = None
        self.control = None

    @property
    def state_stack(self):
        return self._state_stack

    @property
    def current_state(self):
        """Use this property to check if the state stack is empty.
        Can be used by checking the boolean value:
        if self.current_state: pass
        if not self.current_state: pass"""
        if self._state_stack:
            return self._state_stack[-1]
        else:
            return None

    def _validate(self, state_name):
        if state_name.lower() not in self.state_dict:
            raise KeyError(
                f"No such state {state_name} in state dictionary: "
                f"{self.state_dict}")

    def _initialise_state(self, state_name):
        self._validate(state_name.lower())
        state_class = self.state_dict[state_name.lower()]
        return state_class()

    def append(self, state_name: str):
        if self.current_state:
            self.current_state.cleanup()
        self._state_stack.append(self._initialise_state(state_name))
        self.current_state.startup()

    def pop(self):
        if not self.current_state:
            raise AttributeError("No states to pop.")
        self.current_state.cleanup()
        self._state_stack.pop()
        if self.current_state:
            self.current_state.startup()

    def switch(self, state_name: str):
        if self.current_state:
            self.current_state.cleanup()
            self._state_stack.pop()
        else:
            warnings.warn("Attempted to switch state while no state was "
                          "present in the state stack.")
        self._state_stack.append(self._initialise_state(state_name))
        self.current_state.startup()

    def back_to(self, state_name: str):
        if self.current_state:
            self.current_state.cleanup()
        else:
            warnings.warn("Attempted to go back to a state when no state was "
                          "present in the state stack.")

        while self._state_stack and self.current_state != state_name:
            self._state_stack.pop()

        if self.current_state:
            self.current_state.startup()
        else:
            warnings.warn(f"State {state_name} not found in the state stack.")

    def quit(self):
        self.current_state.cleanup()
        self.control.quit()


state_manager = StateManager()
