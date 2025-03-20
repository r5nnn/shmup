"""Module including the widget base class and other utilities for them to use."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Sequence
from typing import override, Any

from src.core.structs import Validator

if TYPE_CHECKING:
    from src.core.types import RectAlignments


class AlignmentNeeded(Validator):
    @override
    def validate(self, instance: Any, value: Any) -> None:
        instance.requires_realignment = True


class RenderNeeded(AlignmentNeeded):
    @override
    def validate(self, instance: Any, value: Any) -> None:
        super().validate(instance, value)
        instance.requires_rerender = True
        instance.requires_realignment = True


class WidgetBase(ABC):
    x = AlignmentNeeded()
    y = AlignmentNeeded()
    align = AlignmentNeeded()

    def __init__(
        self,
        position: Sequence[int, int],
        align: RectAlignments | str = "topleft",
        *,
        sub_widget: bool = False,
    ):
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
    def blit(self) -> None: ...

    # noinspection PyTypeChecker
    @abstractmethod
    def contains(self, x: int, y: int) -> bool:
        if self.disabled:  # noqa: RET503
            return False
        # return will be provided when method is overriden
