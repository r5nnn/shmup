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
from src.components.ui.buttons import ToggleArrayGroup
from src.components.ui.buttons import (TextRectToggleButtonArray,
                                       TextRectToggleButtonArrayConfig)


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
        self.active_overlay = None
        self.padding = 20
        config = TextRectToggleButtonArrayConfig(
            (round(self.bg_rect.width / 3), 30), texts=
            (("Graphics", ), ("Keybinds",), ("Audio",)),
            on_toggle_on=((lambda: self.switch_overlay(GraphicsOptions),),
                          (lambda: self.switch_overlay(KeybindsOptions),),
                          (lambda: self.switch_overlay(AudioOptions),)))
        self.option_headings_group = ToggleArrayGroup(
            TextRectToggleButtonArray(self.bg_rect.topleft, (1, 3), 0, config),
            toggle_on_init=False)
        self.widgets = (self.option_headings_group,)

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
        super().startup()
        self.option_headings_group.toggle_start_button()

    @override
    def cleanup(self) -> None:
        super().cleanup()
        overlaymanager.remove(self.active_overlay)

    def switch_overlay(self, overlay: type[Overlay]) -> None:
        if self.active_overlay is not None:
            overlaymanager.remove(self.active_overlay)
        overlaymanager.append(overlay)
        self.active_overlay = overlay
