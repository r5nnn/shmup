from dataclasses import dataclass
from typing import Optional, override
import pygame
from pygame import freetype
from data.components import RectAlignments
from data.components.ui import ButtonBase, Text
from data.components.ui.widgetutils import WidgetBase
from data.core import screen
from data.core.prepare import screen_center
from data.core.utils import Popups, ColorPalette


@dataclass(kw_only=True)
class PopupConfig:
    position: tuple[int, int] = None
    size: tuple[int, int]
    align: RectAlignments = 'center'
    color: Optional[pygame.Color | tuple] = None
    text: str = ''
    text_color: Optional[pygame.Color | tuple] = None
    font: Optional[pygame.freetype.Font] = None
    font_size: int = 32
    buttons: tuple[ButtonBase, ...] = ()
    padding: int = 0
    popup_type: Popups = 0


class Popup(WidgetBase):
    def __init__(self, config: PopupConfig):
        position = screen_center if config.position is None else config.position
        super().__init__(position, config.align)
        self._width, self._height = config.size
        self._color = config.color or ColorPalette.PRIMARY
        self._rect = pygame.Rect(0, 0, self._width, self._height)
        self._align_rect(self._rect, self.align, (self._x, self._y))
        self._text = None
        if config.text:
            self._text = Text(
                (self._rect.centerx, (self._rect.top + int(self._height * 0.2)) \
                    if config.buttons else self._rect.centery),
                config.text, config.font, config.font_size,
                config.text_color if config.text_color is True else \
                    pygame.Color('white'),
                'midtop' if config.buttons else 'center',
                sub_widget=True)

        # Buttons setup
        self._buttons = config.buttons
        if self._buttons:
            self._align_buttons(self._buttons, self._rect, config.padding)

    def _align_rect(self, rect, align, coords):
        setattr(rect, align, coords)
        self._x, self._y = getattr(rect, align)

    def _align_buttons(self, buttons: tuple[ButtonBase, ...], rect: pygame.Rect, padding: int):
        # Calculate button positioning based on rect
        total_button_width = sum(button.width for button in buttons)
        gaps = len(buttons) + 1
        button_padding_x = round((rect.width - total_button_width) / gaps)

        # Position each button within the rect
        y_position = rect.centery if not self._text else rect.bottom - int(self._height * 0.1)
        print(y_position, rect.bottom)
        left = rect.left + button_padding_x
        for button in buttons:
            button.align = 'bottomleft' if self._text else 'midleft'
            button.x = left
            button.y = y_position
            left += button.width + button_padding_x

    @override
    def update(self):
        if self._text:
            self._text.update()
        for button in self._buttons:
            button.update()

    @override
    def blit(self):
        # Draw background
        pygame.draw.rect(screen, self._color, self._rect)

        # Draw text if available
        if self._text:
            self._text.blit()

        # Draw each button
        for button in self._buttons:
            button.blit()
