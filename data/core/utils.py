"""Module that contains constants and utilities used globally across the game.

Stores a module level global `dt` variable to avoid any relative imports.
Stores many constants in frozen dataclass namespaces.
Stores common design pattern abstract base classes like the singleton and observer.
Stores a descriptor validator abstract base class."""
from abc import ABC, ABCMeta, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, ClassVar

dt = 1.0


AbstractField = lambda: property(abstractmethod(lambda s: s))


def mixin_requiring(*attributes):
    def make_mixin_class(cls):
        wrapped_cls = type(cls.__name__, (cls, ABC), {})
        for a in attributes:
            for attr_name in a:
                setattr(wrapped_cls, attr_name, AbstractField())
        return wrapped_cls
    return make_mixin_class


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
    _instances: ClassVar[dict["Singleton", object]] = {}

    def __call__(cls, *args, **kwargs):
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
    def register(self, event, handler: Callable) -> None:
        """Registers the event to its handler."""

    @abstractmethod
    def deregister(self, event, handler: Callable) -> None:
        """Deregisters the event from its handler."""

    def is_registered(self, event, handler: Callable) -> bool:
        return event in self._handlers and handler in self._handlers[event]


class SingletonABCMeta(Singleton, ABCMeta):
    """Class used to combine a Singleton and ABC for use as a metaclass."""


class Validator(ABC):
    """Descriptor abstract base class for validating when a property is set."""
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        self._validate(instance, value)
        setattr(instance, self.private_name, value)

    @abstractmethod
    def _validate(self, instance, value):
        pass
