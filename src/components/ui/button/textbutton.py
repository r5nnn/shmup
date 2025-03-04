"""Module for displaying text buttons on the screen."""
from __future__ import annotations

from typing import Callable, TYPE_CHECKING, override

from src.components.ui.button.basemixins import (
    TextButtonBaseMixin, RectButtonMixin)
from src.components.ui.button.inputmixins import checktoggle
from src.components.ui.button.textmixins import (
    ToggleTextMixin, ClickTextMixin)
from src.components.ui.widgetutils import WidgetBase

if TYPE_CHECKING:
    import pygame
    from src.core.constants import RectAlignments
    from src.components.ui.button._types import _Align, _Colors


class TextToggleButton(TextButtonBaseMixin, ToggleTextMixin):
    def __init__(self, position: tuple[int, int],
                 text: str, align: RectAlignments = "topleft",
                 start_text: int = 0, text_colors: _Colors = None,
                 text_align: _Align | None = None,
                 font: pygame.font.Font | None = None, font_size: int = 32,
                 on_toggle_on: Callable | None = None,
                 on_toggle_off: Callable | None = None,
                 click_audio_tag: str = "click",
                 release_audio_tag: str = "click", *,
                 requires_state: bool = False, sub_widget: bool = False):
        TextButtonBaseMixin.__init__(self, position, align, click_audio_tag,
                                  release_audio_tag, sub_widget=sub_widget)
        ToggleTextMixin.__init__(self, text, start_text, text_colors, font,
                                      font_size, text_align, 0, on_toggle_on,
                                      on_toggle_off,
                                      requires_state=requires_state)
        self._rect = self.text_rect
        self._width, self._height = self.text_rect.size
        self._align_rect()

    @override
    def update(self) -> None:
        WidgetBase.update(self)
        ToggleTextMixin.update(self)
        if self.requires_realignment:
            self._align_text()

    @checktoggle
    def update_hover(self) -> None:
        super().update_hover()

    @checktoggle
    def update_idle(self) -> None:
        super().update_idle()

    @override
    def blit(self) -> None:
        ToggleTextMixin.blit(self)

    @override
    def _align_rect(self) -> None:
        TextButtonBaseMixin._align_rect(self)
        ToggleTextMixin._align_rect(self)


class TextClickButton(TextButtonBaseMixin, ClickTextMixin):
    def __init__(self, position: tuple[int, int],
                 text: str, align: RectAlignments = "topleft",
                 text_colors: _Colors = None,
                 text_align: _Align | None = None,
                 font: pygame.font.Font | None = None, font_size: int = 32,
                 on_click: Callable | None = None,
                 on_release: Callable | None = None,
                 click_audio_tag: str = "click",
                 release_audio_tag: str = "click", *,
                 sub_widget: bool = False):
        TextButtonBaseMixin.__init__(self, position, align, click_audio_tag,
                                      release_audio_tag, sub_widget=sub_widget)
        ClickTextMixin.__init__(self, text, text_colors, text_align, 0, font,
                                font_size, on_click, on_release)
        self._rect = self.text_rect
        self._width, self._height = self._rect.size
        self._align_rect()

    @override
    def update(self) -> None:
        WidgetBase.update(self)
        ClickTextMixin.update(self)
        if self.requires_realignment:
            self._align_text()

    @override
    def blit(self) -> None:
        ClickTextMixin.blit(self)

    def _align_rect(self) -> None:
        TextButtonBaseMixin._align_rect(self)
        ClickTextMixin._align_rect(self)


class TextRectToggleButton(RectButtonMixin, ToggleTextMixin):
    def __init__(self, position: tuple[int, int], size: tuple[int, int],
                 text: str, align: RectAlignments = "topleft", radius: int = 0,
                 colors: _Colors = None, click_audio: str = "click",
                 release_audio: str = "click", start_text: int = 0,
                 text_colors: _Colors = None,
                 font: pygame.font.Font | None = None, font_size: int = 32,
                 text_align: _Align | None = None, padding: int = 20,
                 on_toggle_on: Callable | None = None,
                 on_toggle_off: Callable | None = None, *,
                 requires_state: bool = False, sub_widget: bool = False):
        RectButtonMixin.__init__(self, position, size, align, radius, colors,
                                 click_audio, release_audio,
                                 sub_widget=sub_widget)
        ToggleTextMixin.__init__(self, text, start_text, text_colors, font,
                                 font_size, text_align, padding, on_toggle_on,
                                 on_toggle_off, requires_state=requires_state)

    def toggle_on(self) -> None:
        super().toggle_on()
        self._color = self.colors[2]

    @checktoggle
    def update_hover(self) -> None:
        super().update_hover()
        self._color = self.colors[1]

    @checktoggle
    def update_idle(self) -> None:
        super().update_idle()
        self._color = self.colors[0]

    def update(self) -> None:
        ToggleTextMixin.update(self)
        RectButtonMixin.update(self)
        if self.requires_realignment:
            self._align_rect()

    def blit(self) -> None:
        RectButtonMixin.blit(self)
        ToggleTextMixin.blit(self)

    def _align_rect(self) -> None:
        RectButtonMixin._align_rect(self)
        self._align_text()


class TextRectClickButton(RectButtonMixin, ClickTextMixin):
    def __init__(self, position: tuple[int, int], size: tuple[int, int],
                 text: str, align: RectAlignments = "topleft", radius: int = 0,
                 colors: _Colors = None, click_audio: str = "click",
                 release_audio: str = "click", text_colors: _Colors = None,
                 font: pygame.font.Font | None = None, font_size: int = 32,
                 text_align: _Align | None = None, padding: int = 20,
                 on_click: Callable | None = None,
                 on_release: Callable | None = None, *,
                 sub_widget: bool = False):
        RectButtonMixin.__init__(self, position, size, align, radius, colors,
                                 click_audio, release_audio,
                                 sub_widget=sub_widget)
        ClickTextMixin.__init__(self, text, text_colors, text_align, padding,
                                font, font_size, on_click, on_release)

    def update_click(self) -> None:
        super().update_click()
        self._color = self.colors[2]

    def update_hover(self) -> None:
        super().update_hover()
        self._color = self.colors[1]

    def update_idle(self) -> None:
        super().update_idle()
        self._color = self.colors[0]

    def update(self) -> None:
        ClickTextMixin.update(self)
        RectButtonMixin.update(self)
        if self.requires_realignment:
            self._align_rect()

    def blit(self) -> None:
        RectButtonMixin.blit(self)
        ClickTextMixin.blit(self)

    def _align_rect(self) -> None:
        RectButtonMixin._align_rect(self)
        self._align_text()
