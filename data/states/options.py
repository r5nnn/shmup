import pygame

from data.components.ui import ToggleButton, TextButtonConfig, ToggleGroup, widgethandler
from data.core import Colors
from data.core.prepare import image_paths, screen, screen_size, screen_center
from data.states.state import State


class Options(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load(image_paths('menu')).convert()
        self.title = pygame.transform.scale_by(
            pygame.image.load(image_paths('title options')), 4)
        self.bg_rect = pygame.Rect(
            0, screen_size[1] * 0.1 + 20 + self.title.get_height(),
            screen_size[0] * 0.8, (screen_size[1] - self.title.get_height()) * 0.8)
        self.bg_rect.centerx = screen_center[0]
        self.bg_surf = pygame.Surface(self.bg_rect.size)
        self.bg_surf.fill(Colors.BACKGROUND)
        self.bg_surf.set_alpha(96)
        config = TextButtonConfig(position=self.bg_rect.topleft,
                                  size=(round(self.bg_rect.width / 3), 30),
                                  colors={'default': Colors.BACKGROUND,
                                          'hovered': Colors.FOREGROUND,
                                          'clicked': Colors.ACCENT},
                                  text='Graphics')
        self.graphics = ToggleButton(config)
        config.position = self.graphics.rect.topright
        config.text = 'Keybinds'
        self.keybinds = ToggleButton(config)
        config.position = self.keybinds.rect.topright
        config.text = 'Audio'
        self.audio = ToggleButton(config)
        self.options = ToggleGroup(self.keybinds, self.graphics, self.audio)

    def update(self):
        super().update()
        self.options.update()
        widgethandler.update()

    def render(self):
        screen.blit(self.background, (0, 0))
        screen.blit(self.bg_surf, self.bg_rect)
        screen.blit(self.title,
                    (screen_size[0] / 2 - self.title.get_width() / 2,
                     screen_size[1] * 0.1))
        self.graphics.blit()
        self.keybinds.blit()
        self.audio.blit()
        widgethandler.blit()

    def startup(self):
        super().startup()

    def cleanup(self):
        super().cleanup()