"""Module for displaying text on the screen."""
from __future__ import annotations

import warnings
from typing import Literal, TYPE_CHECKING, override

import pygame
from pygame import freetype

from data.components.ui.widgetutils import RenderNeeded, WidgetBase
from data.core import screen
from data.core.prepare import font_paths

if TYPE_CHECKING:
    from data.components import RectAlignments

text_rect_alignments = Literal["right", "left", "center", "justified"]
default_font_dir = font_paths("editundo")
default_font_size = 32


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
        if (font is not None and font_size != default_font_size) and not \
                isinstance(font, (pygame.freetype.Font, pygame.font.Font)):
            warnings.warn("font_size parameter passed when default font not used.",
                          stacklevel=2)

        self._text = text
        self._font = font if font is not None \
            else pygame.freetype.Font(default_font_dir)
        self._font_size = font_size
        self._color = color if color is not None else pygame.Color("white")
        self._antialias = antialias
        self._text_surface, self._rect = self._render_text(self._text, self._color)
        self._align_rect(self._rect, self._align, (self._x, self._y))
        self.requires_rerender = False

    @property
    def antialias(self) -> bool:
        return self._antialias

    @antialias.setter
    def antialias(self, value: bool) -> None:
        self._antialias = value
        self._font.antialiased = value

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @override
    def blit(self) -> None:
        screen.blit(self._text_surface, self._rect)

    @override
    def update(self) -> None:
        if self.requires_rerender:
            self._text_surface, self._rect = self._render_text(self._text, self._color)
        if self.requires_realignment:
            self._align_rect(self._rect, self._align, (self._x, self._y))

    @override
    def contains(self, x: int, y: int) -> bool:
        return (self._x < x - screen.get_abs_offset()[0] < self._x + self._rect.width) \
            and (self._y < y - screen.get_abs_offset()[1] < self._y + self._rect.height)


    def _render_text(self, text: str,
                     color: pygame.Color | tuple) -> tuple[pygame.Surface, pygame.Rect]:
        self._requires_rerender = False
        return self._font.render(text, color, size=self.font_size)

    def _align_rect(self, rect: pygame.Rect, align: RectAlignments,
                    position: tuple[int, int]) -> None:
        self._requires_realignment = False
        setattr(rect, align, position)
        self._x, self._y = getattr(rect, align)
