"""Used for associating events with functions"""
from typing import Callable
from operator import attrgetter
from collections import defaultdict

from pygame.event import Event


class EventManager:
    """
    Attributes:
        managers: A dict containing the name of the manager linked to its object
    """
    managers = dict()

    def __init__(self, name: str):
        """Initialises EventManager with the name of the manager and creates a defaultdict for the handlers.
        Args:
            name: The name to be tied with the event manager for easy refrence via a dict.
        """
        self.name = name
        self.handlers: dict[int, list[Callable[[Event], None]]] = defaultdict(list)
        self.pass_event = {}

    def notify(self, event: Event, selector=attrgetter("type")) -> None:
        """Calls the registered function with its associated event.

        Args:
            event: The event occuring in the event handling loop.
            selector: Which attribute of event.Event to look for
        """
        # noinspection PyTypeChecker
        for handler in self.handlers[selector(event)]:
            handler(event) if self.pass_event[selector(event)] else handler()

    def register(self, event_type: int, handler: Callable[[Event], None], pass_event: bool = True) -> None:
        """Registers a handler function with an associated event type.

        Args:
            event_type: The type of event to trigger the function call.
            handler: The function to be called upon detecting the event.
            pass_event: Should event be passed to function when detected
        """
        # print(f"{self.name} registered {event_type}")
        self.handlers[event_type].append(handler)
        self.pass_event[event_type] = pass_event

    def deregister(self, event_type: int, handler: Callable[[Event], None]) -> None:
        """Deregister a handler function from its associated event type.

        Args:
            event_type: The event type to stop detecting.
            handler: The function to stop calling on detection.
        """
        if handler in self.handlers[event_type]:
            self.handlers[event_type] = [handler_ for handler_ in self.handlers[event_type] if handler_ != handler]

    def _is_registered(self, event_type, handler):
        return event_type in self.handlers and handler in self.handlers[event_type]

    @classmethod
    def get(cls, name: str) -> "EventManager":
        """Creates a object of name given if it doesn't already exist, otherwise just returns the already existing object.

        Args:
            name: The name attribute of the object to create/look for.

        Returns:
            The object if found, or a new object with the name provided.
        """
        if name not in cls.managers:
            cls.managers[name] = cls(name)
        return cls.managers[name]


generalEventManager = EventManager.get("General Events")
userEventManager = EventManager.get("User Events")
keyEventManager = EventManager.get("Key Events")
