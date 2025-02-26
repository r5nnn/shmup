"""Module containing a collection on functions for checking if any inputs are active."""
from __future__ import annotations

from typing import Callable, override, TYPE_CHECKING

import pygame

from src.core import EventObserver
from src.core.utils import SingletonABCMeta

if TYPE_CHECKING:
    from src.core.constants import input_types


_keydown_events = []
_keyup_events = []
_held_keys = []
_mousedown_events = []
_mouseup_events = []
_mouse_buttons = []
_mouse_pos = (0, 0)
_quit = False


def get_quit() -> bool:
    return _quit


def process_events(events: list) -> None:
    global _quit, _mouse_pos
    _keydown_events.clear()
    _keyup_events.clear()
    _mousedown_events.clear()
    _mouseup_events.clear()

    for event in events:
        match event.type:
            case pygame.KEYDOWN:
                _keydown_events.append(event.key)
                _held_keys.append(event.key)
            case pygame.KEYUP:
                _keyup_events.append(event.key)
                _held_keys.remove(event.key)
            case pygame.MOUSEBUTTONDOWN:
                _mousedown_events.append(event.button)
                _mouse_buttons.append(event.button)
            case pygame.MOUSEBUTTONUP:
                _mouseup_events.append(event.button)
                _mouse_buttons.remove(event.button)
            case pygame.QUIT:
                _quit = True

    _mouse_pos = pygame.mouse.get_pos()


def is_key_down(key: int) -> bool:
    return key in _keydown_events


def is_key_up(key: int) -> bool:
    return key in _keyup_events


def is_key_pressed(key: int) -> bool:
    return key in _held_keys


def is_mouse_down(button: int) -> bool:
    return button in _mousedown_events


def is_mouse_up(button: int) -> bool:
    return button in _mouseup_events


def is_mouse_pressed(button: int) -> bool:
    return button in _mouse_buttons


def get_mouse_pos() -> tuple[int, int]:
    return _mouse_pos


class InputBinder(EventObserver, metaclass=SingletonABCMeta):
    """Singleton for binding inputs to call a function.

    For handling held persistent inputs, just check for the input directly.
    """

    def __init__(self):
        super().__init__()
        self._input_checks = {
            "key": is_key_pressed,
            "keydown": is_key_down,
            "keyup": is_key_up,
            "mouse": is_mouse_pressed,
            "mousedown": is_mouse_down,
            "mouseup": is_mouse_up,
            "quit": lambda: get_quit,
        }

    @override
    def register(self, *inputs: tuple[input_types, int],
                 action: Callable) -> None:
        self._handlers[inputs] = action

    @override
    def deregister(self, *inputs: tuple[input_types, int]) -> None:
        if inputs in self._handlers:
            self._handlers.pop(inputs)

    @override
    def notify(self) -> None:
        sorted_bindings = sorted(self._handlers.items(),
                                 key=lambda binding: len(binding[0]),
                                 reverse=True)
        used_inputs = set()

        for inputs, action in sorted_bindings:
            if self._are_inputs_active(inputs, used_inputs):
                action()
                used_inputs.update(inputs)

    def _are_inputs_active(self, inputs: tuple[str, int], used_inputs: set) -> bool:
        for input_type, value in inputs:
            if (input_type, value) in used_inputs:
                return False

            check_func = self._input_checks.get(input_type)
            if check_func is not None and not check_func(value):
                return False
        return True
