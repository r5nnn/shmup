"""Module containing functions and design patterns used globally across the game."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pygame

from src.core.constants import DISPLAY_FLAG_NAMES
from src.core.data import config, system_data
from src.components import events


def toggle_flag(flag: int) -> None:
    """Toggles the given flag and resets the screen mode with the new flags.

    :param flag: The integer value of the flag to toggle.
    """
    system_data["flags"] ^= flag
    config["flags"][DISPLAY_FLAG_NAMES[flag]] = not config[
        "flags"][DISPLAY_FLAG_NAMES[flag]]
    pygame.display.set_mode((1920, 1080), system_data["flags"])

def toggle_fullscreen() -> None:
    """Toggles the fullscreen flag of the screen.

    While this could be done using exclusively the toggle_flag procedure,
    pygame has an inbuilt toggle_fullscreen procedure that is more efficient,
    however doesn't work if already in fullscreen. This procedure abstracts the
    logic for choosing the correct method.

    Also sets the absolute position of the mouse cursor to the same location it
    was before toggling using pynput, since pygame cannot get or set
    coordinates beyond the main window.
    """
    coords = events.get_abs_mouse_pos()
    if system_data["flags"] & pygame.FULLSCREEN:
        # Ssing the pygame inbuilt display.toggle_fullscreen to exit fullscreen
        # causes the noframe  flag and potentially other flags to disappear.
        # Toggling the flag and manually setting the mode of the screen makes
        # sure all flags are preserved.
        toggle_flag(pygame.FULLSCREEN)
    else:
        system_data["flags"] ^= pygame.FULLSCREEN
        config["flags"][DISPLAY_FLAG_NAMES[pygame.FULLSCREEN]] = not (
            config)["flags"][DISPLAY_FLAG_NAMES[pygame.FULLSCREEN]]
        pygame.display.toggle_fullscreen()
    events.set_abs_mouse_pos(coords)


class Validator(ABC):
    """Descriptor abstract base class for validating when a property is set."""

    def __set_name__(self, owner: type, name: str):
        self.private_name = "_" + name

    def __get__(self, instance: Any | None, owner: type | None = None):
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: Any, value: Any):
        if getattr(instance, self.private_name) == value:
            return
        self.validate(instance, value)
        setattr(instance, self.private_name, value)

    @abstractmethod
    def validate(self, instance: Any, value: Any) -> None:
        pass
