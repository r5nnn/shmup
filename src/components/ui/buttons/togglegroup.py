from __future__ import annotations

from typing import override, TYPE_CHECKING

from src.components import events
from src.components.ui.widgetutils import CompositeWidgetBase, WidgetBase
from src.core.constants import LEFTCLICK

if TYPE_CHECKING:
    from collections.abc import Sequence
    from src.core.types import AnyToggleArray, AnyToggleButton


class ToggleButtonGroup(CompositeWidgetBase):
    def __init__(
        self,
        buttons: list[AnyToggleButton],
        start_button: int = 0,
        *,
        toggle_on_init: bool = True,
        sub_widget: bool = False,
    ):
        super().__init__((0, 0), sub_widget=sub_widget)
        self.buttons = buttons
        self.start_button = start_button
        for button in self.buttons:
            button.sub_widget = True
        if toggle_on_init:
            self.toggle_start_button()

    @override
    def update(self, disabled_sub_widgets: Sequence[WidgetBase] = ()) -> None:
        if not super().update(disabled_sub_widgets):
            return
        for button in self.buttons:
            if button not in disabled_sub_widgets:
                button.update(disabled_sub_widgets)
            if button.toggled:
                for other_button in self.buttons:
                    if other_button != button and other_button.toggled:
                        other_button.toggle_off_call(silent=True)

    @override
    def blit(self) -> None:
        for button in self.buttons:
            if not button.disabled:
                button.blit()

    @override
    def contains(self, x: int, y: int) -> list[AnyToggleButton]:
        if not super().contains(x, y):
            return []
        buttons = [button for button in self.buttons if button.contains(x, y)]
        return [self] if buttons == self.buttons else buttons

    def toggle_start_button(self) -> None:
        self.buttons[self.start_button].toggle_on_call(silent=True)
