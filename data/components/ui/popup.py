import warnings
from dataclasses import dataclass
from typing import Optional, override

import pygame
from pygame import freetype

from data.components.ui import ButtonBase, Text
from data.components.ui.widgetutils import WidgetBase
from data.core.utils import Popups, CustomTypes, ColorPalette


@dataclass(kw_only=True)
class PopupConfig:
    position: tuple[int, int] = None
    size: tuple[int, int]
    align: CustomTypes.rect_alignments = 'center'
    color: Optional[pygame.Color | tuple] = None
    text: str = ''
    text_color: Optional[pygame.Color | tuple] = None
    font: Optional[pygame.freetype.Font] = None
    font_size: int = 32
    buttons: tuple[ButtonBase]
    padding: int = 10
    popup_type: Popups = 0
    surface: pygame.Surface = pygame.display.get_surface()


class Popup(WidgetBase):
    def __init__(self, config: PopupConfig):
        position = tuple(round(coord/2) for coord in
                         pygame.display.get_surface().get_size()) \
            if config.position is None else config.position
        super().__init__(position, config.align, config.surface)
        self._width, self._height = config.size
        self._color = config.color if config.color is not None else \
            ColorPalette.PRIMARY
        self._popup_type = config.popup_type
        self._buttons = config.buttons
        total_button_width, total_button_height = self._get_button_sizes()
        self._rect = pygame.Rect(0, 0, self._width, self._height)
        self._align_rect(self._rect, self.align, (self._x, self._y))
        self._text = Text(
            (self._rect.centerx, round(self._rect.top+self._rect.height/3)),
            config.text, config.font, config.font_size, 
            config.text_color if config.text_color is not None else \
                pygame.Color('white'),
            'midtop', sub_widget=True)
        self._text.x -= self._text.rect.height
        self.padding = config.padding

    def _get_button_sizes(self) -> tuple[int, int]:
        total_button_width, total_button_height = 0, 0
        for button in self._buttons:
            total_button_width += button.width
            total_button_height += button.height
            if not button.sub_widget:
                raise ValueError(f'Button passed: {button} is not a sub '
                                 f'widget. All buttons should be sub widgets.')
        if total_button_width >= self._width:
            raise ValueError(f"Total width of buttons ({total_button_width}) "
                             f"is more than width of popup given ({self._width})")
        if total_button_height >= self._height:
            raise ValueError(f"Total height of buttons ({total_button_height}) "
                             f"is more than height of popup given ({self._height})")
        return total_button_width, total_button_height

    def _align_rect(self, rect, align, coords):
        setattr(rect, align, coords)
        self._x, self._y = getattr(rect, align)

    def _align_buttons(self, buttons: tuple[ButtonBase], rect: pygame.Rect):
        num_of_buttons = len(buttons)
        left = rect.left
        for index, button in enumerate(buttons):
            padding = (rect.width - num_of_buttons * button.width) / num_of_buttons + 1
            button.x = left + padding * index
            left = button.x + button.width
            button.y = self._rect.bottom - round(self._rect.height/3) - button.height

    @override
    def update(self) -> None:
        self._text.update()
        for button in self._buttons:
            button.update()

    @override
    def blit(self) -> None:
        pygame.draw.rect(self._surface, self._color, self._rect)
        self._text.blit()
        for button in self._buttons:
            button.blit()

    @override
    def contains(self, x, y):
        return (self._x < x - self._surface.get_abs_offset()[0] < self._x + self._rect.width) and \
            (self._y < y - self._surface.get_abs_offset()[1] < self._y + self._rect.height)