import inspect
import operator
from collections import defaultdict
from operator import attrgetter
from typing import Any, Callable, override

from pygame.event import Event


class _Observer:
    """
    Attributes:
        managers: A dict containing the names of a manager linked to its object.
    """
    managers = dict()

    def __init__(self, name: str):
        """
        Private class meant to be inherited by other classes that use the
        observer design pattern.
        Allows you to register an event to a method so that
        the method is called whenever the event is detected.

        Args:
            name: The name to be tied with the observer
        """
        self.name = name
        self.handlers: dict = defaultdict(list)

    def notify(self, *args: Any) -> None:
        """
        Calls the registered handler.

        Args:
            *args: Any parameters to pass to the handler.
        """

    def register(self, event_type: Any, handler: Callable) -> None:
        """
        Registers a handler function with an associated event type.

        Args:
            event_type: The type of event to trigger the function call.
            handler: The function to be called upon detecting the event.
        """
        self.handlers[event_type].append(handler)

    def deregister(self, event_type: Any, handler: Callable) -> None:
        """
        Deregister a handler function from its associated event type.

        Args:
            event_type: The event type to stop detecting.
            handler: The function to stop calling on detection.
        """
        if handler in self.handlers[event_type]:
            self.handlers[event_type] = \
                [i for i in self.handlers[event_type] if i != handler]

    def is_registered(self, event_type: Any, handler: Callable) -> bool:
        """
        Check if handler is bound to an event.

        Args:
            event_type: Event type to check.
            handler: Handler bound to event.

        Returns:
            Bool confirming if handler is registered.
        """
        return event_type in self.handlers and \
            handler in self.handlers[event_type]

    @classmethod
    def get(cls, name: str) -> "_Observer":
        """
        Creates an object of name given if it doesn't already exist,
        otherwise just returns the already existing object.

        Args:
            name: The name attribute of the object to create/look for.

        Returns:
            The object if found, or a new object with the name provided.
        """
        if name not in cls.managers:
            cls.managers[name] = cls(name)
        return cls.managers[name]


class EventManager(_Observer):
    managers = dict()

    def __init__(self, name: str):
        """
        Allows you to register a pygame event to a method so that
        the method is called whenever the event is detected.
        """
        super().__init__(name)
        self.handlers: dict[int, list[Callable[[Event], None]]]

    @override
    def notify(self, event: Event,
               selector: operator.attrgetter = attrgetter("type")) -> None:
        """
        Args:
            event: The event occuring in the event handling loop.
            selector: Which attribute of event.Event to look for
        """
        for handler in self.handlers[selector(event)]:
            if 'event' in inspect.getfullargspec(handler).args:
                handler(event)
            else:
                handler()

    @override
    def register(self, event_type: int,
                 handler: Callable[[Event], None]) -> None:
        super().register(event_type, handler)

    @override
    def deregister(self, event_type: int,
                   handler: Callable[[Event], None]) -> None:
        super().deregister(event_type, handler)