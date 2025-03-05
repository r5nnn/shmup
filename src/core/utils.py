"""Module containing functions and design patterns used globally across the game."""
from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from typing import ClassVar, Any
from src.core.constants import DISPLAY_FLAG_NAMES

import pygame

from src.core.data import config, system_data


def toggle_flag(flag: int) -> None:
    system_data["flags"] ^= flag
    config["flags"][DISPLAY_FLAG_NAMES[flag]] = not config[
        "flags"][DISPLAY_FLAG_NAMES[flag]]
    pygame.display.set_mode((1920, 1080), system_data["flags"])

def toggle_fullscreen() -> None:
    if system_data["flags"] & pygame.FULLSCREEN:
        # using the pygame inbuilt display.toggle_fullscreen to exit fullscreen
        # causes the noframe  flag and potentially other flags to disappear.
        # Toggling the flag and manually setting the mode of the screen makes
        # sure all flags are preserved.
        toggle_flag(pygame.FULLSCREEN)
    else:
        system_data["flags"] ^= pygame.FULLSCREEN
        config["flags"][DISPLAY_FLAG_NAMES[pygame.FULLSCREEN]] = not (
            config)["flags"][DISPLAY_FLAG_NAMES[pygame.FULLSCREEN]]
        pygame.display.toggle_fullscreen()


class Singleton(type):
    """Enforces the singleton pattern when passed as a metaclass."""

    _instances: ClassVar[dict[object, Singleton]] = {}

    def __call__(cls, *args, **kwargs) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonABCMeta(Singleton, ABCMeta):
    """Class used to combine a Singleton and ABC for use as a metaclass."""


class Validator(ABC):
    """Descriptor abstract base class for validating when a property is set."""

    def __set_name__(self, owner: type, name: str):
        self.private_name = "_" + name

    def __get__(self, instance: Any | None, owner: type | None = None):
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: Any, value: Any):
        self.validate(instance, value)
        setattr(instance, self.private_name, value)

    @abstractmethod
    def validate(self, instance: Any, value: Any) -> None:
        pass
