from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, override

from src.components.ui.buttons import (
    TextToggleButton, TextButtonConfig)
from src.components.ui.buttons.buttonbases import (
    _BaseButtonArrayConfig, ButtonArrayBase)

if TYPE_CHECKING:
    import pygame
    from src.components.ui.buttons._types import _Colors, _AnyButton


@dataclass(kw_only=True)
class TextButtonArrayConfig(_BaseButtonArrayConfig):
    text_colors: _Colors = None
    font: pygame.font.Font | None = None
    font_size: int = 32


@dataclass
class TextToggleButtonArrayConfig(TextButtonArrayConfig):
    texts: tuple[tuple[str | list[str], ...], ...]
    start_texts: tuple[tuple[int, ...], ...] | int = 0
    on_toggle_on: tuple[tuple[Callable | None, ...], ...] | None = None
    on_toggle_off: tuple[tuple[Callable | None, ...], ...] | None = None
    requires_state: bool = False


class TextToggleButtonArray(ButtonArrayBase):
    def __init__(self, arr_position: tuple[int, int],
                 arr_shape: tuple[int, int], arr_padding: tuple[int, int] | int,
                 config: TextToggleButtonArrayConfig,
                 *, arr_sub_widget: bool = False):
        super().__init__(arr_position, arr_shape, arr_padding, config,
                         arr_sub_widget=arr_sub_widget)

    @override
    def make_button(self, row: int, column: int, x_pos: int, y_pos: int,
                    config: TextToggleButtonArrayConfig) -> _AnyButton:
        config_ = TextButtonConfig(
            position=(x_pos, y_pos), align=config.align, audio_tags=config.audio_tags,
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


@dataclass
class TextClickButtonArrayConfig(TextButtonArrayConfig):
    texts: tuple[tuple[str, ...], ...]
    on_click: tuple[tuple[Callable | None, ...], ...] | None = None
    on_release: tuple[tuple[Callable | None, ...], ...] | None = None


class TextClickButtonArray(ButtonArrayBase):
    ...