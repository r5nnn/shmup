"""Used to process and query events."""
from __future__ import annotations

from typing import Sequence

import pygame
import pynput

from src.core.data import system_data

_keydown_events = []
_keyup_events = []
_held_keys = []
_mousedown_events = []
_mouseup_events = []
_mouse_buttons = []
_mouse_pos = (0, 0)
_mouse_controller = pynput.mouse.Controller()


def process(events: list[pygame.event.Event]) -> None:
    global _mouse_pos
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
                system_data["quit"] = True

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

def get_abs_mouse_pos() -> tuple[int, int]:
    return _mouse_controller.position

def set_abs_mouse_pos(pos: tuple[int, int]):
    _mouse_controller.position = pos
