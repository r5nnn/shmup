"""Title state."""

import random
from typing import override

import pygame

from src.components.audio import background_audio
from src.components.managers import statemanager
from src.components.ui import widgethandler
from src.components.ui.buttons import (
    ImageClickButtonArray,
    ImageClickButtonArrayConfig,
)
from src.core.prepare import image_paths, audio_paths
from src.core import system_data
from src.states.state import State


class Title(State):
    def __init__(self):
        super().__init__()
        # images
        self.background = pygame.image.load(image_paths("menu")).convert()
        self.title = pygame.transform.scale_by(
            pygame.image.load(image_paths("title main")), 4
        )
        self.splash = pygame.transform.scale_by(
            pygame.image.load(
                image_paths(random.choice(("gun die", "tiferet")))
            ).convert(),
            5,
        )

        # audio
        background_audio.add_audio(audio_paths("menuloop rmx"))
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
                system_data["window size"][0] * 0.65,
                system_data["window size"][1] * 0.3,
            ),
            (4, 1),
            0,
            config,
        )
        self.widgets = (self.title_buttons,)

    @override
    def startup(self) -> None:
        super().startup()
        background_audio.play_audio("menuloop rmx", loops=-1)

    @override
    def cleanup(self) -> None:
        super().cleanup()

    @override
    def render(self) -> None:
        super().render()
        widgethandler.blit()
        system_data["window"].blit(
            self.title,
            (
                system_data["window size"][0] * 0.5
                - self.title.get_width() / 2,
                system_data["window size"][1] * 0.1,
            ),
        )
        system_data["window"].blit(
            self.splash,
            (
                system_data["window size"][0] * 0.13,
                system_data["window size"][1] * 0.25,
            ),
        )

    @override
    def back(self) -> None:
        statemanager.append("options")
