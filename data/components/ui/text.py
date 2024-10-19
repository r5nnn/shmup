"""Module for displaying text on the screen."""
import warnings
from typing import Literal, Optional, override, Type

import pygame
from pygame import freetype

from data.core.prepare import font_paths
from data.core.utils import CustomTypes
from .widgetutils import RenderNeeded, AlignmentNeeded, WidgetBase

text_rect_alignments: Type[str] = Literal['right', 'left', 'center', 'justified']
default_font_dir: str = font_paths('editundo')


class Text(WidgetBase):
    """Class for creating and displaying text on a surface.
    
    Aligns and renders text using `self._align_rect` and `self._render_text`:
    can be updated in real time and will update the rect and re-render itself
    as needed. Only to be used when the text is non interactable and doesn't
    need wrapping. Allows alligning the text to the coordinates provided.

    :param position: The position of the text with reference to the `align`
        argument passed.
    :param font: The font of the text. Defaults to `None` in order to use the
        `default_font_dir`.
    :param font_size: The size of the font, should only be used when the default
        font is used.
    :param color: The color of the text. Defaults to white.
    :param align: The point of the text rect that the `position` argument is
        referencing.
    :param antialias: Whether antialiasing should be used when rendering the text
        surface.
    :param surface: The surface that the text should be rendered to. Defaults
        to `None` to use the current display surface.
    """
    text = RenderNeeded()
    font = RenderNeeded()
    font_size = RenderNeeded()
    color = RenderNeeded()

    def __init__(self, position: tuple[int, int], text: str,
                 font: Optional[pygame.freetype.Font] = None,
                 font_size: int = 32,
                 color: pygame.Color | tuple = pygame.Color('white'),
                 align: CustomTypes.rect_alignments = 'topleft',
                 antialias: bool = False,
                 surface: Optional[pygame.Surface] = None,
                 sub_widget: bool = False):
        super().__init__(position, align, surface, sub_widget)

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

    @override
    def blit(self):
        self.surface.blit(self._text_surface, self._rect)

    @override
    def update(self):
        """Rerenders the text surface and updates the position of the rect."""
        if self._requires_rerender:
            self._text_surface, self._rect = self._render_text(self._text, self._color)
        if self._requires_realignment:
            self._align_rect(self._rect, self._align, self._coords)

    @override
    def contains(self, x, y):
        return (self._x < x - self._surface.get_abs_offset()[0] < self._x + self._rect.width) and \
               (self._y < y - self._surface.get_abs_offset()[1] < self._y + self._rect.height)

    def _render_text(self, text, color):
        self._requires_rerender = False
        return self._font.render(text, color, size=self.font_size)

    def _align_rect(self, rect, align, position):
        self._requires_realignment = False
        setattr(rect, align, position)
        self._coords = self._x, self._y = getattr(rect, align)


class WrappedText:
    """Class for creating and displaying wrapped text on a surface.
    
    Text wraps according to the bounding rect argument passed. Text can be
    aligned to the left, right, center or justified in the bounding rect. Text
    that cannot fit inside the rect is not displayed. Changing font size
    after an object has been instantiated is not supported yet.

    :param rect: The bounding rectangle that the text should fit in and wrap in
        accordance with.
    :param font: The font of the text. Defaults to `None` in order to use the
        `default_font_dir`.
    :param font_size: The size of the font, should only be used when the default
        font is used. Defaults to `32`.
    :param align: The point of the text rect that the `position` argument is
        referencing. Defaults to `'topleft'`.
    :param text_align: The alignment of the text inside the bounding rect provided.
        Can be left, right, center or justified.
    :param antialias: Whether antialiasing should be used when rendering the text
        surface. Defaults to `False`.
    :param surface: The surface that the text should be rendered to. Defaults
        to the current display surface: `pygame.display.get_surface`.
    """
    rect = AlignmentNeeded()
    text = RenderNeeded()
    font = RenderNeeded()
    color = RenderNeeded()
    align = AlignmentNeeded()
    line_spacing = RenderNeeded()

    def __init__(self, rect: pygame.Rect, text: str,
                 font: Optional[pygame.font.Font] = None, font_size: int = 32,
                 color: pygame.Color | tuple = pygame.Color('white'),
                 align: CustomTypes.rect_alignments = 'topleft',
                 text_align: text_rect_alignments = 'left',
                 antialias: bool = False, line_spacing: int = 0,
                 surface: Optional[pygame.Surface] = None):
        self._rect = rect if rect is not None else surface.get_rect()
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
        """Rerenders the text surface and updates the position of the rect."""
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
