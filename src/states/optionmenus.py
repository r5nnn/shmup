import pygame

from src.components.ui import Text, ToggleableTextButtonConfig, ToggleableTextButton
from src.core import toggle_fullscreen
from src.core.constants import PRIMARY, SECONDARY, ACCENT
from src.core.utils import toggle_flag
from src.states.state import Overlay
from src.core.data import config


class GraphicsOptions(Overlay):
    def __init__(self):
        super().__init__()
        self.fullscreen_text = Text(
            (self.current_state.bg_rect.left + self.current_state.padding,
             self.current_state.bg_rect.top + self.current_state.graphics.height +
             self.current_state.padding),
            text="Fullscreen:")
        fullscreen_graphics_config = ToggleableTextButtonConfig(
            position=(self.fullscreen_text.rect.right +
                      self.current_state.padding,
                      self.fullscreen_text.rect.centery),
            size=(200, 30), colors=(PRIMARY, SECONDARY, ACCENT),
            text=("True", "False"), start_text=0 if config["flags"]["fullscreen"] else 1,
            align="midleft",
            on_toggle=toggle_fullscreen)
        self.fullscreen_button = ToggleableTextButton(fullscreen_graphics_config)
        self.borderless_text = Text(
            (self.current_state.bg_rect.left + self.current_state.padding,
             self.fullscreen_text.rect.bottom + self.current_state.padding),
            text="Borderless:")
        borderless_graphics_config = ToggleableTextButtonConfig(
            position=(self.borderless_text.rect.right +
                      self.current_state.padding,
                      self.borderless_text.rect.centery),
            size=(200, 30), colors=(PRIMARY, SECONDARY, ACCENT),
            text=("True", "False"), start_text=0 if config["flags"]["noframe"] else 1,
            align="midleft", on_toggle=lambda: toggle_flag(flag=pygame.NOFRAME))
        self.borderless_button = ToggleableTextButton(borderless_graphics_config)
        self.widgets = (self.fullscreen_text, self.fullscreen_button,
                        self.borderless_text, self.borderless_button)

    def render(self) -> None:
        super().render()

    def update(self, *args) -> None:
        if config["flags"]["fullscreen"]:
            self.fullscreen_button.toggle_on()
        else:
            self.fullscreen_button.toggle_off()
        if config["flags"]["noframe"]:
            self.borderless_button.toggle_on()
        else:
            self.borderless_button.toggle_off()


class KeybindsOptions(Overlay):
    def __init__(self):
        super().__init__()


class AudioOptions(Overlay):
    def __init__(self):
        super().__init__()
