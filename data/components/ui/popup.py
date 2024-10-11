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
        self._width, self._height = size
        self._popup_type = popup_type
        self._buttons = buttons
        for button in self._buttons:
            total_button_width += button.width
            total_button_height += button.height
        if total_button_width >= self._width:
            raise ValueError(f"Total width of buttons ({total_button_width}) is more"
                f" than width of popup given ({self._width})")
        if total_button_height >= self._height:
            raise ValueError(f"Total height of buttons ({total_button_height}) is more"
                f" than height of popup given ({self._height})")
        self.rect = pygame.Rect(self._x, self._y, self._width, self.height)

    def _align_popup(self):
        ...
