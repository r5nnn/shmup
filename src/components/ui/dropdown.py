from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from src.components.ui.buttons import TextButton, TextButtonConfig
from src.components.ui.widgetutils import WidgetBase
from src.core.constants import PRIMARY, SECONDARY, ACCENT

if TYPE_CHECKING:
    from src.components import RectAlignments


class Dropdown(WidgetBase):
    def __init__(self, position: tuple[int, int], size: tuple[int, int],
                 colors: tuple[tuple | pygame.Color] = (PRIMARY, SECONDARY,ACCENT),
                 *choices: str, start_choice: int | str | None,
                 align: RectAlignments = "topleft"):
        super().__init__(position, align)
        self._chosen = None
        self._dropped = False
        # head_config = TextButtonConfig(position=position, size=size, align=align,
        #                                colors=colors, text=choices[0 if start_choice is])
