from typing import Literal

import pygame

_Colors = list[tuple | pygame.Color] | tuple | pygame.Color | None
_Align = list[Literal["top", "bottom", "mid", "left", "right"]]
_Images = tuple[pygame.Surface, ...] | pygame.Surface | str
