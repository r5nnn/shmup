"""Module containing a set of functions that are used to interact with all
widgets added to the handler at once from a centralized location.

Attributes:
    widgets: An insertion-ordered set of widgets.
    """
import weakref
from collections import OrderedDict
from collections.abc import MutableSet
from typing import override, TYPE_CHECKING

import pygame

from data.components.input import inputmanager

if TYPE_CHECKING:
    from data.components.ui.widgetutils import WidgetBase


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


widgets: _OrderedWeakset[weakref.ref] = _OrderedWeakset()


def blit() -> None:
    """Calls all the widgets' `blit()` methods to render them onto the screen.

    Widgets are rendered in the order they were added. Must be called once
    every game tick."""
    # Conversion is used to prevent errors when widgets are added/removed
    # during iteration a.k.a safe iteration
    for widget in list(widgets):
        widget.blit()


def update() -> None:
    """Calls all the widgets' `update()` methods. Update done varies by widget.

    Widgets are updated in the order they were added. If widgets are
    overlapping, only the topmost widget will be updated. Must be called once
    every game tick."""
    blocked = False
    # Conversion is used to prevent errors when widgets are added/removed
    # during iteration a.k.a safe iteration
    for widget in list(widgets)[::-1]:
        if not blocked or not widget.contains(*inputmanager.get_mouse_pos()):
            widget.update()

        # Ensure widgets covered by others are not affected
        # (widgets created later)
        if widget.contains(*inputmanager.get_mouse_pos()):
            blocked = True


def add_widget(widget: "WidgetBase") -> None:
    """Adds the widget given to an centralised ordered set of widgets.

    Widgets must be added so that all the other functions relating to the
    widgets can work.

    Args:
        widget: The widget to add to the set.
    """
    if widget not in widgets:
        widgets.add(widget)
        move_to_top(widget)


def remove_widget(widget: "WidgetBase") -> None:
    """Removes the widget given from the ordered set of widgets.

    Args:
        widget: The widget to remove from the set.

    Raises:
        ValueError: If the widget is not in the set."""
    try:
        widgets.remove(widget)
    except ValueError:
        print(f'Error: Tried to remove {widget} when {widget} '
              f'not in the set.')


def move_to_top(widget: "WidgetBase") -> None:
    """Moves the widget given to the top of the ordered set of widgets.

    A widget at the top will be rendered over all other widgets (if
    they are overlapping) and will always recieve input even if if there
    are other widgets below that should recieve input.

    Args:
        widget: The widget to move to the top of the set.

    Raises:
        KeyError: If the widget is not in the set."""
    try:
        widgets.move_to_end(widget)
    except KeyError:
        print(f'Error: Tried to move {widget} to top when {widget} '
              f'not in WidgetHandler.')


def move_to_bottom(widget: "WidgetBase") -> None:
    """Moves the widget given to the bottom of the ordered set of widgets.

    A widget at the bottom will be rendered under all other widgets (if
    they are overlapping) and will not recieve input if the overlapped part
    is interacted with.

    Args:
        widget: The widget to move to the bottom of the set.

    Raises:
        KeyError: If the widget is not in the set."""
    try:
        widgets.move_to_start(widget)
    except KeyError:
        print(f'Error: Tried to move {widget} to bottom when {widget} '
              f'not in WidgetHandler.')


def update_screen(screen: pygame.Surface) -> None:
    """Updates the surface value for all of the widgets in the widget set.

    Args:
        screen: The new surface that the widgets should render to.
    """
    for widget in widgets:
        widget.surface = screen
