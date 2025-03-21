"""Collection of overlays used by the button state."""

import pygame

from src.components.managers import statemanager
from src.components.ui import (
    TextArray,
    TextArrayConfig,
    TextButtonConfig,
    TextRectToggleButton,
    TextDropdown,
)
from src.core import keybinds
from src.core.data import settings, system_data
from src.states.state import Overlay
from src.core.utils import toggle_flag, toggle_fullscreen, set_resolution, \
    update_scale_factor


class OptionsOverlay(Overlay):
    def __init__(self):
        super().__init__()
        headings_group = statemanager.current_state().option_headings_group
        self.padding = statemanager.current_state().padding
        self.row_width = (
            statemanager.current_state().option_headings_group.sub_widgets[0].width
        )
        self.row_positions = tuple(
            statemanager.current_state()
            .option_headings_group.sub_widgets[num]
            .rect.right
            for num in range(
                len(statemanager.current_state().option_headings_group.sub_widgets)
            )
        )
        self.text_pos = [
            statemanager.current_state().bg_rect.left + self.padding,
            statemanager.current_state().bg_rect.top
            + headings_group.sub_widgets[0].height
            + self.padding,
        ]
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
                self.text_row1.sub_widgets[0].rect.centery,
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
            (
                (
                    "Fullscreen:",
                    "Borderless:",
                    "Resolution:",
                    "Allow non-integer resolution scaling:",
                    "Allow non-native resolution ratio:"
                ),
            ),
            wrap_width=self.row_width - self.padding,
        )
        self.text_row1 = TextArray(
            self.text_pos, (5, 1), self.padding, config_
        )

        config_ = TextButtonConfig(
            position=(
                self.row_positions[0] + self.padding,
                self.text_row1.sub_widgets[0].rect.centery,
            ),
            align="midleft",
        )
        self.fullscreen_button = TextRectToggleButton(
            config_,
            self.button_size,
            start_text=1 if settings.flags["fullscreen"] else 0,
            on_toggle_on=toggle_fullscreen,
            on_toggle_off=toggle_fullscreen,
        )
        config_.position = (
            self.row_positions[0] + self.padding,
            self.text_row1.sub_widgets[1].rect.centery,
        )
        self.borderless_button = TextRectToggleButton(
            config_,
            self.button_size,
            start_text=1 if settings.flags["noframe"] else 0,
            on_toggle_on=lambda: toggle_flag(pygame.NOFRAME),
            on_toggle_off=lambda: toggle_flag(pygame.NOFRAME),
        )
        resolutions, resolutions_str = self.recalculate_resolutions(
            non_int_scaling=settings.non_int_scaling
        )
        self.resolution_dropdown = TextDropdown(
            (
                self.row_positions[0] + self.padding,
                self.text_row1.sub_widgets[2].rect.centery,
            ),
            self.button_size,
            choices=resolutions_str,
            start_choice=resolutions.index(settings.resolution),
            actions=lambda index: set_resolution(resolutions[index]),
            align="midleft",
        )
        config_.position = (
            self.row_positions[0] + self.padding,
            self.text_row1.sub_widgets[3].rect.centery,
        )
        self.non_int_scaling_button = TextRectToggleButton(
            config_,
            self.button_size,
            start_text=1 if settings.non_int_scaling else 0,
            on_toggle_on=lambda: self.recalculate_resolutions(
                non_int_scaling=True
            ),
            on_toggle_off=lambda: self.recalculate_resolutions(
                non_int_scaling=False
            ),
        )
        config_.position = (
            self.row_positions[0] + self.padding,
            self.text_row1.sub_widgets[4].rect.centery,
        )
        self.non_native_resolution_ratio_button = TextRectToggleButton(
            config_,
            self.button_size,
            start_text=1 if settings.non_native_ratio else 0,
        )
        self.widgets = (
            self.text_row1,
            self.fullscreen_button,
            self.borderless_button,
            self.non_int_scaling_button,
            self.non_native_resolution_ratio_button,
            self.resolution_dropdown,
        )

    def update(self) -> None:
        if settings.flags["fullscreen"]:
            self.fullscreen_button.toggle_on()
        else:
            self.fullscreen_button.toggle_off()
        if settings.flags["noframe"]:
            self.borderless_button.toggle_on()
        else:
            self.borderless_button.toggle_off()
        if settings.non_int_scaling:
            self.non_int_scaling_button.toggle_on()
        else:
            self.non_int_scaling_button.toggle_off()

    def recalculate_resolutions(
        self, *, non_int_scaling: bool, update_dropdown: bool = False
    ) -> tuple[list[tuple[int, int]], list[str]]:
        settings.non_int_scaling = non_int_scaling
        update_scale_factor()
        resolutions = pygame.display.list_modes()
        if not non_int_scaling:
            resolutions = [
                resolution
                for resolution in resolutions
                if min(resolution[0] // system_data.abs_window_rect.width,
                       resolution[1] // system_data.abs_window_rect.height) != 0
            ]
        # Truncate list to remove low resolution options so that popup fits
        # display since they would look bad anyway.
        del resolutions[:17:-1]
        resolutions_str = [
            f"{resolution[0]}, {resolution[1]}" for resolution in resolutions
        ]
        # if update_dropdown:
        #     if non_int_scaling:
        #         for resolution in resolutions_str:
        #             if not any(resolution == button.text for button in self.resolution_dropdown.option_button_arr.buttons):
        #     else:
        #         for button in (buttons := self.resolution_dropdown.option_button_arr.buttons):
        #             if not any(button.text == resolution for resolution in resolutions_str):
        #                 buttons.pop(button)
        return resolutions, resolutions_str


class KeybindsOptions(OptionsOverlay):
    def __init__(self):
        super().__init__()
        self.text_arr_arr = []
        for i, keybind_items in enumerate(keybinds):
            config_ = TextArrayConfig(
                (
                    tuple(f"{items[0]}:" for items in keybind_items[1]), ()
                ),
                wrap_width=self.row_width * (i + 1) - self.padding,
            )
            text_arr = TextArray(
                (self.text_pos[0] + self.row_width * 2 * i, self.text_pos[1]),
                (len(config_.text[0]), 1),
                self.padding,
                config=config_
            )
            self.text_arr_arr.append(text_arr)
        self.widgets = (text_arr for text_arr in self.text_arr_arr)


class AudioOptions(OptionsOverlay):
    def __init__(self):
        super().__init__()
