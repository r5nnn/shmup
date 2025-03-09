"""Collection of overlays used by the button state."""

import pygame

from src.components.managers import statemanager
from src.components.ui import (
    TextArray,
    TextArrayConfig,
    TextRectToggleButton,
    TextButtonConfig,
)
from src.core import toggle_fullscreen, toggle_flag, config
from src.states.state import Overlay


class OptionsOverlay(Overlay):
    def __init__(self):
        super().__init__()
        headings_group = statemanager.current_state().option_headings_group
        self.text_pos = (
            statemanager.current_state().bg_rect.left
            + statemanager.current_state().padding,
            statemanager.current_state().bg_rect.top
            + headings_group.buttons[0].height
            + statemanager.current_state().padding * 1.5,
        )
        self.button_size = (200, 30)


class GeneralOptions(OptionsOverlay):
    def __init__(self):
        super().__init__()
        config_ = TextArrayConfig(
            (("Keep absolute position on fullscreen toggle:",),),
            wrap_width=500,
        )
        self.text_row1 = TextArray(
            self.text_pos,
            (1, 1),
            statemanager.current_state().padding * 1.5,
            config_,
        )
        self.widgets = (self.text_row1,)

    def update(self) -> None: ...


class GraphicsOptions(OptionsOverlay):
    def __init__(self):
        super().__init__()
        config_ = TextArrayConfig(
            (("Fullscreen:", "Borderless:", "Resolution:"),)
        )
        self.text_row1 = TextArray(
            self.text_pos,
            (3, 1),
            statemanager.current_state().padding * 1.5,
            config_,
        )

        config_ = TextButtonConfig(
            position=(
                self.text_row1.texts[0].rect.right
                + statemanager.current_state().padding,
                self.text_row1.texts[0].rect.centery,
            ),
            align="midleft",
        )
        self.fullscreen_button = TextRectToggleButton(
            config_,
            self.button_size,
            start_text=0 if config["flags"]["fullscreen"] else 1,
            on_toggle_on=toggle_fullscreen,
            on_toggle_off=toggle_fullscreen,
        )
        config_.position = (
            self.text_row1.texts[1].rect.right
            + statemanager.current_state().padding,
            self.text_row1.texts[1].rect.centery,
        )
        self.borderless_button = TextRectToggleButton(
            config_,
            self.button_size,
            on_toggle_on=lambda: toggle_flag(pygame.NOFRAME),
            on_toggle_off=lambda: toggle_flag(pygame.NOFRAME),
        )
        self.widgets = (
            self.text_row1,
            self.fullscreen_button,
            self.borderless_button,
        )

    def render(self) -> None:
        super().render()

    def update(self) -> None:
        if config["flags"]["fullscreen"]:
            self.fullscreen_button.toggle_on()
        else:
            self.fullscreen_button.toggle_off()
        if config["flags"]["noframe"]:
            self.borderless_button.toggle_on()
        else:
            self.borderless_button.toggle_off()


class KeybindsOptions(OptionsOverlay):
    def __init__(self):
        super().__init__()


class AudioOptions(OptionsOverlay):
    def __init__(self):
        super().__init__()
