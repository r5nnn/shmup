import warnings
from abc import ABC, abstractmethod

import pygame

from data.components import button_audio
from data.components import inputbinder
from data.core import screen, screen_size
from data.core.utils import Singleton


class State(ABC):
    def __init__(self):
        self.state_manager = state_manager
        self.background = pygame.Surface(screen_size)

    @abstractmethod
    def startup(self):
        inputbinder.register(('keydown', pygame.K_ESCAPE),
                             action=self.back)

    @abstractmethod
    def cleanup(self):
        inputbinder.deregister(('keydown', pygame.K_ESCAPE))

    @abstractmethod
    def update(self, *args):
        """Called before rendering"""

    @abstractmethod
    def render(self):
        screen.blit(self.background, (0, 0))

    def back(self):
        button_audio.play_audio('click', override=True)
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
        try:
            return self._state_stack[-1]
        except IndexError:
            return None

    def _validate(self, state_name):
        try:
            self.state_dict[state_name.lower()]
        except KeyError:
            print(f'No such state {state_name} in state dictionary: '
                  f'{self.state_dict}')
            raise

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
        try:
            self.current_state.cleanup()
            self._state_stack.pop()
            self.current_state.startup()
        except AttributeError:
            warnings.warn("Attempted to pop top level state when no states in"
                          "the state stack.")

    def switch(self, state_name: str):
        try:
            self.current_state.cleanup()
            self._state_stack.pop()
        except AttributeError:
            warnings.warn("Attempted to switch state while no state was "
                          "present in the state stack.")
        self._state_stack.append(self._initialise_state(state_name))
        self.current_state.startup()

    def back_to(self, state_name: str):
        try:
            self.current_state.cleanup()
        except AttributeError:
            warnings.warn("Attempted to go back to state when no state was "
                          "present in the state stack.")
        index = self._state_stack.index(state_name)
        self._state_stack = self._state_stack[:index + 1]
        self.current_state.startup()

    def quit(self):
        self.current_state.cleanup()
        self.control.quit()


state_manager = StateManager()
