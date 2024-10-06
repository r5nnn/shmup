"""Module for getting and handling all forms of user input.
Also allows for custom userevents to be detected."""
from typing import Callable, override

import pygame

from data.core.utils import Singleton, Observer, SingletonABCMeta, CustomTypes


class InputManager(metaclass=Singleton):
    """Class that stores all the input states."""

    def __init__(self):
        """Creates all the lists for storing inputs."""
        self._keydown_events = []
        self._keyup_events = []
        self._held_keys = []
        self._mousedown_events = []
        self._mouseup_events = []
        self._mouse_buttons = []
        self._mouse_pos = (0, 0)
        self._quit = False

    @property
    def quit(self):
        return self._quit

    def process_events(self, events: list) -> None:
        """Process events from the pygame events list.
        
        Clears keydown and keyup events, iterates through and updates the
        input lists as necessary.
        
        :param events: `pygame.event.get()` should be passed in every game tick.
        """
        self._keydown_events.clear()
        self._keyup_events.clear()
        self._mousedown_events.clear()
        self._mouseup_events.clear()

        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    self._keydown_events.append(event.key)
                    self._held_keys.append(event.key)
                case pygame.KEYUP:
                    self._keyup_events.append(event.key)
                    self._held_keys.remove(event.key)
                case pygame.MOUSEBUTTONDOWN:
                    self._mousedown_events.append(event.button)
                    self._mouse_buttons.append(event.button)
                case pygame.MOUSEBUTTONUP:
                    self._mouseup_events.append(event.button)
                    self._mouse_buttons.remove(event.button)
                case pygame.QUIT:
                    self._quit = True

        self._mouse_pos = pygame.mouse.get_pos()

    def is_key_down(self, key: int) -> bool:
        """Checks if key is currently being pressed down
        (only happens at the very beginning of the keypress).

        :param key: The key to check for.
        :returns: True if key is being pressed down."""
        return key in self._keydown_events

    def is_key_up(self, key: int) -> bool:
        """Checks if the key is currently being released
        (only happens at the very end of the keypress).

        :param key: The key to check for.
        :returns: True if key is being released."""
        return key in self._keyup_events

    def is_key_pressed(self, key: int) -> bool:
        """Checks if key is currently being held down.
        
        :param key: The key to check for.
        :returns: True if key is being held."""
        return key in self._held_keys

    def is_mouse_down(self, button: int) -> bool:
        """Checks if the mouse button is currently being pressed
        (only happens at the very beginning of the button press).

        :param button: The mousebutton to check for.
        :returns: True if mousebutton is being pressed down."""
        return button in self._mousedown_events

    def is_mouse_up(self, button: int) -> bool:
        """Checks if the mouse button is currently being released
        (only happens at the very end of the button press).

        :param button: The mousebutton to check for.
        :returns: True if the mousebutton is being released."""
        return button in self._mouseup_events

    def is_mouse_pressed(self, button: int) -> bool:
        """Checks if the mouse button is being held down.

        :param button: The mousebutton to check for.
        :returns: True if button is being held down."""
        return button in self._mouse_buttons

    def get_mouse_pos(self) -> tuple[int, int]:
        """Gets the position of the mouse.

        :returns: The coordinates of the mouse."""
        return self._mouse_pos


class InputBinder(Observer, metaclass=SingletonABCMeta):
    """Class for binding inputs to execute callables via the observer algorithm."""

    def __init__(self):
        super().__init__()

    @override
    def register(self, *inputs: tuple[CustomTypes.input_types, int],
                 action: Callable) -> None:
        """
        :param inputs: A tuple of the type and input.
        :param action: The action to call upon the input being detected.
        """
        self._handlers[inputs] = action

    @override
    def deregister(self, *inputs: tuple[CustomTypes.input_types, int]) -> None:
        """
        :param inputs: A tuple of the type and input that the action should be
            unregistered from.
        """
        if inputs in self._handlers:
            self._handlers.pop(inputs)

    @override
    def notify(self, input_manager: InputManager) -> None:
        """
        :param input_manager: Input manager to get status of inputs.
        """
        # Sort bindings by priority (more inputs = higher priority)
        sorted_bindings = sorted(self._handlers.items(),
            key=lambda binding: len(binding[0]), reverse=True)
        # Track which inputs have already been used to prevent double execution
        used_inputs = set()

        for inputs, action in sorted_bindings:
            if self._are_inputs_active(inputs, input_manager, used_inputs):
                action()
                used_inputs.update(inputs)

    @staticmethod
    def _are_inputs_active(inputs, input_manager, used_inputs):
        for input_type, value in inputs:
            if (input_type, value) in used_inputs:
                return False
            elif (input_type == 'key' and not
                  input_manager.is_key_pressed(value)):
                return False
            elif (input_type == 'keydown' and not
                  input_manager.is_key_down(value)):
                return False
            elif (input_type == 'keyup' and not
                  input_manager.is_key_up(value)):
                return False
            elif (input_type == 'mouse' and not
                  input_manager.is_mouse_pressed(value)):
                return False
            elif (input_type == 'mousedown' and not
                  input_manager.is_mouse_down(value)):
                return False
            elif (input_type == 'mouseup' and not
                  input_manager.is_mouse_up(value)):
                return False
            elif input_type == 'quit' and not input_manager.quit:
                return False
        return True

inputmanager = InputManager()
inputbinder = InputBinder()