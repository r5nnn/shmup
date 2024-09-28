import weakref
from collections import OrderedDict
from collections.abc import MutableSet

from data.components.input import InputManager

# Implementation of an insertion-ordered set. Necessary to keep track of the 
# order in which widgets are added.
class OrderedSet(MutableSet):
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


class OrderedWeakset(weakref.WeakSet):
    _remove = ...  # Getting defined after the super().__init__() call

    def __init__(self, values=()):
        super(OrderedWeakset, self).__init__()

        self.data = OrderedSet()
        for elem in values:
            self.add(elem)

    def move_to_end(self, item):
        self.data.move_to_end(weakref.ref(item, self._remove))

    def move_to_start(self, item):
        self.data.move_to_start(weakref.ref(item, self._remove))


class WidgetHandler:
    _widgets: OrderedWeakset[weakref.ref] = OrderedWeakset()
    input_manager = InputManager()

    @staticmethod
    def blit():
        # Conversion is used to prevent errors when widgets are added/removed
        # during iteration a.k.a safe iteration
        widgets = list(WidgetHandler._widgets)

        for widget in widgets:
            widget.blit()

    @staticmethod
    def update() -> None:
        blocked = False

        # Conversion is used to prevent errors when widgets are added/removed
        # during iteration a.k.a safe iteration
        widgets = list(WidgetHandler._widgets)

        for widget in widgets[::-1]:
            if (not blocked or not
                widget.contains(*WidgetHandler.input_manager.get_mouse_pos())):
                widget.update()

            # Ensure widgets covered by others are not affected 
            # (widgets created later)
            if widget.contains(*WidgetHandler.input_manager.get_mouse_pos()):
                blocked = True

    @staticmethod
    def add_widget(widget) -> None:
        if widget not in WidgetHandler._widgets:
            WidgetHandler._widgets.add(widget)
            WidgetHandler.move_to_top(widget)

    @staticmethod
    def remove_widget(widget) -> None:
        try:
            WidgetHandler._widgets.remove(widget)
        except ValueError:
            print(f'Error: Tried to remove {widget} when {widget} '
                  f'not in WidgetHandler.')

    @staticmethod
    def move_to_top(widget):
        try:
            WidgetHandler._widgets.move_to_end(widget)
        except KeyError:
            print(f'Error: Tried to move {widget} to top when {widget} '
                  f'not in WidgetHandler.')

    @staticmethod
    def move_to_bottom(widget):
        try:
            WidgetHandler._widgets.move_to_start(widget)
        except KeyError:
            print(f'Error: Tried to move {widget} to bottom when {widget} '
                  f'not in WidgetHandler.')

    @staticmethod
    def update_screen(screen):
        for widget in WidgetHandler._widgets:
            widget.surface = screen

    @staticmethod
    def get_widgets():
        return WidgetHandler._widgets