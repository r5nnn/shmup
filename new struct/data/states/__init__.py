from abc import ABC, abstractmethod
import warnings

import pygame

from data.utils import Singleton
from data.components import input


class State(ABC):
    """Parent class for creating _states."""
    def __init__(self):
        """Defines the screen and creates a black background meant to be
        overriden."""
        self._screen = pygame.display.get_surface()
        self._screen_size = self._screen.get_size()
        self.state_manager = stateManager
        self.input_manager = stateManager.input_manager
        self.input_binder = stateManager.input_binder
        self.input_binder.bind(('keydown', pygame.K_ESCAPE), self.back)

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
        """Called before self.render, meant to update all the state elements.
        """

    @abstractmethod
    def render(self):
        """Meant to render all the state's elements to the screen."""
        self._screen.blit(self.background, (0, 0))

    @abstractmethod
    def back(self):
        """Default behaviour exits to the previous states, however should be
        overriden in certain cases e.g. for the first state."""
        self.state_manager.pop()


class StateManager(metaclass=Singleton):
    """Class for interacting with the state stack."""
    def __init__(self, inputmanager, inputbinder):
        """Defines properties."""
        self._input_manager = inputmanager
        self._input_binder = inputbinder
        
        self.state_dict = {}
        self._state_stack = []
        self._current_state = None
        self.control = None

    @property
    def input_manager(self):
        return self._input_manager

    @property
    def input_binder(self):
        return self._input_binder

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
        """Gets the state object from the name passed and appends the state
        name to the end of the state stack. Calls relevant startup and cleanup
        methods.

        :param state_name: The name of the state to append as stored in the
        _states property dictionary.

        :raises KeyError: When state_name is not present in the _states
        property dictionary.
        """
        if self.current_state:
            self.current_state.cleanup()
        self._state_stack.append(self._initialise_state(state_name))
        self.current_state.startup()

    def pop(self):
        """Removes the last state from the state stack, calls relevant startup
        and cleanup methods."""
        try:
            self.current_state.cleanup()
            self._state_stack.pop()
            self.current_state.startup()
        except AttributeError:
            warnings.warn("Attempted to pop top level state when no states in"
                          "the state stack.")

    def switch(self, state_name: str):
        """Removes the last state from the state stack, gets the state object
        from the name passed and appends the state name to the end of the state
        stack. Calls relevant startup and cleanup.
        methods.

        :param state_name: The name of the state to switch as stored in the
            _states property dictionary.

        :raises KeyError: When state_name is not present in the _states
            property dictionary.
        """
        try:
            self.current_state.cleanup()
            self._state_stack.pop()
        except AttributeError:
            warnings.warn("Attempted to switch state while no state was "
                          "present in the state stack.")
        self._state_stack.append(self._initialise_state(state_name))
        self.current_state.startup()

    def back_to(self, state_name: str):
        """Removes every state on top of the state to go back to, and calls the
        relevant startup and cleanup methods (only of the top state and state
        moving back to, _states inbetween are ignored).

        :param state_name: The name of the state to go back to as stored in the
            _states property dictionary.

        :raises KeyError: When state_name is not present in the _states
            property dictionary.
        """
        try:
            self.current_state.cleanup()
        except AttributeError:
            warnings.warn("Attempted to go back to state when no state was "
                          "present in the state stack.")
        index = self._state_stack.index(state_name)
        self._state_stack = self._state_stack[:index+1]
        self.current_state.startup()
    
    def quit(self):
        self.current_state.cleanup()
        self.control.quit()


stateManager = StateManager(input.InputManager(), input.InputBinder())
