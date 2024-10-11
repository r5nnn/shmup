from collections.abc import Callable
from typing import Type

import pygame

from data.components.ui import ButtonConfig, ButtonBase
from data.components.ui.widgetutils import WidgetBase
from data.core import CustomTypes
from data.core.utils import Popups


class Popup(WidgetBase):
    def __init__(self, position: tuple[int, int], size: tuple[int, int],
                 align: CustomTypes.rect_alignments,
                 text: str,
                 *buttons: Type[ButtonBase],
                 popup_type: Popups = 0,
                 surface: pygame.Surface = pygame.display.get_surface()):
        super().__init__(position, align, surface)
        self.size = size
        self.popup_type = popup_type