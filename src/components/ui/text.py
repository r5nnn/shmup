"""Module for displaying text on the screen."""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING, override

import pygame
from pygame import freetype

from src.components.ui.widgetutils import (
    CompositeWidgetBase,
    RenderNeeded,
    WidgetBase,
)
from src.core.constants import DEFAULT_FONT_SIZE, DEFAULT_FONT_NAME
from src.core.data import system_data
from src.core.load import Load

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
        allow_passthrough: bool = True,
        sub_widget: bool = False,
    ):
        super().__init__(
            position,
            align,
            allow_passthrough=allow_passthrough,
            sub_widget=sub_widget,
        )
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
            else pygame.freetype.Font(Load("font").path[DEFAULT_FONT_NAME])
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
        system_data.abs_window.blit(self.text_surface, self.rect)

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
        if not super().contains(x, y):
            return False
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

        This method splits text into paragraphs by '\n' and then wraps each
        paragraph by measuring word widths. It renders each line onto a new
        surface.
        """
        newline_wrapped_text = text.split("\n")
        wrapped_lines = []
        # line_rect is defined outside the for loop to avoid crashes if no text
        # passed but wrap_width still defined.
        longest_line_width = 0
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
                    current_line_rect = self._font.get_rect(
                        current_line, size=self._font_size
                    )
                    self.wrap_rects.append(current_line_rect)
                    longest_line_width = max(
                        longest_line_width, current_line_rect.width
                    )
                    # start the next line with the word that didn't fit
                    current_line = word
                else:
                    current_line = new_line
            # During the last iteration, the current_line and line_rect won't
            # be appended in the inner for loop so is appended here.
            if current_line:
                current_line_rect = self._font.get_rect(
                    current_line, size=self._font_size
                )
                wrapped_lines.append(current_line)
                longest_line_width = max(
                    longest_line_width, current_line_rect.width
                )
                self.wrap_rects.append(current_line_rect)
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
        for line, line_rect in zip(wrapped_lines, self.wrap_rects):
            self._font.render_to(
                surface, (0, y_offset), line, color, size=self._font_size
            )
            line_rect.top = y_offset
            y_offset += self.line_height + self.wrap_padding
        return surface, pygame.Rect(
            *self.wrap_rects[0].topleft, longest_line_width, 0
        )

    def align_rect(self) -> None:
        self.requires_realignment = self.sub_widget
        setattr(self.rect, self._align, (self._x, self._y))
        if self.wrap_rects:
            for line_rect in self.wrap_rects:
                line_rect.left = self._x
                line_rect.top += self._y
            self.rect.height = (
                self.wrap_rects[-1].bottom - self.wrap_rects[0].top
            )

    def __str__(self):
        return f"{super().__str__()[:-1]} {self.text=}"


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
    allow_passthrough: bool = True


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
        allow_passthrough=config.allow_passthrough,
        sub_widget=True,
    )


class TextArray(CompositeWidgetBase):
    def __init__(
        self,
        position: tuple[int, int] | list[int],
        shape: tuple[int, int],
        padding: tuple[int, int] | int,
        config: TextArrayConfig,
        **kwargs,
    ):
        super().__init__(position, **kwargs)
        self.shape = shape
        self.padding = (
            padding if isinstance(padding, tuple) else (padding, padding)
        )
        self.texts = []
        x_pos, y_pos = self._x, self._y
        for column in range(self.shape[1]):
            for row in range(self.shape[0]):
                self.texts.append(
                    _make_text(row, column, x_pos, y_pos, config)
                )
                y_pos = self.texts[-1].rect.bottom + self.padding[1]
            x_pos = self.texts[-1].rect.right + self.padding[0]
            y_pos = self._y

    @override
    def update(self, *, disabled_sub_widgets: list[WidgetBase] = ()) -> None:
        if not super().update(disabled_sub_widgets):
            return
        for text_obj in self.texts:
            if text_obj not in disabled_sub_widgets:
                text_obj.update()

    @override
    def blit(self) -> None:
        for text_obj in self.texts:
            if not text_obj.hidden:
                text_obj.blit()

    @override
    def contains(self, x: int, y: int) -> list[Text]:
        if not super().contains(x, y):
            return []
        texts = [
            text_obj for text_obj in self.texts if text_obj.contains(x, y)
        ]
        return [self] if texts == self.texts else texts

    @override
    def __str__(self):
        return f"{super().__str__()[:-1]} {self.shape=} {self.texts=}"
