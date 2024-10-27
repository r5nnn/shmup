from abc import ABC, abstractmethod
from typing import override

from data.components.ui import widgethandler
from data.core.utils import CustomTypes, Validator


class AlignmentNeeded(Validator):
    @override
    def _validate(self, instance, value):
        instance._requires_realignment = True


class RenderNeeded(AlignmentNeeded):
    @override
    def _validate(self, instance, value):
        super()._validate(instance, value)
        instance._requires_rerender = True


class WidgetBase(ABC):
    x = AlignmentNeeded()
    y = AlignmentNeeded()
    align = AlignmentNeeded()

    def __init__(self, position: tuple[int, int],
                 align: CustomTypes.rect_alignments = 'topleft',
                 sub_widget: bool = False):
        self._x, self._y = position
        self._align = align
        self.is_sub_widget = sub_widget

        self._hidden = False
        self._disabled = False
        self._requires_realignment = False

        if not sub_widget:
            widgethandler.add_widget(self)

    @abstractmethod
    def update(self) -> None:
        ...

    @abstractmethod
    def blit(self) -> None:
        ...

    def hide(self) -> None:
        self._hidden = True
        if not self.is_sub_widget:
            widgethandler.move_to_bottom(self)

    def show(self) -> None:
        self._hidden = False
        if not self.is_sub_widget:
            widgethandler.move_to_top(self)

    def disable(self) -> None:
        self._disabled = True

    def enable(self) -> None:
        self._disabled = False
