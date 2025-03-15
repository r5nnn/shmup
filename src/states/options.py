"""Options screen."""

from typing import override

import pygame

from src.components.managers import overlaymanager
from src.components.ui import (
    widgethandler,
    ToggleArrayGroup,
    TextRectToggleButtonArray,
    TextRectToggleButtonArrayConfig,
)
from src.core.constants import PRIMARY
from src.core.load import Load
from src.states.optionmenus import (
    GeneralOptions,
    GraphicsOptions,
    KeybindsOptions,
    AudioOptions,
)
from src.states.state import State, Overlay
from src.core.data import system_data


class Options(State):
    def __init__(self):
        super().__init__()
        # images
        self.title = pygame.transform.scale_by(
            pygame.image.load(Load("image").path["title options"]), 4
        )
        # background rect
        self.bg_rect = pygame.Rect(
            0,
            0,
            system_data.abs_window_rect.width * 0.8,
            (system_data.abs_window_rect.height - self.title.get_height()) * 0.8,
        )
        self.bg_rect.midtop = (
            system_data.abs_window_rect.centerx,
            system_data.abs_window_rect.height * 0.1 + 20 + self.title.get_height(),
        )
        self.bg_surf = pygame.Surface(self.bg_rect.size)
        self.bg_surf.fill(PRIMARY)
        self.bg_surf.set_alpha(96)
        self.active_overlay = None
        self.padding = 30
        config = TextRectToggleButtonArrayConfig(
            sizes=(round(self.bg_rect.width / 4), 30),
            texts=(("General",), ("Graphics",), ("Keybinds",), ("Audio",)),
            on_toggle_on=(
                (lambda: self.switch_overlay(GeneralOptions),),
                (lambda: self.switch_overlay(GraphicsOptions),),
                (lambda: self.switch_overlay(KeybindsOptions),),
                (lambda: self.switch_overlay(AudioOptions),),
            ),
        )
        self.option_headings_group = ToggleArrayGroup(
            TextRectToggleButtonArray(self.bg_rect.topleft, (1, 4), 0, config),
            toggle_on_init=False,
        )
        self.widgets = (self.option_headings_group,)

    @override
    def render(self) -> None:
        system_data.abs_window.blit(self.background, (0, 0))
        system_data.abs_window.blit(self.bg_surf, self.bg_rect)
        system_data.abs_window.blit(
            self.title,
            (
                system_data.abs_window_rect.width / 2 - self.title.get_width() / 2,
                system_data.abs_window_rect.height * 0.1,
            ),
        )
        widgethandler.blit()

    @override
    def startup(self) -> None:
        super().startup()
        self.option_headings_group.toggle_start_button()

    @override
    def cleanup(self) -> None:
        super().cleanup()
        overlaymanager.remove(self.active_overlay)

    def switch_overlay(self, overlay: type[Overlay]) -> None:
        if self.active_overlay is not None:
            overlaymanager.remove(self.active_overlay)
        overlaymanager.append(overlay)
        self.active_overlay = overlay
