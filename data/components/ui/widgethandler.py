import weakref
from collections import OrderedDict
from collections.abc import MutableSet

from data.components.input import InputManager

# Implementation of an insertion-ordered set. Necessary to keep track of the 
# order in which widgets are added.
class _OrderedSet(MutableSet):
    def __init__(self, values=()):
        self._od = OrderedDict().fromkeys(values)

    def __len__(self):
        return len(self._od)

    def __iter__(self):
        return iter(self._od)

    def __contains__(self, value):
        return value in self._od

    def add(self, value):
        self._od[value] = None

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


_widgets: _OrderedWeakset[weakref.ref] = _OrderedWeakset()
_input_manager = InputManager()

def blit():
    # Conversion is used to prevent errors when widgets are added/removed
    # during iteration a.k.a safe iteration
    widgets = list(_widgets)

    for widget in widgets:
        widget.blit()

def update() -> None:
    blocked = False

    # Conversion is used to prevent errors when widgets are added/removed
    # during iteration a.k.a safe iteration
    widgets = list(_widgets)

    for widget in widgets[::-1]:
        if (not blocked or not
            widget.contains(*_input_manager.get_mouse_pos())):
            widget.update()

        # Ensure widgets covered by others are not affected
        # (widgets created later)
        if widget.contains(*_input_manager.get_mouse_pos()):
            blocked = True

def add_widget(widget) -> None:
    if widget not in _widgets:
        _widgets.add(widget)
        move_to_top(widget)

def remove_widget(widget) -> None:
    try:
        _widgets.remove(widget)
    except ValueError:
        print(f'Error: Tried to remove {widget} when {widget} '
              f'not in WidgetHandler.')

def move_to_top(widget):
    try:
        _widgets.move_to_end(widget)
    except KeyError:
        print(f'Error: Tried to move {widget} to top when {widget} '
              f'not in WidgetHandler.')

def move_to_bottom(widget):
    try:
        _widgets.move_to_start(widget)
    except KeyError:
        print(f'Error: Tried to move {widget} to bottom when {widget} '
              f'not in WidgetHandler.')

def update_screen(screen):
    for widget in _widgets:
        widget.surface = screen

def get_widgets():
    return _widgets