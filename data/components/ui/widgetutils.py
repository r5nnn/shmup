"""Module including the widget base class and other utilities for them to use."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import override, Any

from typing import TYPE_CHECKING
from data.core.utils import Validator
from . import widgethandler

if TYPE_CHECKING:
    from data.components import RectAlignments


class AlignmentNeeded(Validator):
    @override
    def _validate(self, instance: Any, value: Any) -> None:
        instance._requires_realignment = True  # noqa: SLF001


class RenderNeeded(AlignmentNeeded):
    @override
    def _validate(self, instance: Any, value: Any) -> None:
        super()._validate(instance, value)
        instance._requires_rerender = True  # noqa: SLF001


class WidgetBase(ABC):
    x = AlignmentNeeded()
    y = AlignmentNeeded()
    align = AlignmentNeeded()

    def __init__(self, position: tuple[int, int],
                 align: RectAlignments = "topleft", *,
                 sub_widget: bool = False):
        self._x, self._y = position
        self._align = align
        self.sub_widget = sub_widget

        self._hidden = False
        self._disabled = False
        self._requires_realignment = False

    @abstractmethod
    def update(self) -> None:
        ...

    @abstractmethod
    def blit(self) -> None:
        ...

    def contains(self, x: int, y: int) -> bool:
        if self._disabled:
            return False

    def hide(self) -> None:
        self._hidden = True
        if not self.sub_widget:
            widgethandler.move_to_bottom(self)

    def show(self) -> None:
        self._hidden = False
        if not self.sub_widget:
            widgethandler.move_to_top(self)

    @property
    def disabled(self) -> bool:
        return self._disabled

    @disabled.setter
    def disabled(self, value: bool) -> None:
        self._disabled = value
