import random
from typing import override

import pygame

from data.utils import graphics
from . import State
from ..components.ui import widgethandler
from ..components.ui.button import ButtonImage


class Title(State):
    def __init__(self):
        super().__init__()
        self.background = graphics('menu')
        self.logo = pygame.transform.scale_by(graphics('logo'), 5)
        self.splashes = [
            pygame.transform.scale_by(graphics('gun die'), 5),
            pygame.transform.scale_by(graphics('can we get more christof'), 5),
            pygame.transform.scale_by(graphics('tiferet'), 5),
        ]
        self.splash = random.choice(self.splashes)
        self.play = ButtonImage(
            self._screen, pygame.Rect(self._screen_size[0]*0.6,
                                      self._screen_size[1]*0.35, 0, 0),
            tuple(pygame.transform.scale_by(images, 3)
                  for images in graphics('play').values()))
        self.editor = ButtonImage(
            self._screen, pygame.Rect(self._screen_size[0]*0.6,
                                      self._screen_size[1]*0.475, 0, 0),
            tuple(pygame.transform.scale_by(images, 3)
                  for images in graphics('editor').values())
        )
        self.options = ButtonImage(
            self._screen, pygame.Rect(self._screen_size[0]*0.6,
                                      self._screen_size[1]*0.6, 0, 0),
            tuple(pygame.transform.scale_by(images, 3)
                  for images in graphics('options').values()),
            on_click=lambda: self.state_manager.append("options"))
        self.quit = ButtonImage(
            self._screen, pygame.Rect(self._screen_size[0]*0.6,
                                      self._screen_size[1]*0.725, 0, 0),
            tuple(pygame.transform.scale_by(images, 3)
                  for images in graphics('quit').values()),
            on_click=self.state_manager.quit)
        for widget in [self.play, self.editor, self.options, self.quit]:
            widgethandler.WidgetHandler.add_widget(widget)

    @override
    def update_screen(self):
        widgethandler.WidgetHandler.update_screen(self._screen)

    @override
    def startup(self):
        super().startup()
        self.input_binder.register(('keydown', pygame.K_LEFT),
                               action=lambda: self.switch_splash(-1))
        self.input_binder.register(('keydown', pygame.K_RIGHT),
                               action=lambda: self.switch_splash(1))

    @override
    def cleanup(self):
        super().cleanup()
        self.input_binder.deregister(('keydown', pygame.K_LEFT))
        self.input_binder.deregister(('keydown', pygame.K_RIGHT))

    @override
    def render(self):
        super().render()
        widgethandler.WidgetHandler.blit()
        self._screen.blit(self.logo,
                         (self._screen_size[0] / 2 - self.logo.get_width() / 2,
                          self._screen_size[1] * 0.1))
        self._screen.blit(self.splash,
                          (self._screen_size[0]/2-self.splash.get_width(),
                           self._screen_size[1]*0.275))

    @override
    def update(self):
        widgethandler.WidgetHandler.update()

    def switch_splash(self, direction):
        try:
            self.splash = self.splashes[self.splashes.index(self.splash) +
                                        direction]
        except IndexError:
            self.splash = self.splashes[0]

    @override
    def back(self):
        self.state_manager.append('options')