"""Module containing a widget handler, the widget base class and other utilities.

The widget handler is a set of functions that should be used after adding the
widget to the handler. This allows the managment of all widgets through a set
number of functions.
todo: The widget base class does some stuff.
Also features decorators for widget properties that need to update the
`_requires_render` and `_requires_rect_update` properties upon being changed."""

import weakref
from abc import ABC, abstractmethod
from collections import OrderedDict
from collections.abc import MutableSet
from tkinter import BaseWidget
from typing import override, Type

import pygame

from data.components import inputmanager, inputbinder
from data.core.utils import CustomTypes, Validator


# Implementation of an insertion-ordered set. Necessary to keep track of the
# order in which widgets are added.
# noinspection PyMissingOrEmptyDocstring
class _OrderedSet(MutableSet):
    def __init__(self, values=()):
        self._od = OrderedDict.fromkeys(values)

    @override
    def __len__(self):
        return len(self._od)

    @override
    def __iter__(self):
        return iter(self._od)

    @override
    def __contains__(self, value):
        return value in self._od

    @override
    def add(self, value):
        self._od[value] = None

    @override
    def discard(self, value):
        self._od.pop(value, None)

    def move_to_end(self, value):
        self._od.move_to_end(value)

    def move_to_start(self, value):
        self._od.move_to_end(value, last=False)


# noinspection PyMissingOrEmptyDocstring
class _OrderedWeakset(weakref.WeakSet):
    _remove = ...  # Getting defined after the super().__init__() call

    def __init__(self, values=()):
        super(_OrderedWeakset, self).__init__()

        self.data = _OrderedSet()
        for elem in values:
            self.add(elem)

    def move_to_end(self, item):
        self.data.move_to_end(weakref.ref(item, self._remove))

    def move_to_start(self, item):
        self.data.move_to_start(weakref.ref(item, self._remove))


class RectUpdateNeeded(Validator):
    """Decorator that updates the `_requires_rect_update` property to `True`."""
    @override
    def _validate(self, instance, value):
        instance._requires_rect_update = True


class RenderNeeded(RectUpdateNeeded):
    """Decorator that updates the `_requires_render` property to `True`."""
    @override
    def _validate(self, instance, value):
        super()._validate(instance, value)
        instance._requires_render = True


_widgets: _OrderedWeakset[weakref.ref] = _OrderedWeakset()

def blit() -> None:
    """Calls all the widgets' `blit()` methods to render them onto the screen.

    Widgets are rendered in the order they were added. Must be called once
    every game tick."""
    # Conversion is used to prevent errors when widgets are added/removed
    # during iteration a.k.a safe iteration
    widgets = list(_widgets)

    for widget in widgets:
        widget.blit()

def update() -> None:
    """Calls all the widgets' `update()` methods. Update done varies by widget.

    Widgets are updated in the order they were added. If widgets are
    overlapping, only the topmost widget will be updated. Must be called once
    every game tick."""
    blocked = False

    # Conversion is used to prevent errors when widgets are added/removed
    # during iteration a.k.a safe iteration
    widgets = list(_widgets)

    for widget in widgets[::-1]:
        if not blocked or not widget.contains(*inputmanager.get_mouse_pos()):
            widget.update()

        # Ensure widgets covered by others are not affected
        # (widgets created later)
        if widget.contains(*inputmanager.get_mouse_pos()):
            blocked = True

def add_widget(widget: Type[BaseWidget]) -> None:
    """Adds the widget given to an centralised ordered set of widgets.

    Widgets must be added so that all the other functions relating to the
    widgets can work.

    Args:
        widget: The widget to add to the set.
    """
    if widget not in _widgets:
        _widgets.add(widget)
        move_to_top(widget)

def remove_widget(widget: Type[BaseWidget]) -> None:
    """Removes the widget given from the ordered set of widgets.

    Args:
        widget: The widget to remove from the set.

    Raises:
        ValueError: If the widget is not in the set."""
    try:
        _widgets.remove(widget)
    except ValueError:
        print(f'Error: Tried to remove {widget} when {widget} '
              f'not in the set.')

def move_to_top(widget: Type[BaseWidget]) -> None:
    """Moves the widget given to the top of the ordered set of widgets.

    Args:
        widget: The widget to move to the top of the set.

    Raises:
        KeyError: If the widget is not in the set."""
    try:
        _widgets.move_to_end(widget)
    except KeyError:
        print(f'Error: Tried to move {widget} to top when {widget} '
              f'not in WidgetHandler.')

def move_to_bottom(widget: Type[BaseWidget]) -> None:
    """Moves the widget given to the bottom of the ordered set of widgets.

    Args:
        widget: The widget to move to the bottom of the set.

    Raises:
        KeyError: If the widget is not in the set."""
    try:
        _widgets.move_to_start(widget)
    except KeyError:
        print(f'Error: Tried to move {widget} to bottom when {widget} '
              f'not in WidgetHandler.')

def update_screen(screen: pygame.Surface) -> None:
    """Updates the surface value for all of the widgets in the widget set.

    Args:
        screen: The new surface that the widgets should render to.
    """
    for widget in _widgets:
        widget.surface = screen

def get_widgets() -> _OrderedWeakset[weakref.ref]:
    """Getter function for the insertion-ordered set of widgets.

    Returns:
        The insertion-ordered set of widgets."""
    return _widgets


class WidgetBase(ABC):
    """Base class for widgets."""
    def __init__(self, position: tuple[int, int], size: tuple[int, int],
                 align: CustomTypes.rect_alignments = 'topleft',
                 sub_widget: bool = False):
        """"""
        self.surface = pygame.display.get_surface()
        self._x, self._y = position
        self._width, self._height = size
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._align = align
        self._align_rect(self._rect, self._align, self._rect.topleft)
        self._coords = getattr(self._rect, self._align)

        if not sub_widget:
            add_widget(self)

    def _align_rect(self, rect, align, coords):
        setattr(rect, align, coords)
        self._coords = self._x, self._y = getattr(rect, align)

    def contains(self, x: int, y: int):
        """Basic collision detection for the widget rectangle."""
        return (self._rect.left < x - self.surface.get_abs_offset()[0] <
                self._rect.left + self._width) and (
                self._rect.top < y - self.surface.get_abs_offset()[1] <
                self._rect.top + self._height)

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def blit(self):
        ...