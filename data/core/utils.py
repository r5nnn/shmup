from abc import ABC, ABCMeta, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable

dt = 1


@dataclass(frozen=True)
class Mouse:
    LEFTCLICK = 1
    MIDDLECLICK = 2
    RIGHTCLICK = 3
    SCROLLUP = 4
    SCROLLDOWN = 5


@dataclass(frozen=True)
class Popups:
    ANY = 0
    INFO = 1
    INPUT = 3
    OK_CANCEL = 4
    YES_NO = 5


@dataclass(frozen=True)
class Colors:
    BACKGROUND = (30, 30, 30)
    FOREGROUND = (35, 35, 35)
    ACCENT = (85, 85, 85)


@dataclass(frozen=True)
class ColorPalette:
    PRIMARY = (30, 30, 30)
    SECONDARY = (35, 35, 35)
    ACCENT = (85, 85, 85)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]


class Observer(ABC):
    def __init__(self):
        self._handlers = defaultdict(list)

    @abstractmethod
    def notify(self, *args):
        """Calls the registered handler."""

    @abstractmethod
    def register(self, event, handler: Callable):
        """Registers the event to its handler."""

    @abstractmethod
    def deregister(self, event, handler: Callable):
        """Deregisters the event from its handler."""

    def is_registered(self, event, handler: Callable) -> bool:
        return event in self._handlers and handler in self._handlers[event]


class SingletonABCMeta(Singleton, ABCMeta):
    pass


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

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
