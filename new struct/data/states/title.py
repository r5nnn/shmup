import random

import pygame

from data.utils import graphics
from . import State
from ..components.ui import widgethandler
from ..components.ui.button import ButtonImage
from . import stateManager


class Title(State):
    def __init__(self):
        super().__init__()
        self.background = graphics('menu')
        self.logo = pygame.transform.scale_by(graphics('logo'), 5)
        self.splashes = [
            pygame.transform.scale_by(graphics('at the stake'), 5),
            pygame.transform.scale_by(graphics('can we get more christof'), 5),
            pygame.transform.scale_by(graphics('its real'), 5),
            pygame.transform.scale_by(graphics('tiferet'), 5),
        ]
        self.splash = random.choice(self.splashes)
        self.surfaces += [[self.logo,
                           (self._screen_size[0]/2-self.logo.get_width()/2,
                               self._screen_size[1]*0.1)],
                          [self.splash,
                           (self._screen_size[0]/2-self.splash.get_width(),
                            self._screen_size[1]*0.275)]]
        self.play = ButtonImage(
            self.screen, pygame.Rect(self._screen_size[0]*0.6,
                                     self._screen_size[1]*0.35, 0, 0),
            tuple(pygame.transform.scale_by(images, 3)
                  for images in graphics('play').values()))
        self.editor = ButtonImage(
            self.screen, pygame.Rect(self._screen_size[0]*0.6,
                                     self._screen_size[1]*0.475, 0, 0),
            tuple(pygame.transform.scale_by(images, 3)
                  for images in graphics('editor').values())
        )
        self.options = ButtonImage(
            self.screen, pygame.Rect(self._screen_size[0]*0.6,
                                     self._screen_size[1]*0.6, 0, 0),
            tuple(pygame.transform.scale_by(images, 3)
                  for images in graphics('options').values()))
        self.quit = ButtonImage(
            self.screen, pygame.Rect(self._screen_size[0]*0.6,
                                     self._screen_size[1]*0.725, 0, 0),
            tuple(pygame.transform.scale_by(images, 3)
                  for images in graphics('quit').values()), on_click=stateManager.quit)
        for widget in [self.play, self.editor, self.options, self.quit]:
            widgethandler.WidgetHandler.add_widget(widget)

    def update_screen(self):
        widgethandler.WidgetHandler.update_screen(pygame.display.get_surface())

    def startup(self):
        ...

    def cleanup(self):
        ...

    def render(self):
        super().render()
        widgethandler.WidgetHandler.blit()

    def update(self):
        widgethandler.WidgetHandler.update()
