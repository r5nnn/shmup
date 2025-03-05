"""Module for displaying text on the screen."""
from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, override

import pygame
from pygame import freetype

from src.components.ui.widgetutils import RenderNeeded, WidgetBase
from src.core import screen
from src.core.constants import DEFAULT_FONT_SIZE, DEFAULT_FONT_NAME
from src.core.prepare import font_paths

if TYPE_CHECKING:
    from src.core.constants import RectAlignments


class Text(WidgetBase):
    text = RenderNeeded()
    font = RenderNeeded()
    font_size = RenderNeeded()
    color = RenderNeeded()

    def __init__(self, position: tuple[int, int], text: str,
                 font: pygame.freetype.Font | None = None,
                 font_size: int = 32,
                 color: pygame.Color | tuple | None = None,
                 align: RectAlignments = "topleft", *,
                 antialias: bool = False,
                 sub_widget: bool = False):
        super().__init__(position, align, sub_widget=sub_widget)
        if (font is not None and font_size != DEFAULT_FONT_SIZE) and not \
                isinstance(font, (pygame.freetype.Font, pygame.font.Font)):
            warnings.warn(f"font_size: {font_size} parameter passed when "
                          f"default font not used.", stacklevel=2)

        self._text = text
        self._font = (font if font is not None
                      else pygame.freetype.Font(font_paths(DEFAULT_FONT_NAME)))
        self._font_size = font_size
        self._color = color if color is not None else pygame.Color("white")
        self._antialias = antialias
        self.requires_rerender = False
        self.text_surface, self.rect = self.render_text(
            self._text, self._color)
        self.align_rect()

    @property
    def antialias(self) -> bool:
        return self._antialias

    @antialias.setter
    def antialias(self, value: bool) -> None:
        self._antialias = value
        self._font.antialiased = value

    @override
    def blit(self) -> None:
        screen.blit(self.text_surface, self.rect)

    @override
    def update(self) -> None:
        if self.requires_rerender:
            self.text_surface, self.rect = self.render_text(
                self._text, self._color)
        if self.requires_realignment:
            self.align_rect()

    @override
    def contains(self, x: int, y: int) -> bool:
        super().contains(x, y)
        return self.rect.collidepoint(x, y)


    def render_text(self, text: str, color: pygame.Color | tuple) -> (
            tuple)[pygame.Surface, pygame.Rect]:
        self.requires_rerender = False
        return self._font.render(text, color, size=self.font_size)

    def align_rect(self) -> None:
        self.requires_realignment = False
        setattr(self.rect, self._align, (self._x, self._y))
        self._x, self._y = self.rect.topleft
