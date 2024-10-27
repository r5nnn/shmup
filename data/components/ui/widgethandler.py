import weakref
from collections import OrderedDict
from collections.abc import MutableSet
from typing import override, TYPE_CHECKING

from data.components.input import inputmanager

if TYPE_CHECKING:
    from data.components.ui.widgetutils import WidgetBase


# Implementation of an insertion-ordered set. Necessary to keep track of the
# order in which widgets are added.
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
    # Conversion is used to prevent errors when widgets are added/removed
    # during iteration a.k.a safe iteration
    for widget in list(widgets):
        widget.blit()


def update() -> None:
    blocked = False
    # Conversion is used to prevent errors when widgets are added/removed
    # during iteration a.k.a safe iteration
    for widget in list(widgets)[::-1]:
        if not blocked or not widget.contains(*inputmanager.get_mouse_pos()):
            widget.update()

        # Ensure widgets covered by others are not affected
        # (widgets created later)
        # if widget.contains(*inputmanager.get_mouse_pos()):
        #     blocked = True


def add_widget(widget: "WidgetBase") -> None:
    if widget not in widgets:
        widgets.add(widget)
        move_to_top(widget)


def remove_widget(widget: "WidgetBase") -> None:
    try:
        widgets.remove(widget)
    except ValueError:
        print(f'Error: Tried to remove {widget} when {widget} '
              f'not in the set.')


def move_to_top(widget: "WidgetBase") -> None:
    try:
        widgets.move_to_end(widget)
    except KeyError:
        print(f'Error: Tried to move {widget} to top when {widget} '
              f'not in WidgetHandler.')


def move_to_bottom(widget: "WidgetBase") -> None:
    try:
        widgets.move_to_start(widget)
    except KeyError:
        print(f'Error: Tried to move {widget} to bottom when {widget} '
              f'not in WidgetHandler.')
