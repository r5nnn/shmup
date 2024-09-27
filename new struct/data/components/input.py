from typing import Callable

import pygame

from data.utils import Singleton


class InputManager(metaclass=Singleton):
    """Class that stores all the input states"""

    def __init__(self):
        """Creates all the lists for storing inputs."""
        self._keydown_events = list()
        self._keyup_events = list()
        self._held_keys = list()
        self._mouse_buttons = list()
        self._mouse_pos = (0, 0)
        self._quit = False

    @property
    def quit(self):
        return self._quit

    def process_events(self, events: list):
        """Clears keydown and keyup events, iterates through
        pygame events and updates the input lists as necessary.
        
        :param event: the events returned by pygame.event.get()
        """
        self._keydown_events.clear()
        self._keyup_events.clear()

        for event in events:
            if event.type == pygame.KEYDOWN:
                self._keydown_events.append(event.key)
                self._held_keys.append(event.key)
            elif event.type == pygame.KEYUP:
                self._keyup_events.append(event.key)
                self._held_keys.remove(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_buttons.append(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_buttons.remove(event.button)
            elif event.type == pygame.QUIT:
                self._quit = True

        self._mouse_pos = pygame.mouse.get_pos()

    def is_key_pressed(self, key: int):
        """Checks if key is currently being held down
        
        :param key: the key to check for.
        
        returns: True if key is in the held_keys list."""
        return key in self._held_keys

    def is_key_down(self, key: int):
        """returns: True if key is in the keydown_events list."""
        return key in self._keydown_events

    def is_key_up(self, key: int):
        """returns: True if key is in the keyup_events list."""
        return key in self._keyup_events

    def is_mouse_button_pressed(self, button: int):
        """returns: True if button is in the mouse_buttons list."""
        return button in self._mouse_buttons

    def get_mouse_pos(self) -> tuple[int, int]:
        """returns: The position of the mouse."""
        return self._mouse_pos


class InputBinder:
    """Class for binding inputs to execute callables via the
    observer algorithm."""

    def __init__(self):
        self._bindings = {}

    def bind(self, *inputs: tuple[str, int], action: Callable):
        """Bind a specific input combination to an action.
        
        :param inputs: Tuple of the type and input
        :param action: The"""
        self._bindings[inputs] = action

    def process_bindings(self, input_manager: InputManager):
        """Check current input state and trigger actions.
        
        :param input_manager: """
        for inputs, action in self._bindings.items():
            if self._are_inputs_active(inputs, input_manager):
                action()

    @staticmethod
    def _are_inputs_active(inputs, input_manager):
        """Check if the required inputs are active based on the InputManager.
        """
        for input_type, value in inputs:
            print(input_type, value)
            if input_type == 'key' and not input_manager.is_key_pressed(value):
                return False
            elif (input_type == 'keyup' and not
            input_manager.is_key_down(value)):
                return False
            elif (input_type == 'keydown' and not
            input_manager.is_key_up(value)):
                return False
            elif (input_type == 'mouse' and not
            input_manager.is_mouse_button_pressed(value)):
                return False
            elif input_type == 'quit' and not input_manager.quit:
                return False
        return True
  
