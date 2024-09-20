import os

import pygame

from .. import tools
from ..components.ui import widgethandler
from ..components.ui.button import Button
from ..globals import BACKGROUNDS, SCREEN_SIZE
from ..components import pygame_shaders


class Title(tools.State):
    def __init__(self):
        super().__init__()
        self.background = BACKGROUNDS()['menu']
        self.button = Button(self.display,
                             pygame.Rect(*(i/2 for i in SCREEN_SIZE), 200, 100),
                             align='center', text='bnrosjdfgsldfgkj', radius=10)
        widgethandler.WidgetHandler.add_widget(self.button)
        self.shader = pygame_shaders.Shader(
            pygame_shaders.DEFAULT_VERTEX_SHADER,
            os.path.join("data", "states", "frag.glsl"), self.display)

    def render(self):
        super().render()
        widgethandler.WidgetHandler.blit()
        pygame.draw.rect(self.display, (255, 0, 0), (200, 200, 20, 20))
        self.shader.render_direct(pygame.Rect(0, 0, 600, 600))

    def update(self):
        widgethandler.WidgetHandler.update()