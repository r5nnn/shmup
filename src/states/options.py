"""Options screen."""
from typing import override

import pygame

from src.components.managers import overlaymanager
from src.components.ui import widgethandler
from src.core.constants import PRIMARY, SECONDARY, ACCENT
from src.core.prepare import image_paths, screen, screen_size, screen_center
from src.states.optionmenus import GraphicsOptions, KeybindsOptions, AudioOptions
from src.states.state import Overlay
from src.states.state import State


class Options(State):
    def __init__(self):
        super().__init__()
        # images
        self.background = pygame.image.load(image_paths("menu")).convert()
        self.title = pygame.transform.scale_by(pygame.image.load(
            image_paths("title options")), 4)
        # background rect
        self.bg_rect = pygame.Rect(
            0, 0, screen_size[0] * 0.8,
            (screen_size[1] - self.title.get_height()) * 0.8)
        self.bg_rect.midtop = (screen_center[0], screen_size[1] * 0.1 + 20 +
                                self.title.get_height())
        self.bg_surf = pygame.Surface(self.bg_rect.size)
        self.bg_surf.fill(PRIMARY)
        self.bg_surf.set_alpha(96)
        # buttons
        # config = ToggleableTextButtonConfig(
        #     position=self.bg_rect.topleft,
        #     size=(round(self.bg_rect.width / 3), 30),
        #     colors=(PRIMARY, SECONDARY, ACCENT),
        #     text="Graphics",
        #     on_toggle_on=lambda: self.switch_overlay(GraphicsOptions))
        # self.graphics = ToggleableTextButton(config)
        # config.position = self.graphics.rect.topright
        # config.text = "Keybinds"
        # config.on_toggle_on = lambda: self.switch_overlay(KeybindsOptions)
        # self.keybinds = ToggleableTextButton(config)
        # config.position = self.keybinds.rect.topright
        # config.text = "Audio"
        # config.on_toggle_on = lambda: self.switch_overlay(AudioOptions)
        # self.audio = ToggleableTextButton(config)

        # defined on startup
        self.options = None
        self.active_overlay = None
        self.padding = 20

    @override
    def render(self) -> None:
        screen.blit(self.background, (0, 0))
        screen.blit(self.bg_surf, self.bg_rect)
        screen.blit(self.title,
                    (screen_size[0] / 2 - self.title.get_width() / 2,
                     screen_size[1] * 0.1))
        widgethandler.blit()

    @override
    def startup(self) -> None:
        self.options = ToggleGroup(self.graphics, self.audio, self.keybinds)
        self.widgets = (self.options,)
        super().startup()

    @override
    def cleanup(self) -> None:
        super().cleanup()
        overlaymanager.remove(self.active_overlay)

    def switch_overlay(self, overlay: type[Overlay]) -> None:
        if self.active_overlay is not None:
            overlaymanager.remove(self.active_overlay)
        overlaymanager.append(overlay)
        self.active_overlay = overlay
