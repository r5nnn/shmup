"""Module holding all the game's custom types."""
from __future__ import annotations

from typing import Literal

import pygame

from src.components.ui.buttons import (
    TextToggleButton, TextClickButton, TextRectToggleButton,
    TextRectClickButton, ImageClickButton, ImageToggleButton,
    ImageRectToggleButton, ImageRectClickButton)
from src.states import Title, Options, Game

# Literals

RectAlignments = Literal[
    "topleft", "midtop", "topright",
    "midleft", "center", "midright",
    "bottomleft", "midbottom", "bottomright"]
TextRectAlignments = Literal["right", "left", "center", "justified"]
EventTypes = Literal[
    "key", "keydown", "keyup",
    "mouse", "mousedown", "mouseup",
    "quit",
]

# Commonly needed parameter types

Colors = list[tuple | pygame.Color] | tuple | pygame.Color | None
Align = list[Literal["top", "bottom", "left", "right"]] | Literal["center"]
Images = tuple[pygame.Surface, ...] | pygame.Surface | str

# Any

AnyButton = (TextToggleButton | TextClickButton | TextRectToggleButton
            | TextRectClickButton | ImageClickButton | ImageToggleButton
            | ImageRectClickButton | ImageRectToggleButton)
AnyState = Title | Options | Game
