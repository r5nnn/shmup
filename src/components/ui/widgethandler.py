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
    blocked = False
    for widget in reversed(list(widgets)):
        if not widget.disabled:
            if not blocked or not widget.contains(*events.get_mouse_pos()):
                widget.update()
            # Ensure widgets covered by others are not affected (widgets created later)
            if widget.contains(*events.get_mouse_pos()):
                blocked = True


def add_widget(*widgets_: WidgetBase) -> None:
    for widget in widgets_:
        if widget not in widgets:
            _add_widget_with_subwidgets(
                widget, add_sub_widgets_first=not widget.sub_widget_on_top
            )
        else:
            warnings.warn(
                f"Attempted to add widget: {widget!r} which already exists in "
                f"the widgethandler.",
                stacklevel=2,
            )


def _add_widget_with_subwidgets(
    widget: WidgetBase, *, add_sub_widgets_first: bool
) -> None:
    def add_widget_() -> None:
        widgets.add(widget)
        move_to_top(widget)

    if not add_sub_widgets_first:
        add_widget_()
    for sub_widget in widget.sub_widgets:
        _add_widget_with_subwidgets(
            sub_widget, add_sub_widgets_first=not sub_widget.sub_widget_on_top
        )
    if add_sub_widgets_first:
        add_widget_()
    logger.info("Added widget %s to widgethandler.", repr(widget))


def remove_widget(*widgets_: WidgetBase) -> None:
    try:
        for widget in widgets_:
            _remove_widget_with_subwidgets(widget)
    except ValueError as e:
        warnings.warn(
            "Attempted to remove widget which doesn't exist in "
            f"the widgethandler: {e}",
            stacklevel=2,
        )


def _remove_widget_with_subwidgets(widget: WidgetBase) -> None:
    for sub_widget in widget.sub_widgets:
        _remove_widget_with_subwidgets(sub_widget)
    widgets.remove(widget)
    logger.info("Removed widget %s from the widgethandler.", repr(widget))


def move_to_top(*widgets_: WidgetBase) -> None:
    try:
        for widget in widgets_:
            widgets.move_to_end(widget)
    except KeyError as e:
        warnings.warn(
            f"Attempted to move widget to the top when"
            f" widget doesn't exist in widgethandler: {e}.",
            stacklevel=2,
        )


def move_to_bottom(*widgets_: WidgetBase) -> None:
    try:
        for widget in widgets_:
            widgets.move_to_start(widget)
    except KeyError as e:
        warnings.warn(
            f"Tried to move widget to bottom when widget "
            f"doesn't exist in widgethandler: {e}",
            stacklevel=2,
        )


widgets: OrderedWeakset[weakref.ref] = OrderedWeakset()
