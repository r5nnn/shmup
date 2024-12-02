import pygame

from data.components.ui import ToggleGroup, widgethandler, \
    ToggleableTextButton, ToggleableTextButtonConfig
from data.core import Colors
from data.core.prepare import image_paths, screen, screen_size, screen_center
from data.states.state import State


class Options(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load(image_paths("menu")).convert()
        self.title = pygame.transform.scale_by(
            pygame.image.load(image_paths("title options")), 4)
        self.bg_rect = pygame.Rect(0, screen_size[1] * 0.1 + 20 + self.title.get_height(),
                                   screen_size[0] * 0.8, (screen_size[1] - self.title.get_height()) * 0.8)
        self.bg_rect.centerx = screen_center[0]
        self.bg_surf = pygame.Surface(self.bg_rect.size)
        self.bg_surf.fill(Colors.PRIMARY)
        self.bg_surf.set_alpha(96)
        self.current_option = None
        config = ToggleableTextButtonConfig(position=self.bg_rect.topleft,
                                            size=(round(self.bg_rect.width / 3), 30),
                                            colors=(Colors.PRIMARY,
                                                    Colors.SECONDARY,
                                                    Colors.ACCENT),
                                            text="Graphics")
        self.graphics = ToggleableTextButton(config)
        config.position = self.graphics.rect.topright
        config.text = "Keybinds"
        self.keybinds = ToggleableTextButton(config)
        config.position = self.keybinds.rect.topright
        config.text = "Audio"
        self.audio = ToggleableTextButton(config)
        self.options = ToggleGroup(self.graphics, self.audio, self.keybinds)
        widgethandler.add_widget((self.graphics, self.audio, self.keybinds))

    def update(self):
        super().update()
        self.options.update()
        widgethandler.update()
        for index, option in enumerate((self.graphics, self.keybinds, self.audio)):
            if option.toggled:
                self.current_option = index

    def render(self):
        screen.blit(self.background, (0, 0))
        screen.blit(self.bg_surf, self.bg_rect)
        screen.blit(self.title,
                    (screen_size[0] / 2 - self.title.get_width() / 2,
                     screen_size[1] * 0.1))
        widgethandler.blit()
        match self.current_option:
            case 0:
                ...
            case 1:
                ...
            case 2:
                ...

    def startup(self):
        super().startup()

    def cleanup(self):
        super().cleanup()
