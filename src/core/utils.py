"""Module containing variables and design patterns used globally across the game."""
from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from collections import defaultdict
from typing import Callable, ClassVar, Any, override
from typing import TYPE_CHECKING
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
        toggle_flag(pygame.FULLSCREEN)
    else:
        system_data["flags"] ^= pygame.FULLSCREEN
        config["flags"][DISPLAY_FLAG_NAMES[pygame.FULLSCREEN]] = not config[
            "flags"][DISPLAY_FLAG_NAMES[pygame.FULLSCREEN]]
        pygame.display.toggle_fullscreen()


class Singleton(type):
    """Implementation of the singleton design pattern."""

    _instances: ClassVar[dict[Singleton, Any]] = {}

    def __call__(cls, *args, **kwargs) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Observer(ABC):
    """Implementation of the observer design pattern."""

    def __init__(self):
        self._handlers = ()

    @abstractmethod
    def notify(self) -> None:
        """Notify the hanlder of updates."""

    @abstractmethod
    def register(self, *args, **kwargs) -> None:
        """Registers the handler."""

    @abstractmethod
    def deregister(self, *args, **kwargs) -> None:
        """Deregisters the handler."""

    @abstractmethod
    def is_registered(self, *args) -> bool:
        """Checks if handler is registered."""


# noinspection PyMethodOverriding
class EventObserver(Observer, ABC):
    """Implementation of the observer design pattern using events."""

    def __init__(self):
        super().__init__()
        self._handlers = defaultdict(list)

    @override
    def register(self, *args, **kwargs) -> None:
        """Registers the event to its handler."""

    @override
    def deregister(self, *args, **kwargs) -> None:
        """Deregisters the event from its handler."""

    @override
    def is_registered(self, event: int, handler: Callable) -> bool:
        return event in self._handlers and handler in self._handlers[event]


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
        self._validate(instance, value)
        setattr(instance, self.private_name, value)

    @abstractmethod
    def _validate(self, instance: Any, value: Any) -> None:
        pass
