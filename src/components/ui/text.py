"""Module for displaying text on the screen."""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING, override

import pygame
from pygame import freetype

from src.components.ui.widgetutils import RenderNeeded, WidgetBase
from src.core.constants import DEFAULT_FONT_SIZE, DEFAULT_FONT_NAME
from src.core.data import system_data

if TYPE_CHECKING:
    from src.core.types import RectAlignments


class Text(WidgetBase):
    text = RenderNeeded()
    font = RenderNeeded()
    font_size = RenderNeeded()
    color = RenderNeeded()

    def __init__(
        self,
        position: tuple[int, int],
        text: str,
        font: pygame.freetype.Font | None = None,
        font_size: int = 32,
        color: pygame.Color | tuple | None = None,
        align: RectAlignments = "topleft",
        wrap_width: int | None = None,
        wrap_padding: int = 0,
        *,
        antialias: bool = False,
        sub_widget: bool = False,
    ):
        super().__init__(position, align, sub_widget=sub_widget)
        if (
            font is not None and font_size != DEFAULT_FONT_SIZE
        ) and not isinstance(font, (pygame.freetype.Font, pygame.font.Font)):
            warnings.warn(
                f"font_size: {font_size} parameter passed when "
                f"default font not used.",
                stacklevel=2,
            )

        self._text = text
        self._font = (
            font
            if font is not None
            else pygame.freetype.Font(system_data.font_paths(DEFAULT_FONT_NAME))
        )
        self._font_size = font_size
        self._color = color if color is not None else pygame.Color("white")
        self.wrap_width = wrap_width
        self.wrap_padding = wrap_padding
        self.wrap_rects = []
        self._antialias = antialias
        self.requires_rerender = False
        self.line_height = self._font.get_sized_height(self._font_size)
        self.text_surface, self.rect = self.render_text(
            self._text, self._color
        )
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
        system_data.window.blit(self.text_surface, self.rect)
        pygame.draw.rect(system_data.window, (0, 0, 100), self.rect)

    @override
    def update(self) -> None:
        if self.requires_rerender:
            self.line_height = self._font.get_sized_height(self._font_size)
            self.text_surface, self.rect = self.render_text(
                self._text, self._color
            )
        if self.requires_realignment:
            self.align_rect()

    @override
    def contains(self, x: int, y: int) -> bool:
        super().contains(x, y)
        return self.rect.collidepoint(x, y)

    def render_text(
        self, text: str, color: pygame.Color | tuple
    ) -> tuple[pygame.Surface, pygame.Rect]:
        self.requires_rerender = False
        if self.wrap_width is None:
            return self._font.render(text, color, size=self.font_size)
        return self.render_wrapped(text, color)

    def render_wrapped(
        self, text: str, color: pygame.Color | tuple
    ) -> tuple[pygame.Surface, pygame.Rect]:
        r"""Renders the text with word wrapping.

        This method splits text into paragraphs by '\n' and then wraps each paragraph
        by measuring word widths. It renders each line onto a new surface.
        """
        newline_wrapped_text = text.split("\n")
        wrapped_lines = []
        # line_rect is defined outside the for loop to avoid crashes if no text
        # passed but wrap_width still defined.
        line_rect = None
        for line in newline_wrapped_text:
            words = line.split(" ")
            current_line = ""
            for word in words:
                new_line = (
                    f"{current_line} {word}".strip() if current_line else word
                )
                line_rect = self._font.get_rect(new_line, size=self._font_size)
                if line_rect.width > self.wrap_width:
                    wrapped_lines.append(current_line)
                    self.wrap_rects.append(line_rect)
                    # start the next line with the word that didn't fit
                    current_line = word
                else:
                    current_line = new_line
            # During the last iteration, the current_line and line_rect won't
            # be appended in the inner for loop so is appended here.
            wrapped_lines.append(current_line)
            self.wrap_rects.append(line_rect) if line_rect is not None else None
        # There is no padding below the last line, so subtract one when
        # calculating total padding.
        total_height = (
            len(wrapped_lines) * self.line_height
            + (len(wrapped_lines) - 1) * self.wrap_padding
        )
        surface = pygame.Surface(
            (self.wrap_width, total_height), pygame.SRCALPHA
        )
        y_offset = 0
        for line in wrapped_lines:
            self._font.render_to(
                surface, (0, y_offset), line, color, size=self._font_size
            )
            y_offset += self.line_height + self.wrap_padding
        return surface, pygame.Rect(*self.wrap_rects[0].topleft, self.wrap_rects[0].width, 0)

    def align_rect(self) -> None:
        self.requires_realignment = False
        setattr(self.rect, self._align, (self._x, self._y))
        self._x, self._y = self.rect.topleft
        if self.wrap_rects:
            y_offset = 0
            for line_rect in self.wrap_rects:
                line_rect.topleft = (self._x, self._y + y_offset)
                y_offset += line_rect.height + self.wrap_padding
            self.rect.height = self.wrap_rects[-1].bottom - self.wrap_rects[0].top


@dataclass
class TextArrayConfig:
    text: tuple[tuple[str, ...], ...]
    font: pygame.freetype.Font | None = None
    font_size: int = 32
    color: pygame.Color | tuple | None = None
    align: RectAlignments = "topleft"
    wrap_width: int | None = None
    wrap_padding: int = 0
    antialias: bool = False


def _make_text(
    row: int, column: int, x_pos: int, y_pos: int, config: TextArrayConfig
) -> Text:
    return Text(
        (x_pos, y_pos),
        config.text[column][row],
        config.font,
        config.font_size,
        config.color,
        config.align,
        config.wrap_width,
        config.wrap_padding,
        antialias=config.antialias,
        sub_widget=True,
    )


class TextArray(WidgetBase):
    def __init__(
        self,
        arr_position: tuple[int, int],
        arr_shape: tuple[int, int],
        arr_padding: tuple[int, int] | int,
        config: TextArrayConfig,
        *,
        arr_sub_widget: bool = False,
    ):
        super().__init__(arr_position, sub_widget=arr_sub_widget)

        arr_padding = (
            arr_padding
            if isinstance(arr_padding, tuple)
            else (arr_padding, arr_padding)
        )
        self.texts = []
        x_pos, y_pos = self._x, self._y
        for column in range(arr_shape[1]):
            for row in range(arr_shape[0]):
                self.texts.append(
                    _make_text(row, column, x_pos, y_pos, config)
                )
                y_pos = self.texts[-1].rect.bottom + arr_padding[1]
            x_pos = self.texts[-1].rect.right + arr_padding[0]
            y_pos = self._y

    @override
    def update(self) -> None:
        super().update()
        for button in self.texts:
            button.update()

    @override
    def blit(self) -> None:
        for button in self.texts:
            button.blit()

    @override
    def contains(self, x: int, y: int) -> bool | None:
        return super().contains(x, y)