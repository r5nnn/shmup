import pygame

from src.components.ui import ToggleGroup, widgethandler, \
    ToggleableTextButton, ToggleableTextButtonConfig, Text
from src.core.constants import PRIMARY, SECONDARY, ACCENT
from src.core.prepare import image_paths, screen, screen_size, screen_center
from src.states.state import State
from src.states.optionmenus import GraphicsOptions, KeybindsOptions, AudioOptions


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
        self.bg_surf.fill(PRIMARY)
        self.bg_surf.set_alpha(96)
        self.current_option = None
        config = ToggleableTextButtonConfig(
            position=self.bg_rect.topleft,
            size=(round(self.bg_rect.width / 3), 30),
            colors=(PRIMARY, SECONDARY, ACCENT),
            text="Graphics", on_toggle_on=lambda: self.switch_overlay(GraphicsOptions))
        self.graphics = ToggleableTextButton(config)
        config.position = self.graphics.rect.topright
        config.text = "Keybinds"
        config.on_toggle_on = lambda: self.switch_overlay(KeybindsOptions)
        self.keybinds = ToggleableTextButton(config)
        config.position = self.keybinds.rect.topright
        config.text = "Audio"
        config.on_toggle_on = lambda: self.switch_overlay(AudioOptions)
        self.audio = ToggleableTextButton(config)
        self.active_overlay = None
        self.padding = 20

    def update(self):
        super().update()

    def render(self):
        screen.blit(self.background, (0, 0))
        screen.blit(self.bg_surf, self.bg_rect)
        screen.blit(self.title,
                    (screen_size[0] / 2 - self.title.get_width() / 2,
                     screen_size[1] * 0.1))
        widgethandler.blit()

    def startup(self):
        self.options = ToggleGroup(self.graphics, self.audio, self.keybinds)
        self.widgets = (self.options,)
        super().startup()

    def cleanup(self):
        super().cleanup()
        self.overlay_manager.remove(self.active_overlay)

    def switch_overlay(self, cls: type):
        self.overlay_manager.remove(self.active_overlay) if self.active_overlay is not None else None
        self.overlay_manager.append(cls)
        self.active_overlay = cls
