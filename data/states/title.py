import random
from typing import override

import pygame

from data.components import InputBinder
from data.components.audio import background_audio, button_audio
from data.components.ui import widgethandler, button_from_images
from data.core import screen, screen_size
from data.core.prepare import image_paths, audio_paths
from data.states.state import State


class Title(State):
    def __init__(self):
        super().__init__()

        # images
        self.background = pygame.image.load(image_paths('menu')).convert()
        self.logo = pygame.transform.scale_by(
            pygame.image.load(image_paths('logo')), 4)
        self.splashes = tuple(pygame.transform.scale_by(
            pygame.image.load(image_paths(name)).convert(), 5) for name in
            ('gun die', 'can we get more christof', 'tiferet'))
        self.splash = random.choice(self.splashes)

        # audio
        background_audio.add_audio(audio_paths('menuloop rmx'))

        # buttons
        self.play = button_from_images(
            'play', (screen_size[0] * 0.6, screen_size[1] * 0.35),
            lambda: self.state_manager.append('game'))
        self.editor = button_from_images(
            'editor', (screen_size[0] * 0.6, screen_size[1] * 0.475))
        self.options = button_from_images(
            'options', (screen_size[0] * 0.6, screen_size[1] * 0.6),
            lambda: self.state_manager.append('options'))
        self.quit = button_from_images(
            'quit', (screen_size[0] * 0.6, screen_size[1] * 0.725),
            self.state_manager.quit)
        self.widgets = (self.play, self.editor, self.options, self.quit)


    @override
    def startup(self):
        super().startup()
        InputBinder.register(('keydown', pygame.K_LEFT),
                             action=lambda: self.switch_splash(-1))
        InputBinder.register(('keydown', pygame.K_RIGHT),
                             action=lambda: self.switch_splash(1))
        background_audio.play_audio('menuloop rmx', loops=-1)

    @override
    def cleanup(self):
        super().cleanup()
        InputBinder.deregister(('keydown', pygame.K_LEFT))
        InputBinder.deregister(('keydown', pygame.K_RIGHT))

    @override
    def render(self):
        super().render()
        widgethandler.blit()
        screen.blit(self.logo,
                    (screen_size[0] / 2 - self.logo.get_width() / 2,
                     screen_size[1] * 0.1))
        screen.blit(self.splash,
                    (screen_size[0] / 2 - self.splash.get_width(),
                     screen_size[1] * 0.275))

    def switch_splash(self, direction):
        try:
            self.splash = self.splashes[
                self.splashes.index(self.splash) + direction]
        except IndexError:
            self.splash = self.splashes[0]

    @override
    def back(self):
        button_audio.play_audio('click', override=True)
        self.state_manager.append('options')
