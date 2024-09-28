import warnings
from abc import ABC, abstractmethod
from typing import Literal, override

import pygame
from pygame import freetype

from data.utils import CustomTypes
from data import fonts
from .. import ui


class _TextBase(ABC):
    default_font_dir = None

    def __init__(self,
                 font: pygame.freetype.Font | int = None,
                 font_size: int = 32, ):
        if font and _TextBase.default_font_dir is None:
            raise TypeError("default_font_dir not specified and no font passed "
                            "when creating instance. One or the other must be "
                            "defined.")
        elif (font is not None and font_size != 32) and not isinstance(
                font, pygame.freetype.Font):
            warnings.warn("font_size parameter passed when default font not "
                          "used.")

        self._requires_render, self._requires_rect_update = False, False

    @abstractmethod
    def _render_text(self, *args):
        pass

    @abstractmethod
    def _align_rect(self, *args):
        pass


class Text(_TextBase):
    font = ui.RenderNeeded()
    font_size = ui.RenderNeeded()
    text = ui.RenderNeeded()
    x = ui.RectUpdateNeeded()
    y = ui.RectUpdateNeeded()
    coords = ui.RectUpdateNeeded()
    color = ui.RenderNeeded()
    text_surface = ui.RenderNeeded()

    def __init__(self,
                 surface: pygame.Surface,
                 text: str,
                 coordinates: tuple,
                 font_size: int,
                 font: pygame.freetype.Font | int = None,
                 color: pygame.Color | tuple = pygame.Color('white'),
                 align: CustomTypes.rect_alignments = 'topleft',
                 antialias: bool = False):
        """
        Class for creating and managing text surfaces.

        Only to be used when the text is non interactable and doesn't need
        wrapping. Allows alligning the text to the coords provided.

        :param surface: Surface which the text surface will be blit onto.
        :param text: Text to be displayed.
        :param coordinates: X and Y coordinates of font.
        :param font: The pygame.font.Font object to use.
        :param font_size: The size of the default font (if used).
        :param color: Color of the text.
        :param align: Alignment of the text coordinates.
        :param antialias: Whether to use antialiasing when rendering the font.
        """
        super().__init__(font, font_size)  # argument error checking occurs here
        self.surface = surface
        self._font = font if font is not None \
            else pygame.freetype.Font(_TextBase.default_font_dir)
        self.font_size = font_size
        self._text = text
        self._align = align.lower()
        self.antialias = antialias
        self._color = color
        self._text_surface, self._rect = self._render_text(self._text,
                                                           self._color)
        self._align_rect(self._rect, self._align, coordinates)

    @property
    def rect(self):
        return self._rect

    @property
    def antialias(self):
        return self._antialias

    @antialias.setter
    def antialias(self, value):
        self._antialias = value
        self._font.antialiased = value

    def contains(self, x, y):
        return (self._rect.left < x - self.surface.get_abs_offset()[0]
                < self._rect.left + self._rect.width) and \
            (self._rect.top < y - self.surface.get_abs_offset()[1]
             < self._rect.top + self._rect.height)

    def _render_text(self, text, color):
        self._requires_render = False
        return self._font.render(text, color, size=self.font_size)

    def _align_rect(self, rect, align, coords):
        self._requires_rect_update = False
        setattr(rect, align, coords)
        self._coords = self._x, self._y = getattr(rect, align)

    def blit(self):
        """Draws the text onto the surface."""
        self.surface.blit(self._text_surface, self._rect)

    def update(self):
        """Rerenders the text surface and updates
        the position of the rect if nessecary."""
        if self._requires_render:
            self._text_surface, self._rect = self._render_text(self._text,
                                                               self._color)
        if self._requires_rect_update:
            self._align_rect(self._rect, self._align, self._coords)


class WrappedText(_TextBase):
    default_font_dir = None

    text = ui.RenderNeeded()
    rect = ui.RectUpdateNeeded()
    font = ui.RenderNeeded()
    x = ui.RectUpdateNeeded()
    y = ui.RectUpdateNeeded()
    align = ui.RectUpdateNeeded()
    color = ui.RenderNeeded()
    line_spacing = ui.RenderNeeded()

    def __init__(self,
                 surface: pygame.Surface,
                 text: str,
                 rect: pygame.Rect,
                 font: pygame.font.Font | int = None,
                 font_size: int = 32,
                 color: pygame.Color | tuple = pygame.Color('white'),
                 align: CustomTypes.rect_alignments = 'topleft',
                 text_align: Literal['right', 'left', 'block'] = 'left',
                 antialias: bool = False,
                 line_spacing: int = 0):
        """
        Class for creating and managing text surfaces that require wrapping.

        Allows for wrapping to the left, right, center, or block wrapping
        e.g. in a book.

        :param surface: Surface which the text surface will be blit onto.
        :param text: Text to be displayed.
        :param rect: The rect which the text should fit and wrap in.
        :param font: The pygame.font.Font object to use.
        :param font_size: The size of the default font (if used).
        :param color: Color of the text.
        :param align: Alignment of the text coordinates.
        :param text_align: The wrap alignment of the text.
        :param antialias: Whether to use antialiasing when rendering the font.
        :param line_spacing: The spacing between new lines created when
        wrapping.
        """
        super().__init__(font, font_size)
        self.surface = surface
        self._text = text
        self._rect = rect if rect is not None else self.surface.get_rect()
        self._font = font if font is not None else WrappedText.default_font_dir
        self._color = color
        self._align = align.lower()
        self._antialias = antialias
        self.text_align = text_align
        self._line_spacing = line_spacing
        self._line_len_list = [0]
        self._line_list = [[]]
        self._coords = self._x, self._y = self._rect.topleft
        self._align_rect(self._rect, self._align, self._coords)
        self._render_text(antialias, color)

    def blit(self):
        if self._requires_rect_update:
            self._requires_render = True
            self._align_rect(self._rect, self._align, self._coords)
        if self._requires_render:
            self._render_text(self._antialias, self._color)
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

    @override
    def _render_text(self, aa, col):
        self._requires_render = False
        self._space_width = self._font.size(" ")[0]
        self._words_list = self._text.split(" ")
        surface_list = [self._font.render(word, aa, col) for word in
                        self._words_list]
        max_len = self._rect[2]

        for surface in surface_list:
            width = surface.get_width()
            line_len = (self._line_len_list[-1] + len(self._line_list[-1]) *
                        self._space_width + width)
            if len(self._line_list[-1]) == 0 or line_len <= max_len:
                self._line_len_list[-1] += width
                self._line_list[-1].append(surface)
            else:
                self._line_len_list.append(width)
                self._line_list.append([surface])

    @override
    def _align_rect(self, rect, align, coords):
        self._requires_rect_update = False
        setattr(rect, align, coords)


_TextBase.default_font_dir = fonts('editundo')