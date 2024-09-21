import inspect
import operator
import time
from abc import ABC, abstractmethod
from collections import defaultdict
from enum import Enum
from operator import attrgetter
from typing import Callable, override

import pygame
from pygame.event import Event


class _Observer(ABC):

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


class EventManager(_Observer):
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    @override
    def notify(self, event: Event, selector: operator.attrgetter = None):

        selector = attrgetter(self.name) if selector is None else None
        for handler in self._handlers[selector(event)]:
            if 'event' in inspect.getfullargspec(handler).args:
                handler(event)
            else:
                handler()

    @override
    def register(self, event_type: int, handler: Callable):
        self._handlers[event_type].append(handler)

    @override
    def deregister(self, event_type: int, handler: Callable):
        if handler in self._handlers[event_type]:
            self._handlers[event_type] = \
                [i for i in self._handlers[event_type] if i != handler]


class KeyManager(_Observer):
    def __init__(self):
        super().__init__()

    @override
    def register(self, keys: list[int], handler: Callable):
        key_tuple = tuple(sorted(keys))
        self._handlers[key_tuple].append(handler)

    @override
    def deregister(self, keys: list[int], handler: Callable) -> None:
        key_tuple = tuple(sorted(keys))
        if handler in self._handlers[key_tuple]:
            self._handlers[key_tuple] = \
                [i for i in self._handlers[key_tuple] if i != handler]

    @override
    def notify(self):
        pressed_keys = pygame.key.get_pressed()
        best_match = None

        for key_tuple in self._handlers:
            if self._are_keys_pressed(key_tuple, pressed_keys):
                # Find the combination with the most keys pressed
                if best_match is None or len(key_tuple) > len(best_match):
                    best_match = key_tuple

        if best_match:
            for callback in self._handlers[best_match]:
                callback()

    @staticmethod
    def _are_keys_pressed(key_tuple, pressed_keys) -> bool:
        """Check if all keys in key_tuple are pressed."""
        return all(pressed_keys[key] for key in key_tuple)


class MouseState(Enum):
    HOVER = 0
    CLICK = 1
    RIGHT_CLICK = 2
    DRAG = 3
    RIGHT_DRAG = 4  # useless but there for completeness
    RELEASE = 5
    RIGHT_RELEASE = 6


class Mouse:
    # Redundant currently, may use for double click handling
    # lmb and rmb is left mouse button and is right mouse button respectively
    last_lmb = 0
    last_rmb = 0
    lmb_elapsed_time = 0
    rmb_elapsed_time = 0

    _mouse_state = MouseState.HOVER

    @staticmethod
    def update_mouse_state():
        lmb = pygame.mouse.get_pressed()[0]
        rmb = pygame.mouse.get_pressed()[2]

        if lmb:
            if (Mouse._mouse_state == MouseState.CLICK or
                    Mouse._mouse_state == MouseState.DRAG):
                Mouse._mouse_state = MouseState.DRAG
            else:
                Mouse._mouse_state = MouseState.CLICK

        elif rmb:
            if (Mouse._mouse_state == MouseState.RIGHT_CLICK or
                    Mouse._mouse_state == MouseState.RIGHT_DRAG):
                Mouse._mouse_state = MouseState.RIGHT_DRAG
            else:
                Mouse._mouse_state = MouseState.RIGHT_CLICK
        else:
            # If previously was held down, call the release
            if (Mouse._mouse_state == MouseState.CLICK or
                    Mouse._mouse_state == MouseState.DRAG):
                Mouse._mouse_state = MouseState.RELEASE

            elif (Mouse._mouse_state == MouseState.RIGHT_CLICK or
                  Mouse._mouse_state == MouseState.RIGHT_DRAG):
                Mouse._mouse_state = MouseState.RIGHT_RELEASE

            else:
                Mouse._mouse_state = MouseState.HOVER

    @staticmethod
    def update_elapsed_time():
        # Also redundant until double click functionality implemented
        if (Mouse._mouse_state == MouseState.CLICK or Mouse._mouse_state ==
                MouseState.DRAG):
            Mouse.leftClickElapsedTime = time.time() - Mouse.last_lmb
        elif (Mouse._mouse_state == MouseState.RIGHT_CLICK or Mouse._mouse_state
              == MouseState.RIGHT_DRAG):
            Mouse.rightClickElapsedTime = time.time() - Mouse.last_rmb

    @staticmethod
    def get_mouse_state() -> MouseState:
        return Mouse._mouse_state

    @staticmethod
    def get_mouse_pos() -> tuple[int, int]:
        return pygame.mouse.get_pos()


class UserEvents:
    # Class-level counter to assign unique events
    _userevent_counter = pygame.USEREVENT
    user_events = {}

    def __init__(self,
                 name: str,
                 delay: int = None):
        self.user_event = UserEvents._userevent_counter
        self.delay = delay
        UserEvents._userevent_counter += 1
        UserEvents.user_events[name] = self.user_event

    def start_repeat(self):
        pygame.time.set_timer(self.user_event, self.delay) \
            if self.delay is not None else None

    def stop_repeat(self):
        pygame.time.set_timer(self.user_event, 0)


event_manager = EventManager("type")
key_manager = KeyManager()
event_manager.register(pygame.KEYDOWN, key_manager.notify)