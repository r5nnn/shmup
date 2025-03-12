"""Collection of overlays used by the button state."""

import pygame

from src.components.managers import statemanager
from src.components.ui import (
    TextArray,
    TextArrayConfig,
    TextButtonConfig,
    TextRectToggleButton,
)
from src.core.utils import toggle_flag, toggle_fullscreen
from src.core.data import settings
from src.states.state import Overlay


class OptionsOverlay(Overlay):
    def __init__(self):
        super().__init__()
        headings_group = statemanager.current_state().option_headings_group
        self.padding = statemanager.current_state().padding
        self.row_width = (
            statemanager.current_state().option_headings_group.buttons[0].width
        )
        self.row_positions = tuple(
            statemanager.current_state()
            .option_headings_group.buttons[num]
            .rect.right
            for num in range(
                len(statemanager.current_state().option_headings_group.buttons)
            )
        )
        self.text_pos = (
            statemanager.current_state().bg_rect.left + self.padding,
            statemanager.current_state().bg_rect.top
            + headings_group.buttons[0].height
            + self.padding,
        )
        self.button_size = (200, 30)


class GeneralOptions(OptionsOverlay):
    def __init__(self):
        super().__init__()
        config_ = TextArrayConfig(
            (("Keep absolute position on fullscreen toggle:",),),
            wrap_width=self.row_width - self.padding,
        )
        self.text_row1 = TextArray(
            self.text_pos, (1, 1), self.padding, config_
        )
        config_ = TextButtonConfig(
            position=(
                self.row_positions[0] + self.padding,
                self.text_row1.texts[0].wrap_rects[0].centery,
            ),
            align="midleft",
        )
        self.fullscreen_mouse_pos_button = TextRectToggleButton(
            config_,
            self.button_size,
            start_text=1 if settings.keep_mouse_pos else 0,
            on_toggle_on=lambda: setattr(settings, "keep_mouse_pos", True),
            on_toggle_off=lambda: setattr(settings, "keep_mouse_pos", False),
        )
        self.widgets = (self.text_row1, self.fullscreen_mouse_pos_button)

    def update(self) -> None:
        if settings.keep_mouse_pos:
            self.fullscreen_mouse_pos_button.toggle_on()
        else:
            self.fullscreen_mouse_pos_button.toggle_off()


class GraphicsOptions(OptionsOverlay):
    def __init__(self):
        super().__init__()
        config_ = TextArrayConfig(
            (("Fullscreen:", "Borderless:", "Resolution:"),)
        )
        self.text_row1 = TextArray(
            self.text_pos, (3, 1), self.padding, config_
        )

        config_ = TextButtonConfig(
            position=(
                self.row_positions[0] + self.padding,
                self.text_row1.texts[0].rect.centery,
            ),
            align="midleft",
        )
        self.fullscreen_button = TextRectToggleButton(
            config_,
            self.button_size,
            start_text=1 if settings.flags.fullscreen else 0,
            on_toggle_on=toggle_fullscreen,
            on_toggle_off=toggle_fullscreen,
        )
        config_.position = (
            self.row_positions[0] + self.padding,
            self.text_row1.texts[1].rect.centery,
        )
        self.borderless_button = TextRectToggleButton(
            config_,
            self.button_size,
            start_text=1 if settings.flags.noframe else 0,
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
        if settings.flags.fullscreen:
            self.fullscreen_button.toggle_on()
        else:
            self.fullscreen_button.toggle_off()
        if settings.flags.noframe:
            self.borderless_button.toggle_on()
        else:
            self.borderless_button.toggle_off()


class KeybindsOptions(OptionsOverlay):
    def __init__(self):
        super().__init__()


class AudioOptions(OptionsOverlay):
    def __init__(self):
        super().__init__()
