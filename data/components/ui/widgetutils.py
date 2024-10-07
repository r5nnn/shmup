"""Module containing general widget utilities.

The widget base class is a base class meant to be inherited by all widgets. It
is used to define basic properties such as coordinates and alignment, as well
as methods for interacting with the widget handler functions.

There are also two decorators for widget properties that require updating the
`_requires_rerender` and `_requires_realignment` properties upon being changed.
"""

from abc import ABC, abstractmethod
from typing import override, Optional

import pygame

from data.core.utils import CustomTypes, Validator
from data.components.ui import widgethandler


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


class WidgetBase(ABC):
    """Base class for widgets.
    
    Automatically adds itself to the widget hanlder. 
    
    Attributes:
        x: The x coordinate of the widget with reference to the alignment
            (given by `self.align`). Aligns the widget when changed.
        y: The y coordinate of the widget with reference to the alignment
            (given by `self.align`). Aligns the widget when changed.
        align: Alignment of the rect coordinates. Aligns the widget when
            changed.
        surface: The surface which the widget will be displayed on.
        is_sub_widget: Boolean indicating if the widget is a subwidget.

            A subwidget is ignored by all widgethandler methods (that would
            usually affect all widgets). `True` indicates the widget is a sub
            widget.

    Args:
        position: The position of the widget with reference to the `align`
            argument passed.
        align: The point of the widget that the `position` argument is
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
            widgethandler.add_widget(self)

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
            widgethandler.move_to_bottom(self)

    def show(self) -> None:
        """Displays the widget (if it was hidden previously)."""
        self._hidden = False
        if not self.is_sub_widget:
            widgethandler.move_to_top(self)

    def disable(self) -> None:
        """Disables the widget from recieving user input."""
        self._disabled = True

    def enable(self) -> None:
        """Enables the widget to recieve user input (if it was disabled previously)."""
        self._disabled = False
