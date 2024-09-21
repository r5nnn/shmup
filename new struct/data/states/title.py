import pygame

from . import State
from ..components.ui import widgethandler
from ..components.ui.button import Button
from ..components.ui.text import Text
from data import graphics


class Title(State):
    def __init__(self):
        super().__init__()
        self.background = graphics()['menu']
        self.logo = pygame.transform.scale_by(graphics()['logo'], 4)
        dimensions = (self._screen_size[0]*0.98-self.logo.get_width(),
                      self._screen_size[1]*0.1)
        self.surfaces.append([self.logo, dimensions])
        dimensions = (self._screen_size[0]*0.98-300,
                      self._screen_size[1]*0.1 + self.logo.get_height())
        self.button = Button(self.screen, pygame.Rect(*dimensions, 300, 100),
                             text='Play', radius=10, font_size=64)
        widgethandler.WidgetHandler.add_widget(self.button)

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