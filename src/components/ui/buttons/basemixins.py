from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import override, TYPE_CHECKING

import pygame

from src.components.ui.widgetutils import WidgetBase
from src.core import screen
from src.core.constants import PRIMARY, SECONDARY, ACCENT

if TYPE_CHECKING:
    from src.components.ui import Text
    from src.components.ui.buttons._types import _Colors, _Align


@dataclass(kw_only=True)
class _BaseButtonConfig:
    position: tuple[int, int]
    align: _Align | None = None
    audio_tags: list[str | None] | None = None
    sub_widget: bool = False


class RectButtonMixin(WidgetBase):
    def __init__(self, position: tuple[int, int], size: tuple[int, int],
                 align: str = "topleft", radius: int = 0,
                 colors: _Colors = None,
                 audio_tags: list[str | None] | None = None, *,
                 sub_widget: bool = False):
        super().__init__(position, align, sub_widget=sub_widget)
        self._width, self._height = size
        if colors is None:
            self.colors = [PRIMARY, SECONDARY, ACCENT]
        elif isinstance(colors, list):
            self.colors = colors
        else:
            self.colors = (colors,) * 3
        self.color = self.colors[0]
        self.rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self.radius = radius
        self.audio_tags = ["click", None, "click"] if audio_tags is None else (
            audio_tags)
        self.requires_realignment = True

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self.rect.width = value
        self._width = value
        self.requires_realignment = True

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self.rect.height = value
        self._height = value
        self.requires_realignment = True

    @override
    def contains(self, x: int, y: int) -> bool | None:
        super().contains(x, y)
        return self.rect.collidepoint(x, y)

    @override
    def blit(self) -> None:
        pygame.draw.rect(screen, self.color, self.rect,
                         border_radius=self.radius)

    @override
    def update(self) -> None:
        super().update()
        if self.requires_realignment:
            self.align_rect()

    def align_rect(self) -> None:
        setattr(self.rect, self._align, (self._x, self._y))
        self._x, self._y = self.rect.topleft
        self.requires_realignment = False


class TextButtonBaseMixin(WidgetBase, ABC):
    # Defined when integrated with a buttons class.
    rect: pygame.Rect = ...
    _width: int = ...
    _height: int = ...
    text_object: Text = ...

    def __init__(self, position: tuple[int, int], align: str = "topleft",
                 audio_tags: list[str | None] | None = None, *,
                 sub_widget: bool = False):
        super().__init__(position, align, sub_widget=sub_widget)
        self.audio_tags = ["click", None, "click"] if audio_tags is None else (
            audio_tags)

    @override
    def contains(self, x: int, y: int) -> bool | None:
        super().contains(x, y)
        return self.rect.collidepoint(x, y)

    def align_rect(self) -> None:
        setattr(self.rect, self._align, (self._x, self._y))
        self._x, self._y = self.rect.topleft
        self.text_object.x, self.text_object.y = self._x, self._y
        self.requires_realignment = False


class ImageButtonBaseMixin(WidgetBase, ABC):
    # Defined when integrated with a buttons class.
    rect: pygame.Rect = ...
    image_mask: pygame.Mask = ...
    _width: int = ...
    _height: int = ...
    image: pygame.Surface = ...
    use_mask: bool = ...

    def __init__(self, position: tuple[int, int], align: str = "topleft",
                 audio_tags: list[str | None] | None = None, *,
                 sub_widget: bool = False):
        super().__init__(position, align, sub_widget=sub_widget)
        self.audio_tags = ["click", None, "click"] if audio_tags is None else (
            audio_tags)

    def align_rect(self) -> None:
        setattr(self.rect, self._align, (self._x, self._y))
        self._x, self._y = self.rect.topleft

    @override
    def contains(self, x: int, y: int) -> bool | None:
        super().contains(x, y)
        if self.rect.collidepoint(x, y):
            if self.use_mask:
                relx, rely = x - self.rect.x, y - self.rect.y
                return bool(self.image_mask.get_at((relx, rely)))
            return True
        return False
