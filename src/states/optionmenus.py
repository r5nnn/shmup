import pygame

from src.components.ui import Text, ToggleableTextButtonConfig, ToggleableTextButton
from src.core import toggle_fullscreen
from src.core.constants import PRIMARY, SECONDARY, ACCENT
from src.core.utils import toggle_flag
from src.states.state import Overlay


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
            text=("True", "False"), align="midleft",
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
            text=("True", "False"), align="midleft",
            on_toggle=lambda: toggle_flag(flag=pygame.NOFRAME))
        self.borderless_button = ToggleableTextButton(borderless_graphics_config)
        self.widgets = (self.fullscreen_text, self.fullscreen_button,
                        self.borderless_text, self.borderless_text)

    def render(self) -> None:
        super().render()


class KeybindsOptions(Overlay):
    def __init__(self):
        super().__init__()


class AudioOptions(Overlay):
    def __init__(self):
        super().__init__()