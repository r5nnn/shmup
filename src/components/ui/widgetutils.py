"""Module including the widget base class and other utilities for them to use."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import override, Any

from typing import TYPE_CHECKING
from src.core.utils import Validator

if TYPE_CHECKING:
    from src.components import RectAlignments


class AlignmentNeeded(Validator):
    @override
    def _validate(self, instance: Any, value: Any) -> None:
        instance.requires_realignment = True


class RenderNeeded(AlignmentNeeded):
    @override
    def _validate(self, instance: Any, value: Any) -> None:
        super()._validate(instance, value)
        instance.requires_rerender = True


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
        self.disabled = False
        self.requires_realignment = False

    @abstractmethod
    def update(self) -> None:
        if self.disabled:
            return

    @abstractmethod
    def blit(self) -> None:
        ...

    @abstractmethod
    def contains(self, x: int, y: int) -> bool | None:
        if self.disabled:  # noqa: RET503
            return False
