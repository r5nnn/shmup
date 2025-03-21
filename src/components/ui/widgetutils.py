"""Module including the widget base class and other utilities for them to use."""

from __future__ import annotations

from typing import TYPE_CHECKING
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


class WidgetBase:
    x = AlignmentNeeded()
    y = AlignmentNeeded()
    align = AlignmentNeeded()

    def __init__(
        self,
        position: tuple[int, int] | list[int],
        align: RectAlignments | str = "topleft",
        *,
        sub_widget: bool = False,
    ):
        self._x, self._y = position
        self._align = align

        self.sub_widget = sub_widget
        self.sub_widget_on_top = True
        self.sub_widgets = []
        self.disabled = False
        self.hidden = False
        self.requires_realignment = False

    def update(self) -> None: ...

    def blit(self) -> None: ...

    def contains(self, x: int, y: int) -> ...:
        if self.disabled:  # noqa: RET503
            return False
        # return will be provided when method is overriden

    def __repr__(self):
        return (f"WidgetBase(position={self._x, self._y}, align={self.align}, "
                f"sub_widget={self.sub_widget})")
