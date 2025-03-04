from typing import Literal

import pygame

_Colors = tuple[tuple | pygame.Color] | tuple | pygame.Color | None
_Align = tuple[Literal["left", "right"] | None, Literal["top", "bottom"] | None]
_Images = tuple[pygame.Surface] | pygame.Surface | str
