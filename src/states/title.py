"""Title state."""

import random
from typing import override

import pygame

from src.components import Audio
from src.components.managers import statemanager
from src.components.ui import widgethandler
from src.components.ui.buttons import (
    ImageClickButtonArray,
    ImageClickButtonArrayConfig,
)
from src.core.data import system_data
from src.core.load import Load
from src.states.state import State


class Title(State):
    def __init__(self):
        super().__init__()
        # images
        self.background = pygame.image.load(Load("image").path["menu"]).convert()
        self.title = pygame.transform.scale_by(
            pygame.image.load(Load("image").path["title main"]), 4
        )
        self.splash = pygame.transform.scale_by(
            pygame.image.load(
                Load("image").path[random.choice(("gun die", "tiferet"))]
            ).convert(),
            5,
        )

        config = ImageClickButtonArrayConfig(
            images=(("play", "editor", "options", "quit"),),
            scale_by=3,
            image_masks=False,
            on_click=(
                (
                    lambda: statemanager.append("game"),
                    None,
                    lambda: statemanager.append("options"),
                    statemanager.quit_game,
                ),
            ),
            align="midtop",
        )
        self.title_buttons = ImageClickButtonArray(
            (
                round(system_data.abs_window_rect.width * 0.65),
                round(system_data.abs_window_rect.height * 0.3),
            ),
            (4, 1),
            0,
            config,
        )
        self.widgets = (self.title_buttons,)

    @override
    def startup(self) -> None:
        super().startup()
        Audio(channel_name="bgm").play_audio("menuloop rmx", loops=-1)

    @override
    def cleanup(self) -> None:
        super().cleanup()

    @override
    def render(self) -> None:
        super().render()
        widgethandler.blit()
        system_data.abs_window.blit(
            self.title,
            (
                system_data.abs_window_rect.width * 0.5
                - self.title.get_width() / 2,
                system_data.abs_window_rect.height * 0.1,
            ),
        )
        system_data.abs_window.blit(
            self.splash,
            (
                system_data.abs_window_rect.width * 0.03,
                system_data.abs_window_rect.height * 0.25,
            ),
        )

    @override
    def back(self) -> None:
        statemanager.append("options")
