import pygame

from . import State
from ..components.ui import widgethandler
from ..components.ui.button import ButtonBase, ButtonImage, ButtonText
from data.utils import fonts, graphics


class Title(State):
    def __init__(self):
        super().__init__()
        self.background = graphics('menu')
        self.logo = pygame.transform.scale_by(graphics('logo'), 4)
        dimensions = (self._screen_size[0]*0.98-self.logo.get_width(),
                      self._screen_size[1]*0.1)
        self.surfaces.append([self.logo, dimensions])
        dimensions = (self._screen_size[0]*0.98-self.logo.get_width()/2-100/2,
                      self._screen_size[1]*0.1 + self.logo.get_height()*1.1)
        self.button = ButtonImage(
            self.screen, pygame.Rect(*dimensions, 100, 100),
            tuple(pygame.transform.scale_by(i, 3)
                  for i in graphics('play').values()))
        widgethandler.WidgetHandler.add_widget(self.button)
        widgethandler.WidgetHandler.move_to_bottom(self.button)

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