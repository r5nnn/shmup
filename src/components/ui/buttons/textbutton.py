"""Module for displaying text buttons on the screen."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING, override

from src.components.ui.buttons.buttonbases import (
    TextButtonBaseMixin,
    RectButtonBaseMixin,
    _BaseButtonConfig,
)
from src.components.ui.buttons.inputmixins import checktoggle
from src.components.ui.buttons.textmixins import (
    ToggleTextMixin,
    ClickTextMixin,
)

if TYPE_CHECKING:
    import pygame
    from src.core.types import Align, Colors


@dataclass(kw_only=True)
class TextButtonConfig(_BaseButtonConfig):
    text_colors: Colors | None = None
    font: pygame.font.Font | None = None
    font_size: int = 32
    wrap_width: int | None = None
    wrap_padding: int = 0
    antialias: bool = False


class TextToggleButton(TextButtonBaseMixin, ToggleTextMixin):
    def __init__(
        self,
        config: TextButtonConfig,
        text: str | tuple[str] | None = None,
        start_text: int = 0,
        on_toggle_on: Callable | None = None,
        on_toggle_off: Callable | None = None,
        *,
        requires_state: bool = False,
    ):
        TextButtonBaseMixin.__init__(
            self,
            config.position,
            config.align,
            config.audio_tags,
            sub_widget=config.sub_widget,
        )
        ToggleTextMixin.__init__(
            self,
            text,
            start_text,
            config.text_colors,
            config.font,
            config.font_size,
            config.wrap_width,
            config.wrap_padding,
            padding=0,
            text_align=config.align,
            on_toggle_on=on_toggle_on,
            on_toggle_off=on_toggle_off,
            antialias=config.antialias,
            requires_state=requires_state,
        )
        self.rect = self.text_rect
        self.align_rect()
        self._width, self._height = self.text_rect.size
        self.sub_widgets.append(self.text_object)

    @override
    def update(self) -> None:
        ToggleTextMixin.update(self)
        if self.requires_realignment:
            self.requires_realignment = False
            self.align_rect()

    def update_hover(self) -> None:
        super().update_hover()

    @checktoggle
    def update_idle(self) -> None:
        super().update_idle()

    @override
    def align_rect(self) -> None:
        TextButtonBaseMixin.align_rect(self)


class TextClickButton(TextButtonBaseMixin, ClickTextMixin):
    def __init__(
        self,
        config: TextButtonConfig,
        text: str,
        on_click: Callable | None = None,
        on_release: Callable | None = None,
    ):
        TextButtonBaseMixin.__init__(
            self,
            config.position,
            config.align,
            config.audio_tags,
            sub_widget=config.sub_widget,
        )
        ClickTextMixin.__init__(
            self,
            text,
            config.text_colors,
            config.font,
            config.font_size,
            config.wrap_width,
            config.wrap_padding,
            padding=0,
            on_click=on_click,
            on_release=on_release,
            antialias=config.antialias,
        )
        self.rect = self.text_rect
        self.align_rect()
        self._width, self._height = self.rect.size
        self.sub_widgets.append(self.text_object)

    @override
    def update(self) -> None:
        ClickTextMixin.update(self)
        if self.requires_realignment:
            self.requires_realignment = False
            self.align_rect()

    def align_rect(self) -> None:
        TextButtonBaseMixin.align_rect(self)


class TextRectToggleButton(RectButtonBaseMixin, ToggleTextMixin):
    def __init__(
        self,
        config: TextButtonConfig,
        size: tuple[int, int],
        text: list[str] | str | None = None,
        start_text: int = 0,
        text_align: Align | None = None,
        padding: int = 20,
        radius: int = 0,
        colors: Colors | None = None,
        on_toggle_on: Callable | None = None,
        on_toggle_off: Callable | None = None,
        *,
        requires_state: bool = False,
    ):
        RectButtonBaseMixin.__init__(
            self,
            config.position,
            size,
            config.align,
            radius,
            colors,
            config.audio_tags,
            sub_widget=config.sub_widget,
        )
        ToggleTextMixin.__init__(
            self,
            text,
            start_text,
            config.text_colors,
            config.font,
            config.font_size,
            config.wrap_width,
            config.wrap_padding,
            padding,
            text_align,
            on_toggle_on,
            on_toggle_off,
            antialias=config.antialias,
            requires_state=requires_state,
        )
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
        RectButtonBaseMixin.update(self)
        ToggleTextMixin.update(self)
        if self.text_label_requires_realignment:
            self.text_label_requires_realignment = False
            self.align_text()
        if self.requires_realignment:
            self.requires_realignment = False
            self.align_rect()

    def blit(self) -> None:
        RectButtonBaseMixin.blit(self)

    def align_rect(self) -> None:
        RectButtonBaseMixin.align_rect(self)
        ToggleTextMixin.align_rect(self)


class TextRectClickButton(RectButtonBaseMixin, ClickTextMixin):
    def __init__(
        self,
        config: TextButtonConfig,
        size: tuple[int, int],
        text: str,
        text_align: Align | None = None,
        padding: int = 20,
        radius: int = 0,
        colors: Colors = None,
        on_click: Callable | None = None,
        on_release: Callable | None = None,
    ):
        RectButtonBaseMixin.__init__(
            self,
            config.position,
            size,
            config.align,
            radius,
            colors,
            config.audio_tags,
            sub_widget=config.sub_widget,
        )
        ClickTextMixin.__init__(
            self,
            text,
            config.text_colors,
            config.font,
            config.font_size,
            config.wrap_width,
            config.wrap_padding,
            padding,
            text_align,
            on_click,
            on_release,
            antialias=config.antialias,
        )
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
        RectButtonBaseMixin.update(self)
        ClickTextMixin.update(self)
        if self.requires_realignment:
            self.requires_realignment = False
            self.align_rect()

    def blit(self) -> None:
        RectButtonBaseMixin.blit(self)

    def align_rect(self) -> None:
        RectButtonBaseMixin.align_rect(self)
        ClickTextMixin.align_rect(self)
