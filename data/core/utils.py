"""Global utilities used by other submodules.

Contains custom type hints, Mouse button references, design pattern base 
classes, and a descriptor."""
from abc import ABC, ABCMeta, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import Literal, Callable


@dataclass(frozen=True)
class CustomTypes:
    """Contains custom game type hints."""
    rect_alignments = Literal[
        'topleft', 'midtop', 'topright',
        'midleft', 'center', 'midright',
        'bottomleft', 'midbottom', 'bottomright'
        ]
    alignments = Literal['left', 'right', 'center', 'block']
    input_types = Literal[
        'key', 'keydown', 'keyup',
        'mouse', 'mousedown', 'mouseup',
        'quit'
        ]


@dataclass(frozen=True)
class Mouse:
    """Contains pygame style references to mouse buttons."""
    LEFTCLICK = 1
    MIDDLECLICK = 2
    RIGHTCLICK = 3
    SCROLLUP = 4
    SCROLLDOWN = 5


class Singleton(type):
    """An implementation of the singleton design pattern in python.
    
    Makes all classes that inherit from this class only able to have
    one instance of the class. Subsequent attempts to instantiate a new class
    just return the first initialised object.""" 
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Observer(ABC):
    """An implementation of the observer design pattern in python.
    
    Allows you to register an event to a handler so that
    the handler is called whenever the event is detected."""

    def __init__(self):
        self._handlers = defaultdict(list)

    @abstractmethod
    def notify(self, *args):
        """Calls the registered handler."""

    @abstractmethod
    def register(self, event, handler: Callable):
        """Registers the event to a handler."""

    @abstractmethod
    def deregister(self, event, handler: Callable):
        """Deregisters the event from its handler."""

    def is_registered(self, event, handler: Callable) -> bool:
        """Check if handler is bound to an event."""
        return event in self._handlers and handler in self._handlers[event]


class SingletonABCMeta(Singleton, ABCMeta):
    pass


class Validator(ABC):
    """Descriptor parent class for validating a property in various ways."""
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
