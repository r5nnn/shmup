import pygame

from src.components.ui import Text, ToggleableTextButtonConfig, ToggleableTextButton
from src.core import toggle_fullscreen
from src.core.constants import PRIMARY, SECONDARY, ACCENT
from src.core.utils import toggle_flag
from src.states.state import Overlay
from src.core.data import config
from src.components.manager import statemanager


class GraphicsOptions(Overlay):
    def __init__(self):
        super().__init__()
        self.fullscreen_text = Text(
            (statemanager.current_state().bg_rect.left +
             statemanager.current_state().padding,
             statemanager.current_state().bg_rect.top +
             statemanager.current_state().graphics.height +
             statemanager.current_state().padding),
            text="Fullscreen:")
        fullscreen_config = ToggleableTextButtonConfig(
            position=(self.fullscreen_text.rect.right +
                      statemanager.current_state().padding,
                      self.fullscreen_text.rect.centery),
            size=(200, 30), colors=(PRIMARY, SECONDARY, ACCENT),
            text=("True", "False"),
            start_text=0 if config["flags"]["fullscreen"] else 1,
            align="midleft", on_toggle=toggle_fullscreen)
        self.fullscreen_button = ToggleableTextButton(fullscreen_config)
        self.borderless_text = Text(
            (statemanager.current_state().bg_rect.left + statemanager.current_state().padding,
             self.fullscreen_text.rect.bottom + statemanager.current_state().padding),
            text="Borderless:")
        borderless_config = ToggleableTextButtonConfig(
            position=(self.borderless_text.rect.right +
                      statemanager.current_state().padding,
                      self.borderless_text.rect.centery),
            size=(200, 30), colors=(PRIMARY, SECONDARY, ACCENT),
            text=("True", "False"),
            start_text=0 if config["flags"]["noframe"] else 1, align="midleft",
            on_toggle=lambda: toggle_flag(flag=pygame.NOFRAME))
        self.borderless_button = ToggleableTextButton(borderless_config)
        self.resolution_text = Text(
            (statemanager.current_state().bg_rect.left + statemanager.current_state().padding,
             self.borderless_text.rect.bottom + statemanager.current_state().padding),
            text="Resolution:")
        self.widgets = (self.fullscreen_text, self.fullscreen_button,
                        self.borderless_text, self.borderless_button,
                        self.resolution_text)

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
