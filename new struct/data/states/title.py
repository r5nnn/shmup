import os

import pygame

from .. import tools
from ..components.ui import widgethandler
from ..components.ui.button import Button
from ..globals import BACKGROUNDS, ICONS, screen_size


class Title(tools.State):
    def __init__(self):
        super().__init__()
        self.background = BACKGROUNDS()['menu']
        self.logo = pygame.transform.scale_by(ICONS()['logo'], 6)
        xy = (screen_size[0]*0.98-self.logo.get_width(), screen_size[1]*0.1)
        self.surfaces.append([self.logo, xy])
        self.button = Button(self.screen,
                             pygame.Rect(*(i/2 for i in screen_size),
                                         500, 125),
                             align='center', text='bnrosjdfgsldfgkj', radius=10, font_size=64)
        widgethandler.WidgetHandler.add_widget(self.button)

    def update_screen(self):
        self.button.surface = pygame.display.get_surface()

    def render(self):
        super().render()
        widgethandler.WidgetHandler.blit()

    def update(self):
        widgethandler.WidgetHandler.update()