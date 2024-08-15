import inspect
import operator
from typing import Callable, override
from operator import attrgetter

from pygame.event import Event

from .observer import _Observer


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


generalEventManager = EventManager.get("General Events")
userEventManager = EventManager.get("User Events")
keyEventManager = EventManager.get("Key Events")
