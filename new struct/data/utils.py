from abc import ABC, ABCMeta, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class CustomTypes:
    rect_alignments = Literal['topleft', 'midtop', 'topright',
                              'midleft', 'center', 'midright',
                              'bottomleft', 'midbottom', 'bottomright']
    alignments = Literal['left', 'right', 'center', 'block']
    input_types = Literal['key', 'keydown', 'keyup',
                          'mouse', 'mousedown', 'mouseup',
                          'quit']

@dataclass(frozen=True)
class Mouse:
    LEFTCLICK = 1
    MIDDLECLICK = 2
    RIGHTCLICK = 3
    SCROLLUP = 4
    SCROLLDOWN = 5


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]

class Observer(ABC):

    def __init__(self):
        """
        Allows you to register an event to a handler so that
        the handler is called whenever the event is detected.
        """
        self._handlers = defaultdict(list)

    @abstractmethod
    def notify(self, *args):
        """Calls the registered handler."""

    @abstractmethod
    def register(self, event, handler):
        """Registers the event to a handler."""

    @abstractmethod
    def deregister(self, event, handler):
        """
        Deregisters the event from its handler.

        Args:
            event: Event to bound to handler.
            handler: Handler to deregister.
        """

    def is_registered(self, event, handler) -> bool:
        """
            Check if handler is bound to an event.

            Args:
                event: Event to check.
                handler: Handler bound to event.

            Returns:
                Bool confirming if handler is registered.
        """
        return event in self._handlers and \
            handler in self._handlers[event]


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
