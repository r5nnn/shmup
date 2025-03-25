"""Module containing functions to add and manage widgets from a centralised location."""

from __future__ import annotations

import logging
import warnings
from typing import TYPE_CHECKING

from src.components import events
from src.core.structs import OrderedWeakset

if TYPE_CHECKING:
    import weakref
    from src.components.ui.widgetutils import WidgetBase


logger = logging.getLogger("src.components.ui")


def blit() -> None:
    # Conversion is used to prevent errors when widgets are added/removed during
    # iteration a.k.a safe iteration
    for widget in list(widgets):
        if not widget.hidden:
            widget.blit()


def update() -> None:
    pos = events.get_mouse_pos()
    blocked = False

    for widget in reversed(list(widgets)):
        if widget.disabled:
            continue  # Skip disabled widgets immediately

        # Composite widget: it has children that need special handling
        if widget.has_sub_widgets:
            if not (interacted_subwidgets := widget.contains(*pos)):
                # No subwidgets are being interacted with so normal update
                widget.update()
            elif not blocked:
                # First widget interacted with
                widget.update()
                if not widget.allows_passthrough:
                    # Make sure other sprites also interacted with are not updated.
                    blocked = True
            else:
                # Some widget is already blocking -> update only the non-disabled subwidgets
                widget.update(interacted_subwidgets)

        # Non-composite widget
        else:
            if not blocked or not widget.contains(*pos):
                widget.update()
            if widget.contains(*pos) and not widget.allows_passthrough:
                blocked = True


def add_widget(*widgets_: WidgetBase) -> None:
    for widget in widgets_:
        if widget not in widgets:
            widgets.add(widget)
            move_to_top(widget)
        elif widget.sub_widget:
            warnings.warn(
                f"Attempted to add subwidget: {widget!r} to the widgethandler."
                f" Subwidgets should not be added to the widgethandler as the "
                f"parent widget renders and updates the subwidget.",
                stacklevel=2,
            )
        else:
            warnings.warn(
                f"Attempted to add widget: {widget!r} which already exists in "
                f"the widgethandler.",
                stacklevel=2,
            )


def remove_widget(*widgets_: WidgetBase) -> None:
    try:
        for widget in widgets_:
            widgets.remove(widget)
    except ValueError as e:
        warnings.warn(
            "Attempted to remove widget which doesn't exist in "
            f"the widgethandler: "
            f"{[widget_.__class__.__name__ for widget_ in list(widgets)]} "
            f"Error: {e}",
            stacklevel=2,
        )


def move_to_top(widget: WidgetBase) -> None:
    try:
        widgets.move_to_end(widget)
    except KeyError:
        warnings.warn(
            f"Attempted to move widget: {widget!r} to the top when"
            f" widget doesn't exist in widgethandler.",
            stacklevel=2,
        )


def move_to_bottom(widget: WidgetBase) -> None:
    try:
        widgets.move_to_start(widget)
    except KeyError:
        warnings.warn(
            f"Error: Tried to move {widget!r} to bottom when {widget!r} "
            f"doesn't exist in widgethandler.",
            stacklevel=2,
        )


widgets: OrderedWeakset[weakref.ref] = OrderedWeakset()
