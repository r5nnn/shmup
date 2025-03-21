from __future__ import annotations

from typing import override, TYPE_CHECKING

from src.components.ui.widgetutils import WidgetBase

if TYPE_CHECKING:
    from src.core.types import AnyToggleButton, AnyToggleArray


class ToggleButtonGroup(WidgetBase):
    def __init__(
        self,
        buttons: list[AnyToggleButton],
        start_button: int = 0,
        *,
        toggle_on_init: bool = True,
        sub_widget: bool = False,
    ):
        super().__init__((0, 0), sub_widget=sub_widget)
        self.sub_widgets = buttons
        self.sub_widget_on_top = False
        self.start_button = start_button
        for button in self.sub_widgets:
            button.sub_widget = True
        if toggle_on_init:
            self.toggle_start_button()

    @override
    def update(self) -> None:
        for button in self.sub_widgets:
            button.update()
            if button.toggled:
                for other_button in self.sub_widgets:
                    if other_button != button and other_button.toggled:
                        other_button.toggle_off_call(silent=True)

    @override
    def blit(self) -> None:
        for button in self.sub_widgets:
            button.blit()

    @override
    def contains(self, x: int, y: int) -> bool:
        return False

    def toggle_start_button(self) -> None:
        self.sub_widgets[self.start_button].toggle_on_call(silent=True)

    def __repr__(self):
        return (f"ToggleButtonGroup(buttons={self.sub_widgets}, "
                f"start_button={self.start_button}, "
                f"toggle_on_init=..., sub_widget={self.sub_widget})")


class ToggleArrayGroup(ToggleButtonGroup):
    def __init__(
        self,
        buttons: AnyToggleArray,
        start_button: int = 0,
        *,
        toggle_on_init: bool = True,
        sub_widget: bool = False,
    ):
        super().__init__(
            buttons.sub_widgets,
            start_button,
            toggle_on_init=toggle_on_init,
            sub_widget=sub_widget,
        )

    def __repr__(self):
        return (f"ToggleArrayGroup(buttons={self.sub_widgets}, "
                f"start_button={self.start_button}, toggle_on_init=..., "
                f"sub_widget={self.sub_widget})")
