"""Module for displaying text on the screen."""
import warnings
from typing import Literal, Optional, override, Type

import pygame
from pygame import freetype

from data.core.prepare import font_paths
from data.components import RectAlignments
from .widgetutils import RenderNeeded, AlignmentNeeded, WidgetBase
from data.core import screen, screen_size

text_rect_alignments: Type[str] = Literal['right', 'left', 'center', 'justified']
default_font_dir: str = font_paths('editundo')


class Text(WidgetBase):
    text = RenderNeeded()
    font = RenderNeeded()
    font_size = RenderNeeded()
    color = RenderNeeded()

    def __init__(self, position: tuple[int, int], text: str,
                 font: Optional[pygame.freetype.Font] = None,
                 font_size: int = 32,
                 color: pygame.Color | tuple = pygame.Color('white'),
                 align: RectAlignments = 'topleft',
                 antialias: bool = False,
                 sub_widget: bool = False):
        super().__init__(position, align, sub_widget)

        if (font is not None and font_size != 32) and not \
                isinstance(font, (pygame.freetype.Font, pygame.font.Font)):
            warnings.warn("font_size parameter passed when default font not "
                          "used.")

        self._text = text
        self._font = font if font is not None \
            else pygame.freetype.Font(default_font_dir)
        self._font_size = font_size
        self._color = color
        self._antialias = antialias
        self._text_surface, self._rect = self._render_text(self._text, self._color)
        self._align_rect(self._rect, self._align, (self._x, self._y))
        self._requires_rerender = False

    @property
    def antialias(self) -> bool:
        return self._antialias

    @antialias.setter
    def antialias(self, value):
        self._antialias = value
        self._font.antialiased = value

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    def blit(self):
        screen.blit(self._text_surface, self._rect)

    def update(self):
        if self._requires_rerender:
            self._text_surface, self._rect = self._render_text(self._text, self._color)
        if self._requires_realignment:
            self._align_rect(self._rect, self._align, self._coords)

    def contains(self, x, y):
        return (self._x < x - screen.get_abs_offset()[0] < self._x + self._rect.width) and \
               (self._y < y - screen.get_abs_offset()[1] < self._y + self._rect.height)

    def _render_text(self, text, color):
        self._requires_rerender = False
        return self._font.render(text, color, size=self.font_size)

    def _align_rect(self, rect, align, position):
        self._requires_realignment = False
        setattr(rect, align, position)
        self._coords = self._x, self._y = getattr(rect, align)


class WrappedText:
    rect = AlignmentNeeded()
    text = RenderNeeded()
    font = RenderNeeded()
    color = RenderNeeded()
    align = AlignmentNeeded()
    line_spacing = RenderNeeded()

    def __init__(self, rect: pygame.Rect, text: str,
                 font: Optional[pygame.font.Font] = None, font_size: int = 32,
                 color: pygame.Color | tuple = pygame.Color('white'),
                 align: RectAlignments = 'topleft',
                 text_align: text_rect_alignments = 'left',
                 antialias: bool = False, line_spacing: int = 0):
        self._rect = rect if rect is not None else screen_size
        self._text = text
        self._font = font if font is not None else \
            pygame.font.Font(default_font_dir, font_size)
        self._font_size = font_size
        self._color = color
        self._align = align
        self.text_align = text_align
        self._antialias = antialias
        self.surface = surface
        self._line_spacing = line_spacing
        self._space_width = None
        self._line_len_list = [0]
        self._line_list = [[]]
        self._align_rect(self._rect, self._align, self._rect.topleft)
        self._render_text(antialias, color)
        self._requires_render, self._requires_realignment = False, False

    @property
    def antialias(self) -> bool:
        return self._antialias

    @antialias.setter
    def antialias(self, value):
        self._antialias = value
        self._font.antialiased = value

    def blit(self):
        font_height = self._font.size("Tg")[1]
        line_bottom = self._rect[1]
        last_line = 0
        for line_len, line_surfaces in zip(self._line_len_list,
                                           self._line_list):
            line_left = self._rect[0]
            if self.text_align == 'right':
                line_left += + self._rect[2] - line_len - self._space_width * (
                        len(line_surfaces) - 1)
            elif self.text_align == 'center':
                line_left += (self._rect[2] - line_len - self._space_width * (
                        len(line_surfaces) - 1)) // 2
            elif self.text_align == 'block' and len(line_surfaces) > 1:
                self._space_width = (self._rect[2] - line_len) // (len(
                    line_surfaces) - 1)
            if line_bottom + font_height > self._rect[1] + self._rect[3]:
                break
            last_line += 1
            for i, image in enumerate(line_surfaces):
                x, y = line_left + i * self._space_width, line_bottom
                self.surface.blit(image, (round(x), y))
                line_left += image.get_width()
            line_bottom += font_height + self._line_spacing

        if last_line < len(self._line_list):
            draw_words = sum([len(self._line_list[i])
                              for i in range(last_line)])
            remaining_text = ""
            for text in self._words_list[draw_words:]:
                remaining_text += text + " "
            return remaining_text
        return ""

    def update(self):
        if self._requires_render:
            self._render_text(self._text, self._color)
        if self._requires_realignment:
            self._align_rect(self._rect, self._align, self._rect.topleft)

    def _render_text(self, aa, col):
        self._requires_render = False
        self._space_width = self._font.size(" ")[0]
        self._words_list = self._text.split(" ")
        surface_list = [self._font.render(word, aa, col) for word in
                        self._words_list]
        max_len = self._rect[2]

        for surface in surface_list:
            width = surface.get_width()
            line_len = (self._line_len_list[-1] + len(self._line_list[-1]) * self._space_width + width)
            if len(self._line_list[-1]) == 0 or line_len <= max_len:
                self._line_len_list[-1] += width
                self._line_list[-1].append(surface)
            else:
                self._line_len_list.append(width)
                self._line_list.append([surface])

    def _align_rect(self, rect, align, coords):
        self._requires_rect_update = False
        setattr(rect, align, coords)
