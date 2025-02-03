"""Module containing variables and design patterns used globally across the game."""
from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from collections import defaultdict
from typing import Callable, ClassVar, Any, TypeVar, Generic, override

import pygame

dt = 1.0
_flags = pygame.FULLSCREEN | pygame.SCALED


def toggle_flag(flag: int) -> None:
    global _flags
    _flags ^= flag
    print('called w flag', flag)
    pygame.display.set_mode((1920, 1080), _flags)


def toggle_fullscreen() -> None:
    global _flags
    _flags ^= pygame.FULLSCREEN
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
    def notify(self, *args) -> None:
        """Notify the hanlder of updates."""

    @abstractmethod
    def register(self, handler: Any, *args) -> None:
        """Registers the handler."""

    @abstractmethod
    def deregister(self, handler: Any, *args) -> None:
        """Deregisters the handler."""

    def is_registered(self, handler: Any, *args) -> bool:
        return handler in self._handlers


# noinspection PyMethodOverriding
class EventObserver(Observer, ABC):
    """Implementation of the observer design pattern using events."""

    def __init__(self):
        super().__init__()
        self._handlers = defaultdict(list)

    @override
    def register(self, event: int, handler: Callable) -> None:
        """Registers the event to its handler."""

    @override
    def deregister(self, event: int, handler: Callable) -> None:
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

    def __set__(self, instance: Any, value):
        self._validate(instance, value)
        setattr(instance, self.private_name, value)

    @abstractmethod
    def _validate(self, instance: Any, value: Any) -> None:
        pass
