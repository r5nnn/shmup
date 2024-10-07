"""Module containing a widget handler, the widget base class and other utilities.

The widget handler is a set of functions that should be used after adding the
widget to the handler. This allows the managment of all widgets through a set
number of functions.
The widget base class is a base class meant to be inherited by most widgets.
It automatically adds the widget to the widget handler and defines the widget
rect. It also contains a method for collision checking the widget rect with a
point on the screen.
Also features decorators for widget properties that need to update the
`_requires_render` and `_requires_rect_update` properties upon being changed."""

import weakref
from abc import ABC, abstractmethod
from collections import OrderedDict
from collections.abc import MutableSet
from typing import override, Optional

import pygame

from data.components import inputmanager
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


class AlignmentNeeded(Validator):
    """Decorator that updates the `_requires_alignment` property to `True`."""
    @override
    def _validate(self, instance, value):
        instance._requires_realignment = True


class RenderNeeded(AlignmentNeeded):
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


def add_widget(widget: "WidgetBase") -> None:
    """Adds the widget given to an centralised ordered set of widgets.

    Widgets must be added so that all the other functions relating to the
    widgets can work.

    Args:
        widget: The widget to add to the set.
    """
    if widget not in _widgets:
        _widgets.add(widget)
        move_to_top(widget)


def remove_widget(widget: "WidgetBase") -> None:
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


def move_to_top(widget: "WidgetBase") -> None:
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


def move_to_bottom(widget: "WidgetBase") -> None:
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
    """Base class for widgets.
    
    Automatically adds itself to the widget hanlder. Inheritance when
    making a widget is optional if the widget deviates too much from 
    the base widget structure.
    
    Attributes:
        x: The x coordinate of the rect with reference to the alignment
            (given by `self.align`). Updates the rect when changed.
        y: The y coordinate of the rect with reference to the alignment
            (given by `self.align`). Updates the rect when changed.
        align: Alignment of the rect coordinates. Updates the rect when
            changed.
        surface: The surface which the widget will be displayed on.
        is_sub_widget: Boolean indicating if the widget is a subwidget.

            A subwidget is ignored by all widgethandler methods (that would
            usually affect all widgets). `True` indicates the widget is a sub
            widget.

    Args:
        position: The position of the rect with reference to the `align`
            argument passed.
        align: The point of the rect that the `position` argument is
            referencing. Defaults to `'topleft'`.
        surface: The surface that the widget should be rendered to. Defaults
            to `None` to use the current display surface.
        sub_widget: Whether the widget being made is part of another parent
            widget. If it is, it will not be added to the widget handler.
            Defaults to `False`."""
    x = AlignmentNeeded()
    y = AlignmentNeeded()
    align = AlignmentNeeded()
    
    def __init__(self, position: tuple[int, int], 
                 align: CustomTypes.rect_alignments = 'topleft',
                 surface: Optional[pygame.Surface] = None,
                 sub_widget: bool = False):
        self._x, self._y = position
        self._align = align
        self.surface = surface if surface is not None else \
            pygame.display.get_surface()
        self.is_sub_widget = sub_widget

        self._hidden = False
        self._disabled = False
        self._requires_realignment = False

        if not sub_widget:
            add_widget(self)

    @abstractmethod
    def update(self) -> None:
        """Updates the widget with user events."""

    @abstractmethod
    def blit(self) -> None:
        """Renders the widget onto the screen."""

    def hide(self) -> None:
        """Hides the widget from the screen."""
        self._hidden = True
        if not self.is_sub_widget:
            move_to_bottom(self)

    def show(self) -> None:
        """Displays the widget (if it was hidden previously)."""
        self._hidden = False
        if not self.is_sub_widget:
            move_to_top(self)

    def disable(self) -> None:
        """Disables the widget from recieving user input."""
        self._disabled = True

    def enable(self) -> None:
        """Enables the widget to recieve user input (if it was disabled previously)."""
        self._disabled = False

    def move_to_top(self) -> None:
        """Moves the widget to the top.

        A widget at the top will be rendered over all other widgets (if
        they are overlapping) and will always recieve input even if if there
        are other widgets below that should recieve input."""
        move_to_top(self)

    def move_to_bottom(self) -> None:
        """Moves the widget to the bottom.

        A widget at the bottom will be rendered under all other widgets (if
        they are overlapping) and will not recieve input if the overlapped part
        is interacted with."""
        move_to_bottom(self)