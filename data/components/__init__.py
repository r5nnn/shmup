"""Package containing components that help run the game."""
from typing import Literal

RectAlignments = Literal[
    "topleft", "midtop", "topright",
    "midleft", "center", "midright",
    "bottomleft", "midbottom", "bottomright"]

from data.components.audio import Audio, background_audio, button_audio
from data.components.colors import shift_rgb, ColorGradient
from data.components.input import InputBinder
