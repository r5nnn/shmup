from __future__ import annotations

from typing import override

from src.components.ui.buttons.imagebutton import (
    ImageToggleButton, ImageRectToggleButton)
from src.components.ui.buttons.imagebuttonarray import (
    ImageToggleButtonArray, ImageRectToggleButtonArray)
from src.components.ui.buttons.textbutton import (
    TextToggleButton, TextRectToggleButton)
from src.components.ui.buttons.textbuttonarray import (
    TextToggleButtonArray, TextRectToggleButtonArray)
from src.components.ui.widgetutils import WidgetBase

_AnyToggleButton = (TextToggleButton | TextRectToggleButton
                    | ImageToggleButton | ImageRectToggleButton)
_AnyToggleArray = (TextToggleButtonArray | TextRectToggleButtonArray
                   | ImageToggleButtonArray | ImageRectToggleButtonArray)


class ToggleButtonGroup(WidgetBase):
    def __init__(self, buttons: list[_AnyToggleButton], start_button: int = 0,
                 *, toggle_on_init: bool = True, sub_widget: bool = False):
        self.buttons = buttons
        self.start_button = start_button
        for button in self.buttons:
            button.sub_widget = True
        if toggle_on_init:
            self.toggle_start_button()
        super().__init__((0, 0), sub_widget=sub_widget)

    @override
    def update(self) -> None:
        for button in self.buttons:
            button.update()
            if button.toggled:
                for other_button in self.buttons:
                    if other_button != button and other_button.toggled:
                        other_button.toggle_off_call(silent=True)

    @override
    def blit(self) -> None:
        for button in self.buttons:
            button.blit()

    @override
    def contains(self, x: int, y: int) -> bool:
        return False

    def toggle_start_button(self) -> None:
        self.buttons[self.start_button].toggle_on_call(silent=True)


class ToggleArrayGroup(ToggleButtonGroup):
    def __init__(self, button_array: _AnyToggleArray, start_button: int = 0,
                 *, toggle_on_init: bool = True, sub_widget: bool = False):
        super().__init__(button_array.buttons, start_button,
                         toggle_on_init=toggle_on_init, sub_widget=sub_widget)
