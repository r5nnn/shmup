from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, override

from src.components.ui.buttons import (
    TextToggleButton, TextButtonConfig, TextClickButton, TextRectClickButton,
    TextRectToggleButton)
from src.components.ui.buttons.buttonbases import (
    _BaseButtonArrayConfig, ButtonArrayBase)

if TYPE_CHECKING:
    import pygame
    from src.components.ui.buttons._types import _Colors, _AnyButton, _Align


@dataclass(kw_only=True)
class _TextButtonArrayConfig(_BaseButtonArrayConfig):
    text_colors: _Colors = None
    font: pygame.font.Font | None = None
    font_size: int = 32


class TextToggleButtonArrayConfig(_TextButtonArrayConfig):
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
            position=(x_pos, y_pos), align=config.align,
            audio_tags=config.audio_tags, sub_widget=True,
            text_colors=config.text_colors, font=config.font,
            font_size=config.font_size)
        start_texts = (config.start_texts[column][row]
                       if not isinstance(config.start_texts, int)
                       else config.start_texts)
        on_toggle_on = (config.on_toggle_on[column][row]
                        if config.on_toggle_on is not None else None)
        on_toggle_off = (config.on_toggle_off[column][row]
                         if config.on_toggle_off is not None else None)

        return TextToggleButton(config_, config.texts[column][row],
                                start_texts, on_toggle_on, on_toggle_off,
                                requires_state=config.requires_state)


@dataclass(kw_only=True)
class TextClickButtonArrayConfig(_TextButtonArrayConfig):
    texts: tuple[tuple[str, ...], ...]
    on_click: tuple[tuple[Callable | None, ...], ...] | None = None
    on_release: tuple[tuple[Callable | None, ...], ...] | None = None


class TextClickButtonArray(ButtonArrayBase):
    def __init__(self, arr_position: tuple[int, int],
                 arr_shape: tuple[int, int], arr_padding: tuple[int, int] | int,
                 config: TextClickButtonArrayConfig,
                 *, arr_sub_widget: bool = False):
        super().__init__(arr_position, arr_shape, arr_padding, config,
                         arr_sub_widget=arr_sub_widget)

    @override
    def make_button(self, row: int, column: int, x_pos: int, y_pos: int,
                    config: TextClickButtonArrayConfig) -> _AnyButton:
        config_ = TextButtonConfig(
            position=(x_pos, y_pos), align=config.align,
            audio_tags=config.audio_tags, sub_widget=True,
            text_colors=config.text_colors, font=config.font,
            font_size=config.font_size)
        on_click = (config.on_click[column][row]
                        if config.on_click is not None else None)
        on_release = (config.on_release[column][row]
                         if config.on_release is not None else None)

        return TextClickButton(config_, config.texts[column][row], on_click,
                               on_release)


@dataclass
class TextRectToggleButtonArrayConfig(TextToggleButtonArrayConfig):
    sizes: tuple[tuple[tuple[int, int], ...], ...] | tuple[int, int]
    radius: int = 0
    colors: _Colors | None = None
    text_align: _Align | None = None
    padding: int = 20


class TextRectToggleButtonArray(ButtonArrayBase):
    def __init__(self, arr_position: tuple[int, int],
                 arr_shape: tuple[int, int], arr_padding: tuple[int, int] | int,
                 config: TextRectToggleButtonArrayConfig,
                 *, arr_sub_widget: bool = False):
        super().__init__(arr_position, arr_shape, arr_padding, config,
                         arr_sub_widget=arr_sub_widget)

    @override
    def make_button(self, row: int, column: int, x_pos: int, y_pos: int,
                    config: TextRectToggleButtonArrayConfig) -> _AnyButton:
        config_ = TextButtonConfig(
            position=(x_pos, y_pos), align=config.align,
            audio_tags=config.audio_tags, sub_widget=True,
            text_colors=config.text_colors, font=config.font,
            font_size=config.font_size)
        size = (config.sizes
                 if isinstance(config.sizes[0], int)
                 else config.sizes[column][row])
        start_text = (config.start_texts
                       if isinstance(config.start_texts, int)
                       else config.start_texts[column][row])
        on_toggle_on = (config.on_toggle_on[column][row]
                        if config.on_toggle_on is not None else None)
        on_toggle_off = (config.on_toggle_off[column][row]
                         if config.on_toggle_off is not None else None)

        return TextRectToggleButton(
            config_, size, config.texts[column][row],
            config.radius, config.colors, start_text, config.text_align,
            config.padding, on_toggle_on, on_toggle_off,
            requires_state=config.requires_state)


@dataclass
class TextRectClickButtonArrayConfig(TextClickButtonArrayConfig):
    sizes: tuple[tuple[tuple[int, int], ...], ...] | tuple[int, int]
    radius: int = 0
    colors: _Colors | None = None
    text_align: _Align | None = None
    padding: int = 20


class TextRectClickButtonArray(ButtonArrayBase):
    def __init__(self, arr_position: tuple[int, int],
                 arr_shape: tuple[int, int], arr_padding: tuple[int, int] | int,
                 config: TextRectClickButtonArrayConfig,
                 *, arr_sub_widget: bool = False):
        super().__init__(arr_position, arr_shape, arr_padding, config,
                         arr_sub_widget=arr_sub_widget)

    @override
    def make_button(self, row: int, column: int, x_pos: int, y_pos: int,
                    config: TextRectClickButtonArrayConfig) -> _AnyButton:
        config_ = TextButtonConfig(
            position=(x_pos, y_pos), align=config.align,
            audio_tags=config.audio_tags, sub_widget=True,
            text_colors=config.text_colors, font=config.font,
            font_size=config.font_size)
        size = (config.sizes
                 if isinstance(config.sizes[0], int)
                 else config.sizes[column][row])
        on_click = (config.on_click[column][row]
                        if config.on_click is not None else None)
        on_release = (config.on_release[column][row]
                         if config.on_release is not None else None)

        return TextRectClickButton(
            config_, size, config.texts[column][row], config.radius,
            config.colors, config.text_align, config.padding, on_click,
            on_release)
