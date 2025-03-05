"""Module for displaying text buttons on the screen."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING, override

from src.components.ui.buttons.basemixins import (
    TextButtonBaseMixin, RectButtonMixin, _BaseButtonConfig)
from src.components.ui.buttons.inputmixins import checktoggle
from src.components.ui.buttons.textmixins import (
    ToggleTextMixin, ClickTextMixin)
from src.components.ui.widgetutils import WidgetBase

if TYPE_CHECKING:
    import pygame
    from src.components.ui.buttons._types import _Align, _Colors


@dataclass(kw_only=True)
class TextButtonConfig(_BaseButtonConfig):
    text_colors: _Colors | None = None
    font: pygame.font.Font | None = None
    font_size: int = 32


class TextToggleButton(TextButtonBaseMixin, ToggleTextMixin):
    def __init__(self, config: TextButtonConfig, text: str | tuple[str],
                 start_text: int = 0, on_toggle_on: Callable | None = None,
                 on_toggle_off: Callable | None = None, *,
                 requires_state: bool = False):
        TextButtonBaseMixin.__init__(
            self, config.position, (config.align[0] + config.align[1]
                                    if config.align is not None
                                    else "topleft"),
            config.audio_tags, sub_widget=config.sub_widget)
        ToggleTextMixin.__init__(self, text, start_text, config.text_colors,
                                 config.font, config.font_size, config.align,
                                 0, on_toggle_on, on_toggle_off,
                                 requires_state=requires_state)
        self.rect = self.text_rect
        self.align_rect()
        self._width, self._height = self.text_rect.size

    @override
    def update(self) -> None:
        WidgetBase.update(self)
        if self.requires_realignment:
            self.align_rect()
        ToggleTextMixin.update(self)

    def update_hover(self) -> None:
        super().update_hover()

    @checktoggle
    def update_idle(self) -> None:
        super().update_idle()

    @override
    def blit(self) -> None:
        ToggleTextMixin.blit(self)

    @override
    def align_rect(self) -> None:
        TextButtonBaseMixin.align_rect(self)


class TextClickButton(TextButtonBaseMixin, ClickTextMixin):
    def __init__(self, config: TextButtonConfig, text: str,
                 on_click: Callable | None = None,
                 on_release: Callable | None = None):
        TextButtonBaseMixin.__init__(
            self, config.position, (config.align[0] + config.align[1]
                                    if config.align is not None
                                    else "topleft"),
            config.audio_tags, sub_widget=config.sub_widget)
        ClickTextMixin.__init__(
            self, text, config.text_colors, config.align, 0, config.font,
            config.font_size, on_click, on_release)
        self.rect = self.text_rect
        self.align_rect()
        self._width, self._height = self.rect.size

    @override
    def update(self) -> None:
        WidgetBase.update(self)
        if self.requires_realignment:
            self.requires_realignment = False
            self.align_rect()
        ClickTextMixin.update(self)

    @override
    def blit(self) -> None:
        ClickTextMixin.blit(self)

    def align_rect(self) -> None:
        TextButtonBaseMixin.align_rect(self)


class TextRectToggleButton(RectButtonMixin, ToggleTextMixin):
    def __init__(self, config: TextButtonConfig, size: tuple[int, int],
                 text: str, radius: int = 0, colors: _Colors = None,
                 start_text: int = 0, text_align: _Align | None = None,
                 padding: int = 20, on_toggle_on: Callable | None = None,
                 on_toggle_off: Callable | None = None, *,
                 requires_state: bool = False):
        RectButtonMixin.__init__(
            self, config.position, size, (config.align[0] + config.align[1]
                                          if config.align is not None
                                          else "topleft"),
            radius, colors, config.audio_tags, sub_widget=config.sub_widget)
        ToggleTextMixin.__init__(
            self, text, start_text, config.text_colors, config.font,
            config.font_size, text_align, padding, on_toggle_on, on_toggle_off,
            requires_state=requires_state)
        self.align_rect()

    def toggle_on(self) -> None:
        super().toggle_on()
        self.color = self.colors[2]

    def update_hover(self) -> None:
        super().update_hover()
        self.color = self.colors[1]

    @checktoggle
    def update_idle(self) -> None:
        super().update_idle()
        self.color = self.colors[0]

    def update(self) -> None:
        RectButtonMixin.update(self)
        ToggleTextMixin.update(self)

    def blit(self) -> None:
        RectButtonMixin.blit(self)
        ToggleTextMixin.blit(self)

    def align_rect(self) -> None:
        RectButtonMixin.align_rect(self)
        ToggleTextMixin.align_rect(self)


class TextRectClickButton(RectButtonMixin, ClickTextMixin):
    def __init__(self, config: TextButtonConfig, size: tuple[int, int], text: str,
                 radius: int = 0, colors: _Colors = None,
                 text_align: _Align | None = None, padding: int = 20,
                 on_click: Callable | None = None,
                 on_release: Callable | None = None):
        RectButtonMixin.__init__(
            self, config.position, size, (config.align[0] + config.align[1]
                                          if config.align is not None
                                          else "topleft"),
            radius, colors, config.audio_tags, sub_widget=config.sub_widget)
        ClickTextMixin.__init__(
            self, text, config.text_colors, text_align, padding, config.font,
            config.font_size, on_click, on_release)
        self.align_rect()

    def update_click(self) -> None:
        super().update_click()
        self.color = self.colors[2]

    def update_hover(self) -> None:
        super().update_hover()
        self.color = self.colors[1]

    def update_idle(self) -> None:
        super().update_idle()
        self.color = self.colors[0]

    def update(self) -> None:
        RectButtonMixin.update(self)
        ClickTextMixin.update(self)

    def blit(self) -> None:
        RectButtonMixin.blit(self)
        ClickTextMixin.blit(self)

    def align_rect(self) -> None:
        RectButtonMixin.align_rect(self)
        ClickTextMixin.align_rect(self)
