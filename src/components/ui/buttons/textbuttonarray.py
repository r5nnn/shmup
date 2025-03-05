from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, override


from src.components.ui.buttons import (
    TextToggleButton, TextClickButton, TextRectToggleButton,
    TextRectClickButton, ImageClickButton, ImageToggleButton,
    ImageRectClickButton, ImageRectToggleButton, TextButtonConfig)
from src.components.ui.widgetutils import WidgetBase

if TYPE_CHECKING:
    import pygame
    from src.components.ui.buttons._types import _Colors, _Align


_AnyButton = (TextToggleButton | TextClickButton | TextRectToggleButton
            | TextRectClickButton | ImageClickButton | ImageToggleButton
            | ImageRectClickButton | ImageRectToggleButton)


@dataclass(kw_only=True)
class _ArrayBaseButtonConfig:
    audio_tags: list[str | None] | None = None


class ButtonArrayBase(WidgetBase, ABC):
    def __init__(self, arr_position: tuple[int, int],
                 arr_shape: tuple[int, int], arr_padding: tuple[int, int] | int,
                 config: _ArrayBaseButtonConfig, arr_align: _Align = None, *,
                 arr_sub_widget: bool = False):
        super().__init__(arr_position, (arr_align[0] + arr_align[1]
                                        if arr_align is not None
                                        else "topleft"),
                         sub_widget=arr_sub_widget)
        self.buttons = []
        arr_padding = arr_padding if isinstance(arr_padding, tuple) else (
            arr_padding, arr_padding)
        x_pos, y_pos = self._x, self._y
        for column in range(arr_shape[1]):
            for row in range(arr_shape[0]):
                self.buttons.append(
                    self.make_button(row, column, x_pos, y_pos, arr_align,
                                      config))
                y_pos = self.buttons[-1].rect.bottom + arr_padding[1]
            x_pos = self.buttons[-1].rect.right + arr_padding[0]
            y_pos = self._y

    @override
    def update(self) -> None:
        super().update()
        for button in self.buttons:
            button.update()

    @override
    def blit(self) -> None:
        for button in self.buttons:
            button.blit()

    @override
    def contains(self, x: int, y: int) -> bool | None:
        super().contains(x, y)


    def make_button(
            self, row: int, column: int, x_pos: int, y_pos: int, align: _Align,
            config: _ArrayBaseButtonConfig) -> _AnyButton: ...


@dataclass(kw_only=True)
class TextArrayConfig(_ArrayBaseButtonConfig):
    text_colors: _Colors = None
    font: pygame.font.Font | None = None
    font_size: int = 32


@dataclass
class TextToggleButtonArrayConfig(TextArrayConfig):
    texts: tuple[tuple[str | list[str], ...], ...]
    start_texts: tuple[tuple[int, ...], ...] | int = 0
    on_toggle_on: tuple[tuple[Callable | None, ...], ...] | None = None
    on_toggle_off: tuple[tuple[Callable | None, ...], ...] | None = None
    requires_state: bool = False


class TextToggleButtonArray(ButtonArrayBase):
    def __init__(self, arr_position: tuple[int, int],
                 arr_shape: tuple[int, int], arr_padding: tuple[int, int] | int,
                 config: TextToggleButtonArrayConfig, arr_align: _Align = None,
                 *, arr_sub_widget: bool = False):
        super().__init__(arr_position, arr_shape, arr_padding, config,
                         arr_align, arr_sub_widget=arr_sub_widget)

    @override
    def make_button(
            self, row: int, column: int, x_pos: int, y_pos: int, align: _Align,
            config: TextToggleButtonArrayConfig) -> _AnyButton:
        config_ = TextButtonConfig(
            position=(x_pos, y_pos), align=align, audio_tags=config.audio_tags,
            sub_widget=True, text_colors=config.text_colors, font=config.font,
            font_size=config.font_size)
        start_texts = config.start_texts[column][row] \
        if not isinstance(config.start_texts, int) else config.start_texts
        on_toggle_on = config.on_toggle_on[column][row] \
            if config.on_toggle_on is not None else None
        on_toggle_off = config.on_toggle_off[column][row] \
            if config.on_toggle_off is not None else None

        return TextToggleButton(config_, config.texts[column][row],
                                start_texts, on_toggle_on, on_toggle_off,
                                requires_state=config.requires_state)

