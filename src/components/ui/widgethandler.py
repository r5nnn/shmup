"""Module containing functions to add and manage widgets from a centralised location."""
from __future__ import annotations
import warnings
import weakref
from collections import OrderedDict
from collections.abc import MutableSet
from typing import override, TYPE_CHECKING, Any

from src.components import events

if TYPE_CHECKING:
    from src.components.ui.widgetutils import WidgetBase


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


def blit() -> None:
    # Conversion is used to prevent errors when widgets are added/removed during
    # iteration a.k.a safe iteration
    for widget in list(widgets):
        widget.blit()


def update() -> None:
    blocked = False
    for widget in reversed(list(widgets)):
        if widget.disabled or not blocked or not widget.contains(
                *events.get_mouse_pos()):
            widget.update()
        # Ensure widgets covered by others are not affected (widgets created later)
        if widget.contains(*events.get_mouse_pos()):
            blocked = True


def add_widget(*widget_tuple: WidgetBase) -> None:
    for widget in widget_tuple:
        if widget not in widgets:
            widgets.add(widget)
            move_to_top(widget)
        elif widget.sub_widget:
            warnings.warn(
                f"Attempted to add subwidget: {widget!r} to the widgethandler."
                f" Subwidgets should not be added to the widgethandler as the "
                f"parent widget renders and updates the subwidget.",
                stacklevel=2)
        else:
            warnings.warn(
                f"Attempted to add widget: {widget!r} which already exists in "
                f"the widgethandler.", stacklevel=2)


def remove_widget(widget: WidgetBase) -> None:
    try:
        widgets.remove(widget)
    except ValueError:
        warnings.warn(
            f"Attempted to remove widget: {widget!r} which doesn't exist in "
            f"the widgethandler.", stacklevel=2)


def move_to_top(widget: WidgetBase) -> None:
    try:
        widgets.move_to_end(widget)
    except KeyError:
        warnings.warn(f"Attempted to move widget: {widget!r} to the top when"
                      f" widget doesn't exist in widgethandler.", stacklevel=2)


def move_to_bottom(widget: WidgetBase) -> None:
    try:
        widgets.move_to_start(widget)
    except KeyError:
        warnings.warn(
            f"Error: Tried to move {widget!r} to bottom when {widget!r} "
            f"doesn't exist in widgethandler.", stacklevel=2)


widgets: _OrderedWeakset[weakref.ref] = _OrderedWeakset()
