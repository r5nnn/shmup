from __future__ import annotations

from dataclasses import dataclass
from typing import override

import pygame
from pygame import freetype

from data.components import RectAlignments, InputBinder
from data.components.ui import ButtonBase, Text, widgethandler
from data.components.ui.widgetutils import WidgetBase
from data.core import screen
from data.core.prepare import screen_center
from data.core.utils import Colors
from data.states.state import State


@dataclass(kw_only=True)
class PopupConfig:
    position: tuple[int, int] = None
    size: tuple[int, int]
    align: RectAlignments = "center"
    color: pygame.Color | tuple | None = None
    text: str = None
    text_color: pygame.Color | tuple | None = None
    font: pygame.freetype.Font | None = None
    font_size: int = 32
    buttons: tuple[ButtonBase, ...] = ()


class Popup(WidgetBase, State):
    def __init__(self, config: PopupConfig):
        position = config.position if config.position is not None else screen_center
        WidgetBase.__init__(self, position, config.align)
        State.__init__(self)

        self._width, self._height = config.size
        self._color = config.color if config.color is not None else \
            Colors.PRIMARY
        self._rect = pygame.Rect(0, 0, self._width, self._height)
        self._align_rect(self._rect, self.align, (self._x, self._y))

        if config.text is None:
            self._text = None
        else:
            self._text = Text(
                (self._rect.centerx, (self._rect.top + int(self._height * 0.2)))
                if config.buttons else self._rect.centery, config.text, config.font,
                config.font_size, config.text_color,
                "midtop" if config.buttons else "center", sub_widget=True)

        self._buttons = config.buttons
        if self._buttons:
            self._align_buttons(self._buttons, self._rect)

    def _align_rect(self, rect: pygame.Rect, align: RectAlignments,
                    coords: tuple[int, int]) -> None:
        setattr(rect, align, coords)
        self._x, self._y = getattr(rect, align)

    def _align_buttons(self, buttons: tuple[ButtonBase, ...],
                       rect: pygame.Rect) -> None:
        total_button_width = sum(button.width for button in buttons)
        gaps = len(buttons) + 1
        button_padding_x = round((rect.width - total_button_width) / gaps)
        y_position = rect.centery if not self._text else rect.bottom - int(
            self._height * 0.1)
        left = rect.left + button_padding_x

        for button in buttons:
            button.align = "bottomleft" if self._text else "midleft"
            button.x = left
            button.y = y_position
            left += button.width + button_padding_x

    @override
    def update(self) -> None:
        self._text.update() if self._text is not None else None
        for button in self._buttons:
            button.update()

    @override
    def render(self) -> None:
        self.state_manager.state_stack[-2].render()
        pygame.draw.rect(screen, self._color, self._rect)
        self._text.blit() if self._text is not None else None
        for button in self._buttons:
            button.blit()

    def blit(self) -> None:
        ...

    def startup(self) -> None:
        InputBinder.register(("keydown", pygame.K_ESCAPE),
                             action=self.state_manager.pop_overlay)

    def add_widgets(self) -> None:
        for button in self._buttons:
            widgethandler.add_widget(button)
        if self._text:
            widgethandler.add_widget(self._text)

    def cleanup(self) -> None:
        InputBinder.deregister(("keydown", pygame.K_ESCAPE))

    def clear_widgets(self) -> None:
        for button in self._buttons:
            widgethandler.remove_widget(button)
        if self._text:
            widgethandler.remove_widget(self._text)
