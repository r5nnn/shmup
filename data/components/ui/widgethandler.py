"""Module containing functions to add and manage widgets from a centralised location."""
from __future__ import annotations
import warnings
import weakref
from collections import OrderedDict
from collections.abc import MutableSet
from typing import override, TYPE_CHECKING, Any

import data.components.input as InputManager

if TYPE_CHECKING:
    from data.components.ui.widgetutils import WidgetBase


# Implementation of an insertion-ordered set. Necessary to keep track of the
# order in which widgets are added.
class _OrderedSet(MutableSet):
    def __init__(self, values: tuple[weakref.ReferenceType] = ()):
        self._od = OrderedDict.fromkeys(values)

    @override
    def __len__(self):
        return len(self._od)

    @override
    def __iter__(self):
        return iter(self._od)

    @override
    def __contains__(self, value: weakref.ReferenceType):
        return value in self._od

    @override
    def add(self, value: weakref.ReferenceType) -> None:
        self._od[value] = None

    @override
    def discard(self, value: weakref.ReferenceType) -> None:
        self._od.pop(value, None)

    def move_to_end(self, value: weakref.ReferenceType) -> None:
        self._od.move_to_end(value)

    def move_to_start(self, value: weakref.ReferenceType) -> None:
        self._od.move_to_end(value, last=False)


class _OrderedWeakset(weakref.WeakSet):
    _remove = ...  # Getting defined after the super().__init__() call

    def __init__(self, values: tuple = ()):
        super().__init__()

        self.data = _OrderedSet()
        for elem in values:
            self.add(elem)

    def move_to_end(self, item: Any) -> None:
        self.data.move_to_end(weakref.ref(item, self._remove))

    def move_to_start(self, item: Any) -> None:
        self.data.move_to_start(weakref.ref(item, self._remove))


widgets: _OrderedWeakset[weakref.ref] = _OrderedWeakset()


def blit() -> None:
    # Conversion is used to prevent errors when widgets are added/removed during
    # iteration a.k.a safe iteration
    for widget in list(widgets):
        widget.blit()


def update() -> None:
    blocked = False
    for widget in list(widgets)[::-1]:
        if not widget.interactable:
            widget.update()
            continue

        if not blocked or not widget.contains(*InputManager.get_mouse_pos()):
            widget.update()
        # Ensure widgets covered by others are not affected (widgets created later)
        if widget.contains(*InputManager.get_mouse_pos()):
            blocked = True


def add_widget(widget: WidgetBase) -> None:
    if widget not in widgets:
        widgets.add(widget)
        move_to_top(widget)
    else:
        warnings.warn(f"Attempted to add widget: {widget} which already "
                      f"existed in the widgethandler: {widgets}.", stacklevel=2)


def remove_widget(widget: WidgetBase) -> None:
    try:
        widgets.remove(widget)
    except ValueError:
        warnings.warn(f"Attempted to remove widget: {widget} when widget not "
                      f"in the widgethandler: {widgets}.", stacklevel=2)


def move_to_top(widget: WidgetBase) -> None:
    try:
        widgets.move_to_end(widget)
    except KeyError:
        warnings.warn(f"Attempted to move widget: {widget} to the top when "
                      f"widget not in widgethandler: {widgets}.", stacklevel=2)


def move_to_bottom(widget: WidgetBase) -> None:
    try:
        widgets.move_to_start(widget)
    except KeyError:
        warnings.warn(f"Error: Tried to move {widget} to bottom when {widget} not in "
                      f"WidgetHandler.", stacklevel=2)
