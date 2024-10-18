from typing import Type, Optional, override

import pygame

from data.components.ui import ButtonBase, Text
from data.components.ui.widgetutils import WidgetBase
from data.core import CustomTypes
from data.core.utils import Popups


class Popup(WidgetBase):
    def __init__(self, size: tuple[int, int], position: tuple[int, int] = None,
                 align: CustomTypes.rect_alignments = 'center',
                 text: str = "",
                 text_color: pygame.Color | tuple = pygame.Color("white"),
                 font: Optional[pygame.font.Font] = None, font_size: int = 32,
                 padding: int = 10,
                 *buttons: ButtonBase,
                 popup_type: Popups = 0,
                 surface: pygame.Surface = pygame.display.get_surface()):
        position = tuple(int(coord/2) for coord in pygame.display.get_surface().get_size())
        super().__init__(position, align, surface)
        self._width, self._height = size
        self._popup_type = popup_type
        self._buttons = buttons
        total_button_width, total_button_height = 0, 0
        for button in self._buttons:
            total_button_width += button.width
            total_button_height += button.height
        if total_button_width >= self._width:
            raise ValueError(f"Total width of buttons ({total_button_width}) "
                             f"is more than width of popup given ({self._width})")
        if total_button_height >= self._height:
            raise ValueError(f"Total height of buttons ({total_button_height}) "
                             f"is more than height of popup given ({self._height})")
        self.rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._align_rect(self.rect, self.align, (self._x, self._y))
        self._text = Text((self.rect.centerx, 0),
                          text, font, font_size, color=text_color, align='midtop')
        self.padding = padding

    def _align_rect(self, rect, align, coords):
        setattr(rect, align, coords)
        self._x, self._y = getattr(rect, align)

    def _align_popup(self, buttons: tuple[ButtonBase], rect: pygame.Rect):
        num_of_buttons = len(buttons)
        left = rect.left
        for index, button in enumerate(buttons):
            padding = (rect.width - num_of_buttons * button.width) / num_of_buttons + 1
            button.x = left + padding * index
            left = button.x + button.width
            button.y = self.rect.centery - self.padding

    @override
    def update(self) -> None:
        ...

    @override
    def blit(self) -> None:
        ...
