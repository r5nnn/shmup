"""Title state."""
import random
from typing import override

import pygame
from pygame.transform import scale_by

from src.components.audio import background_audio
from src.components.events import eventbinder
from src.components.ui import widgethandler
from src.components.ui.buttons.textbuttonarray import TextToggleButtonArrayConfig
from src.core import screen, screen_size
from src.core.prepare import image_paths, audio_paths
from src.states.state import State
from src.components.managers import statemanager
from src.components.ui.buttons import ImageClickButton, ImageButtonConfig, \
    TextToggleButtonArray


class Title(State):
    def __init__(self):
        super().__init__()
        # images
        self.background = pygame.image.load(
            image_paths("menu")).convert()
        self.title = pygame.transform.scale_by(
            pygame.image.load(image_paths("title main")), 4)
        self.splashes = tuple(pygame.transform.scale_by(
            pygame.image.load(image_paths(name)).convert(), 4) for name in
            ("gun die", "can we get more christof", "tiferet"))
        self.splash = random.choice(self.splashes)

        # audio
        background_audio.add_audio(audio_paths("menuloop rmx"))
        config = ImageButtonConfig(
            position=(int(screen_size[0] * 0.5), screen_size[1] * 0.35), images="play",
            align="center", scale_by=3)
        self.play = ImageClickButton(config, image_mask=False)
        config = TextToggleButtonArrayConfig(((["1", "WHATTT"], "2"), ("3", "4")))
        self.arr = TextToggleButtonArray((int(screen_size[0] * 0.5), screen_size[1] * 0.5),
                                         (2, 2), 10, config)
        # # buttons
        # self.play = button_from_images(
        #     "play", (screen_size[0] * 0.6, screen_size[1] * 0.35),
        #     lambda: statemanager.append("game"))
        # self.editor = button_from_images(
        #     "editor", (screen_size[0] * 0.6, screen_size[1] * 0.475))
        # self.options = button_from_images(
        #     "options", (screen_size[0] * 0.6, screen_size[1] * 0.6),
        #     lambda: statemanager.append("options"))
        # self.quit = button_from_images(
        #     "quit", (screen_size[0] * 0.6, screen_size[1] * 0.725),
        #     statemanager.quit_game)
        # self.widgets = (self.play, self.editor, self.options, self.quit)
        self.widgets = (self.play, self.arr)

    @override
    def startup(self) -> None:
        super().startup()
        eventbinder.register(("keydown", pygame.K_LEFT),
                             action=lambda: self.switch_splash(-1))
        eventbinder.register(("keydown", pygame.K_RIGHT),
                             action=lambda: self.switch_splash(1))
        background_audio.play_audio("menuloop rmx", loops=-1)

    @override
    def cleanup(self) -> None:
        super().cleanup()
        eventbinder.deregister(("keydown", pygame.K_LEFT))
        eventbinder.deregister(("keydown", pygame.K_RIGHT))

    @override
    def render(self) -> None:
        super().render()
        widgethandler.blit()
        screen.blit(self.title,
                    (screen_size[0] / 2 - self.title.get_width() / 2,
                     screen_size[1] * 0.1))
        # screen.blit(self.splash,
        #             (screen_size[0] / 2 - self.splash.get_width(),
        #              screen_size[1] * 0.25))

    def switch_splash(self, direction: int) -> None:
        try:
            self.splash = self.splashes[
                self.splashes.index(self.splash) + direction]
        except IndexError:
            self.splash = self.splashes[0]

    @override
    def back(self) -> None:
        statemanager.append("options")
