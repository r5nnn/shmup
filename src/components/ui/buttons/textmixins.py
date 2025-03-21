from __future__ import annotations

from typing import Callable, TYPE_CHECKING

import pygame

from src.components.ui import Text
from src.components.ui.buttons.inputmixins import (
    ClickInputMixin,
    ToggleInputMixin,
)

if TYPE_CHECKING:
    from src.core.types import Colors, Align


class TextLabelMixin:
    rect: pygame.Rect = ...
    requires_realignment: bool = ...

    def __init__(
        self,
        text: str,
        text_colors: Colors = None,
        font: pygame.font.Font | None = None,
        font_size: int = 32,
        wrap_width: int | None = None,
        wrap_padding: int = 0,
        padding: int = 20,
        text_align: Align | None = None,
        *,
        antialias: bool = False,
    ):
        if isinstance(text_colors, list):
            self.text_colors = text_colors
        else:
            if text_colors is None:
                text_colors = pygame.Color("white")
            self.text_colors = (text_colors,) * 3
        self.text_color = self.text_colors[0]
        self.text_object = Text(
            (0, 0),
            text,
            font,
            font_size,
            self.text_color,
            wrap_width=wrap_width,
            wrap_padding=wrap_padding,
            antialias=antialias,
            sub_widget=True,
        )
        self.text_align = text_align
        self.text_rect = self.text_object.rect
        self.padding = padding
        self.requires_realignment = True
        self.text_label_requires_realignment = True

    def align_text(self) -> None:
        self.text_rect = self.text_object.rect
        self.text_rect.center = self.rect.center
        if self.text_align is not None:
            horisontal, vertical = self.text_align
            if horisontal is not None:
                if horisontal == "left":
                    self.text_rect.left = self.rect.left + self.padding
                else:
                    self.text_rect.right = self.rect.right - self.padding
            if vertical is not None:
                if vertical == "top":
                    self.text_rect.top = self.rect.top + self.padding
                else:
                    self.text_rect.bottom = self.rect.bottom - self.padding
        self.text_object.x, self.text_object.y = self.text_rect.topleft

    def align_rect(self) -> None:
        self.align_text()

    def update(self) -> None:
        if self.text_object.requires_realignment:
            self.text_label_requires_realignment = True


class ToggleTextMixin(ToggleInputMixin, TextLabelMixin):
    def __init__(
        self,
        text: str | list[str] | None = None,
        start_text: int = 0,
        text_colors: Colors = None,
        font: pygame.font.Font | None = None,
        font_size: int = 32,
        wrap_width: int | None = None,
        wrap_padding: int = 0,
        padding: int = 20,
        text_align: Align | None = None,
        on_toggle_on: Callable | None = None,
        on_toggle_off: Callable | None = None,
        *,
        antialias: bool = False,
        requires_state: bool = False,
    ):
        ToggleInputMixin.__init__(
            self, on_toggle_on, on_toggle_off, requires_state=requires_state
        )
        self.texts = (
            ["False", "True"]
            if text is None
            else text if isinstance(text, list) else [text, text]
        )
        TextLabelMixin.__init__(
            self,
            self.texts[start_text],
            text_colors,
            font,
            font_size,
            wrap_width,
            wrap_padding,
            padding,
            text_align,
            antialias=antialias,
        )

    def toggle_on(self) -> None:
        super().toggle_on()
        self.text_object.color = self.text_colors[2]
        self.text_object.text = self.texts[1]

    def toggle_off(self) -> None:
        super().toggle_off()
        # there is no hover text, so no need to update text in the idle method
        self.text_object.text = self.texts[0]

    def update_hover(self) -> None:
        super().update_hover()
        self.text_object.color = self.text_colors[1]

    def update_idle(self) -> None:
        super().update_idle()
        self.text_object.color = self.text_colors[0]

    def update(self) -> None:
        ToggleInputMixin.update(self)
        TextLabelMixin.update(self)


class ClickTextMixin(ClickInputMixin, TextLabelMixin):
    def __init__(
        self,
        text: str,
        text_colors: Colors = None,
        font: pygame.font.Font | None = None,
        font_size: int = 32,
        wrap_width: int | None = None,
        wrap_padding: int = 0,
        padding: int = 20,
        text_align: Align | None = None,
        on_click: Callable | None = None,
        on_release: Callable | None = None,
        *,
        antialias: bool = False,
    ):
        ClickInputMixin.__init__(self, on_click, on_release)
        TextLabelMixin.__init__(
            self,
            text,
            text_colors,
            font,
            font_size,
            wrap_width,
            wrap_padding,
            padding,
            text_align,
            antialias=antialias,
        )

    def update(self) -> None:
        ClickInputMixin.update(self)
        TextLabelMixin.update(self)

    def update_idle(self) -> None:
        super().update_idle()
        self.text_object.color = self.text_colors[0]

    def update_hover(self) -> None:
        super().update_hover()
        self.text_object.color = self.text_colors[1]

    def update_click(self) -> None:
        super().update_click()
        self.text_object.color = self.text_colors[2]
