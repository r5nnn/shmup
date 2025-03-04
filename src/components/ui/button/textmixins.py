from __future__ import annotations

from typing import Callable
from typing import TYPE_CHECKING

import pygame

from src.components.ui import Text
from src.components.ui.button.inputmixins import (
    ToggleInputMixin, ClickInputMixin)

if TYPE_CHECKING:
    from src.components.ui.button._types import _Colors, _Align


class TextLabelMixin:
    _rect: pygame.Rect = ...
    requires_realignment: bool = ...

    def __init__(self, text: str,
                 text_colors: _Colors = None,
                 text_align: _Align | None = None, padding: int = 20,
                 font: pygame.font.Font | None = None, font_size: int = 32):
        if (isinstance(text_colors, (tuple, pygame.Color)) and
                len(text_colors) == 3):
            self.text_colors = text_colors
        else:
            if text_colors is None:
                text_colors = pygame.Color("white")
            self.text_colors = (text_colors,) * 3
        self._text_color = self.text_colors[0]
        self.text_label = Text((0, 0), text, font, font_size, self._text_color,
                               sub_widget=True)
        self._text_align = text_align
        self.text_rect = self.text_label.rect
        self.padding = padding
        self.requires_realignment = True

    def _align_text(self) -> None:
        self.text_rect.center = self._rect.center
        if self._text_align is not None:
            horisontal, vertical = self._text_align
            if horisontal is not None:
                if horisontal == "left":
                    self.text_rect.left = self._rect.left + self.padding
                else:
                    self.text_rect.right = self._rect.right - self.padding
            if vertical is not None:
                if vertical == "top":
                    self.text_rect.top = self._rect.top + self.padding
                else:
                    self.text_rect.bottom = self._rect.bottom - self.padding
        self.text_label.x, self.text_label.y = self.text_rect.topleft

    def _align_rect(self) -> None:
        self._align_text()

    def blit(self) -> None:
        self.text_label.blit()

    def update(self) -> None:
        if self.text_label.requires_realignment:
            self.requires_realignment = True
        self.text_label.update()


class ToggleTextMixin(ToggleInputMixin, TextLabelMixin):
    def __init__(self, text: str, start_text: int = 0,
                 text_colors: _Colors = None,
                 font: pygame.font.Font | None = None, font_size: int = 32,
                 text_align: _Align | None = None, padding: int = 20,
                 on_toggle_on: Callable | None = None,

                 on_toggle_off: Callable | None = None, *,
                 requires_state: bool = False):
        ToggleInputMixin.__init__(self, on_toggle_on, on_toggle_off,
                                  requires_state=requires_state)
        self.text_tuple = text if isinstance(text, tuple) else (text, text)
        TextLabelMixin.__init__(self, self.text_tuple[start_text], text_colors,
                                text_align, padding, font, font_size)

    def toggle_on(self) -> None:
        super().toggle_on()
        self.text_label.color = self.text_colors[2]
        self.text_label.text = self.text_tuple[0]

    def toggle_off(self) -> None:
        super().toggle_off()
        # there is no hover text, so no need to update text in the idle method
        self.text_label.text = self.text_tuple[1]

    def update_hover(self) -> None:
        super().update_hover()
        self.text_label.color = self.text_colors[1]

    def update_idle(self) -> None:
        super().update_idle()
        self.text_label.color = self.text_colors[0]

    def update(self) -> None:
        ToggleInputMixin.update(self)
        TextLabelMixin.update(self)


class ClickTextMixin(ClickInputMixin, TextLabelMixin):
    def __init__(self, text: str,
                 text_colors: _Colors = None,
                 text_align: _Align | None = None, padding: int = 20,
                 font: pygame.font.Font | None = None, font_size: int = 32,
                 on_click: Callable | None = None,
                 on_release: Callable | None = None):
        ClickInputMixin.__init__(self, on_click, on_release)
        TextLabelMixin.__init__(self, text, text_colors, text_align, padding,
                                font, font_size)

    def update(self) -> None:
        ClickInputMixin.update(self)
        TextLabelMixin.update(self)

    def update_idle(self) -> None:
        super().update_idle()
        self.text_label.color = self.text_colors[0]

    def update_hover(self) -> None:
        super().update_hover()
        self.text_label.color = self.text_colors[1]

    def update_click(self) -> None:
        super().update_click()
        self.text_label.color = self.text_colors[2]
