import warnings

import pygame

from data.components import InputBinder
from data.components.ui import widgethandler
from data.core import screen, screen_size
from data.core.utils import Singleton


class State:
    def __init__(self):
        self.state_manager = state_manager
        self.background = pygame.Surface(screen_size)
        self.widgets = ()

    def add_widgets(self):
        for widget in self.widgets:
            widgethandler.add_widget(widget)

    def startup(self):
        InputBinder.register(("keydown", pygame.K_ESCAPE),
                             action=self.back)

    def clear_widgets(self):
        for widget in self.widgets:
            widgethandler.remove_widget(widget)

    def cleanup(self):
        InputBinder.deregister(("keydown", pygame.K_ESCAPE))

    def update(self, *args):
        widgethandler.update()

    def render(self):
        screen.blit(self.background, (0, 0))
        widgethandler.blit()

    def back(self):
        self.state_manager.pop()


class StateManager(metaclass=Singleton):
    def __init__(self):
        self.state_dict = {}
        self._state_stack = []
        self._current_state = None
        self.quit_game = None

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
            self.current_state.clear_widgets()
            self.current_state.cleanup()
        self._state_stack.append(self._initialise_state(state_name))
        self.current_state.startup()
        self.current_state.add_widgets()

    def pop(self):
        if not self.current_state:
            raise AttributeError("No states to pop.")
        self.current_state.clear_widgets()
        self.current_state.cleanup()
        self._state_stack.pop()
        if self.current_state:
            self.current_state.startup()
            self.current_state.add_widgets()

    def switch(self, state_name: str):
        if self.current_state:
            self.current_state.clear_widgets()
            self.current_state.cleanup()
            self._state_stack.pop()
        else:
            warnings.warn("Attempted to switch state while no state was "
                          "present in the state stack.")
        self._state_stack.append(self._initialise_state(state_name))
        self.current_state.startup()
        self.current_state.add_widgets()

    def back_to(self, state_name: str):
        if self.current_state:
            self.current_state.clear_widgets()
            self.current_state.cleanup()
        else:
            warnings.warn("Attempted to go back to a state when no state was "
                          "present in the state stack.")

        while self._state_stack and self.current_state != state_name:
            self._state_stack.pop()

        if self.current_state:
            self.current_state.startup()
            self.current_state.add_widgets()
        else:
            warnings.warn(f"State {state_name} not found in the state stack.")

    def quit(self):
        self.current_state.clear_widgets()
        self.current_state.cleanup()
        self.quit_game()

    def append_overlay(self, state: State, *args):
        """Append a temporary overlay state (like a popup) that can be easily dismissed."""
        if not self.current_state:
            raise ValueError("Overlay must be added on top of existing state.")
        self.current_state.cleanup()
        self._state_stack.append(state)
        self.current_state.startup()
        self.current_state.add_widgets()

    def pop_overlay(self):
        """Remove the overlay without affecting the underlying state."""
        if not self.current_state:
            raise AttributeError("No overlay to pop.")
        self.current_state.clear_widgets()
        self.current_state.cleanup()
        self._state_stack.pop()

        if self.current_state:  # Restart the underlying state’s handling
            self.current_state.startup()


state_manager = StateManager()
