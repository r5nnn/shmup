from __future__ import annotations

from typing import Literal

import pygame

from src.components.ui.buttons import (
    TextToggleButton, TextClickButton, TextRectToggleButton,
    TextRectClickButton, ImageClickButton, ImageToggleButton,
    ImageRectToggleButton, ImageRectClickButton)

_Colors = list[tuple | pygame.Color] | tuple | pygame.Color | None
_Align = list[Literal["top", "bottom", "mid", "left", "right"]] | str
_Images = tuple[pygame.Surface, ...] | pygame.Surface | str
_AnyButton = (TextToggleButton | TextClickButton | TextRectToggleButton
            | TextRectClickButton | ImageClickButton | ImageToggleButton
            | ImageRectClickButton | ImageRectToggleButton)
