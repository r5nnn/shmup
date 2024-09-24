from abc import ABC, abstractmethod

import pygame

from data.utils import Singleton


class State(ABC):
    """Parent class for creating _states."""
    def __init__(self):
        """Defines the screen and creates a black background meant to be
        overriden."""
        self._screen = pygame.display.get_surface()
        self._screen_size = self._screen.get_size()

        self.background = pygame.Surface(self._screen_size)

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, value):
        self._screen = value
        self.update_screen()

    @property
    def screen_size(self):
        return self._screen_size

    @abstractmethod
    def update_screen(self):
        """Method meant to update the screen variables of all elements
        in the state using it."""

    @abstractmethod
    def startup(self):
        """Called when the state enters the top of the state stack."""

    @abstractmethod
    def cleanup(self):
        """Called when the state leaves the top of the state stack."""

    @abstractmethod
    def update(self, *args):
        """Called before self.render, meant to update all the state elements."""

    @abstractmethod
    def render(self):
        """Meant to render all the state's elements to the screen."""
        self.screen.blit(self.background, (0, 0))


class StateManager(metaclass=Singleton):
    """Class for interacting with the state stack."""
    def __init__(self):
        """Defines properties."""
        
        self.states = None
        self._state_stack = []
        self._current_state = None
        self.control = None

    @property
    def state_stack(self):
        return self._state_stack

    @property
    def current_state(self):
        return self.states[self._state_stack[-1]]

    def _validate(self, state_name):
        if state_name not in self.states:
            raise KeyError(f'No such state {state_name} in state dictionary: '
                           f'{self.states}')

    def append(self, state_name: str):
        """Gets the state object from the name passed and appends the state name
        to the end of the state stack. Calls relevant startup and cleanup
        methods.

        :param state_name: The name of the state to append as stored in the
            _states property dictionary.

        :raises KeyError: When state_name is not present in the _states property
            dictionary.
        """
        self._validate(state_name)
        if len(self._state_stack) > 1:
            self.current_state.cleanup()
        self._state_stack.append(state_name)
        self.current_state.startup()

    def pop(self):
        """Removes the last state from the state stack, calls relevant startup
        and cleanup methods."""
        self.current_state.cleanup()
        self._state_stack.pop()
        self.current_state.startup()

    def switch(self, state_name: str):
        """Removes the last state from the state stack, gets the state object
        from the name passed and appends the state name to the end of the state
        stack. Calls relevant startup and cleanup.
        methods.

        :param state_name: The name of the state to switch as stored in the
            _states property dictionary.

        :raises KeyError: When state_name is not present in the _states property
            dictionary.
        """
        self._validate(state_name)
        self.current_state.cleanup()
        self._state_stack.pop()
        self._state_stack.append(state_name)
        self.current_state.startup()

    def back_to(self, state_name: str):
        """Removes every state on top of the state to go back to, and calls the
        relevant startup and cleanup methods (only of the top state and state
        moving back to, _states inbetween are ignored).

        :param state_name: The name of the state to go back to as stored in the
            _states property dictionary.

        :raises KeyError: When state_name is not present in the _states property
            dictionary.
        :raises ValueError: When state_name is not present in the state stack.
        """
        self._validate(state_name)
        if state_name not in self._state_stack:
            raise ValueError(f'{state_name} state not in state stack: '
                             f'{self._state_stack}')
        self.current_state.cleanup()
        index = self._state_stack.index(state_name)
        self._state_stack = self._state_stack[:index+1]
        self.current_state.startup()
    
    def quit(self):
        self.current_state.cleanup()
        self.control.quit()


stateManager = StateManager()
