from abc import ABC, abstractmethod

import pygame


class State(ABC):
    """Parent class for creating states."""
    def __init__(self):
        """Defines the screen and creates a black background meant to be
        overriden."""
        self._screen = pygame.display.get_surface()
        self._screen_size = self._screen.get_size()
        self.background = pygame.Surface(self._screen_size)
        self.surfaces = []

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
        pass

    @abstractmethod
    def startup(self):
        """Called when the state enters the top of the state stack."""
        pass

    @abstractmethod
    def cleanup(self):
        """Called when the state leaves the top of the state stack."""
        pass

    @abstractmethod
    def update(self, *args):
        """Called before self.render, meant to update all the state elements."""
        pass

    @abstractmethod
    def render(self):
        """Meant to render all the state's elements to the screen."""
        self.screen.blit(self.background, (0, 0))
        for surface, coordinates in self.surfaces:
            self.screen.blit(surface, coordinates)


class StateManager:
    """Class for interacting with the state stack."""
    def __init__(self):
        """Defines properties."""
        self._states = {}
        self._state_stack = []
        self._current_state = None

    def __call__(self, state_dict: dict):
        """Meant to be called only once to define the _states property.

        :param state_dict: A dictionary of initialised state objects and their
            names.
        """
        self._states = state_dict

    @property
    def states(self):
        return self._states

    @property
    def state_stack(self):
        return self._state_stack

    @property
    def current_state(self):
        return self._states[self._state_stack[-1]]

    def _validate(self, state_name):
        if state_name not in self._states:
            raise KeyError(f'No such state {state_name} in state dictionary: '
                           f'{self._states}')

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
        moving back to, states inbetween are ignored).

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


stateManager = StateManager()