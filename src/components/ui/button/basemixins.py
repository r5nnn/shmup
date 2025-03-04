from __future__ import annotations

from abc import ABC
from typing import override, TYPE_CHECKING

import pygame

from src.components.ui.widgetutils import WidgetBase
from src.core import screen
from src.core.constants import RectAlignments, PRIMARY, SECONDARY, ACCENT

if TYPE_CHECKING:
    from src.components.ui.button._types import _Colors


class RectButtonMixin(WidgetBase):
    def __init__(self, position: tuple[int, int], size: tuple[int, int],
                 align: RectAlignments = "topleft", radius: int = 0,
                 colors: _Colors = None, click_audio_tag: str = "click",
                 release_audio_tag: str = "click", *, sub_widget: bool = False):
        super().__init__(position, align, sub_widget=sub_widget)
        self._width, self._height = size
        if colors is None:
            self.colors = (PRIMARY, SECONDARY, ACCENT)
        elif (isinstance(colors, (tuple, pygame.Color)) and
                len(colors) == 3):
            self.colors = colors
        else:
            self.colors = (colors,) * 3
        self._color = self.colors[0]
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._align_rect()
        self.radius = radius
        self.click_audio_tag = click_audio_tag
        self.release_audio_tag = release_audio_tag

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._rect.width = value
        self._width = value
        self.requires_realignment = True

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._rect.height = value
        self._height = value
        self.requires_realignment = True

    @override
    def contains(self, x: int, y: int) -> bool | None:
        super().contains(x, y)
        return self._rect.collidepoint(x, y)

    @override
    def blit(self) -> None:
        pygame.draw.rect(screen, self._color, self._rect,
                         border_radius=self.radius)

    @override
    def update(self) -> None:
        super().update()
        if self.requires_realignment:
            self._align_rect()

    def _align_rect(self) -> None:
        setattr(self._rect, self._align, (self._x, self._y))
        self._x, self._y = self._rect.topleft


class TextButtonBaseMixin(WidgetBase, ABC):
    # Defined when integrated with a button class.
    _rect: pygame.Rect = ...
    _width: int = ...
    _height: int = ...

    def __init__(self, position: tuple[int, int],
                 align: RectAlignments = "topleft",
                 click_audio_tag: str = "click",
                 release_audio_tag: str = "click", *,
                 sub_widget: bool = False):
        super().__init__(position, align, sub_widget=sub_widget)
        self.click_audio_tag = click_audio_tag
        self.release_audio_tag = release_audio_tag

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def _align_rect(self) -> None:
        setattr(self._rect, self._align, (self._x, self._y))
        self._x, self._y = self._rect.topleft

    @override
    def contains(self, x: int, y: int) -> bool | None:
        super().contains(x, y)
        return self._rect.collidepoint(x, y)


class ImageButtonBaseMixin(WidgetBase, ABC):
    # Defined when integrated with a button class.
    _rect: pygame.Rect = ...
    _image_mask: pygame.Mask = ...
    _width: int = ...
    _height: int = ...
    _image: pygame.Surface = ...

    def __init__(self, position: tuple[int, int],
                 align: RectAlignments = "topleft",
                 click_audio_tag: str = "click",
                 release_audio_tag: str = "click", *,
                 sub_widget: bool = False):
        super().__init__(position, align, sub_widget=sub_widget)
        self.click_audio_tag = click_audio_tag
        self.release_audio_tag = release_audio_tag

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def _align_rect(self) -> None:
        setattr(self._rect, self._align, (self._x, self._y))
        self._x, self._y = self._rect.topleft

    @override
    def contains(self, x: int, y: int) -> bool | None:
        super().contains(x, y)
        relx, rely = x - self._rect.x, y - self._rect.y
        return (self._rect.collidepoint(x, y) and
                self._image_mask.get_at((relx, rely)))