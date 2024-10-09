import random
from typing import override

import pygame

from data.core.prepare import image_paths, audio_paths, sprites
from .state import State
from ..components.audio import background_audio, button_audio
from ..components.ui import widgethandler
from ..components.ui.button import ImageButton, ImageButtonConfig


class Title(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load(image_paths('menu')).convert()
        self.logo = pygame.transform.scale_by(pygame.image.load(image_paths('logo')), 4)
        self.splashes = [pygame.transform.scale_by(pygame.image.load(image_paths('gun die')).convert(), 5),
                         pygame.transform.scale_by(pygame.image.load(image_paths('can we get more christof')).convert(),
                                                   5),
                         pygame.transform.scale_by(pygame.image.load(image_paths('tiferet')).convert(), 5)]
        self.splash = random.choice(self.splashes)

        background_audio.add_audio(audio_paths('menuloop rmx'))

        play_config = ImageButtonConfig(
            position=(self._screen_size[0] * 0.6, self._screen_size[1] * 0.35),
            size=(0, 0), images=tuple(pygame.transform.scale_by(images, 3)
                                      for images in sprites('play').values()))
        self.play = ImageButton(play_config)
        editor_config = ImageButtonConfig(
            position=(self._screen_size[0] * 0.6, self._screen_size[1] * 0.475),
            size=(0, 0), images=tuple(pygame.transform.scale_by(images, 3)
                                      for images in sprites('editor').values()))
        self.editor = ImageButton(editor_config)
        options_config = ImageButtonConfig(
            position=(self._screen_size[0] * 0.6, self._screen_size[1] * 0.6),
            size=(0, 0), images=tuple(pygame.transform.scale_by(images, 3)
                                      for images in sprites('options').values()),
            on_click=lambda: self.state_manager.append("options"))
        self.options = ImageButton(options_config)

        quit_config = ImageButtonConfig(
            position=(self._screen_size[0] * 0.6, self._screen_size[1] * 0.725),
            size=(0, 0), images=tuple(pygame.transform.scale_by(images, 3)
                                      for images in sprites('quit').values()),
            on_click=self.state_manager.quit)
        self.quit = ImageButton(quit_config)

        for widget in [self.play, self.editor, self.options, self.quit]:
            widgethandler.add_widget(widget)

    @override
    def update_screen(self):
        widgethandler.update_screen(self._screen)

    @override
    def startup(self):
        super().startup()
        self.input_binder.register(('keydown', pygame.K_LEFT), action=lambda: self.switch_splash(-1))
        self.input_binder.register(('keydown', pygame.K_RIGHT), action=lambda: self.switch_splash(1))

        background_audio.play_audio('menuloop rmx', loops=-1)

    @override
    def cleanup(self):
        super().cleanup()
        self.input_binder.deregister(('keydown', pygame.K_LEFT))
        self.input_binder.deregister(('keydown', pygame.K_RIGHT))
        # if button is unrendered before the keyup event triggers,
        # clicked must be manually reset
        self.options.clicked = False

    @override
    def render(self):
        super().render()
        widgethandler.blit()
        self._screen.blit(self.logo, (self._screen_size[0] / 2 - self.logo.get_width() / 2, self._screen_size[1] * 0.1))
        self._screen.blit(self.splash,
                          (self._screen_size[0] / 2 - self.splash.get_width(), self._screen_size[1] * 0.275))

    @override
    def update(self):
        widgethandler.update()

    def switch_splash(self, direction):
        try:
            self.splash = self.splashes[self.splashes.index(self.splash) + direction]
        except IndexError:
            self.splash = self.splashes[0]

    @override
    def back(self):
        button_audio.play_audio('click', override=True)
        self.state_manager.append('options')
