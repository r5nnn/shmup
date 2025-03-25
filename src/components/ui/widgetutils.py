"""Module including the widget base class and other utilities for them to use."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override, Any

from src.core.structs import Validator

if TYPE_CHECKING:
    from collections.abc import Sequence
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
        allow_passthrough: bool = False,
        sub_widget: bool = False,
    ):
        self._x, self._y = position
        self._align = align
        self.allows_passthrough = allow_passthrough
        self.sub_widget = sub_widget

        self.has_sub_widgets = False
        self.disabled = False
        self.hidden = False
        self.requires_realignment = False

    @abstractmethod
    def update(self) -> None: ...

    @abstractmethod
    def blit(self) -> None: ...

    @abstractmethod
    def contains(self, x: int, y: int) -> bool:
        return not self.disabled

    @override
    def __str__(self):
        return f"<{self.__class__.__module__}.{self.__class__.__name__} {self.x=}, {self.y=}>"


class CompositeWidgetBase(WidgetBase, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_sub_widgets = True

    @abstractmethod
    @override
    def update(self, disabled_sub_widgets: Sequence[WidgetBase] = ()) -> bool:
        return self not in disabled_sub_widgets
