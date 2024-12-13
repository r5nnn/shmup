"""Module containing variables and design patterns used globally across the game."""
from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, ClassVar, Any, TypeVar, Generic

import pygame

dt = 1.0
_T = TypeVar("_T")


@dataclass(frozen=True)
class Mouse:
    """Pygame style references to mouse buttons."""

    LEFTCLICK = 1
    MIDDLECLICK = 2
    RIGHTCLICK = 3
    SCROLLUP = 4
    SCROLLDOWN = 5


@dataclass(frozen=True)
class Colors:
    """Pygame style references to shmup's color palette."""

    PRIMARY = (30, 30, 30)
    SECONDARY = (35, 35, 35)
    ACCENT = (85, 85, 85)


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
        self._handlers = defaultdict(list)

    @abstractmethod
    def notify(self, *args) -> None:
        """Calls the registered handler."""

    @abstractmethod
    def register(self, event: int, handler: Callable) -> None:
        """Registers the event to its handler."""

    @abstractmethod
    def deregister(self, event: int, handler: Callable) -> None:
        """Deregisters the event from its handler."""

    def is_registered(self, event: int, handler: Callable) -> bool:
        return event in self._handlers and handler in self._handlers[event]


class SingletonABCMeta(Singleton, ABCMeta):
    """Class used to combine a Singleton and ABC for use as a metaclass."""


class Validator(ABC, Generic[_T]):
    """Descriptor abstract base class for validating when a property is set."""

    def __set_name__(self, owner: type, name: str):
        self.private_name = "_" + name

    def __get__(self, instance: Any | None, owner: type | None = None) -> _T:
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: Any, value: _T):
        self._validate(instance, value)
        setattr(instance, self.private_name, value)

    @abstractmethod
    def _validate(self, instance: Any, value: _T) -> None:
        pass
