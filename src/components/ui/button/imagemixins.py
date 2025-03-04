from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import pygame

from src.components.ui.button.inputmixins import ToggleInputMixin, ClickInputMixin
from src.core import screen

if TYPE_CHECKING:
    from src.components.ui.button._types import _Align


class ImageLabelMixin:
    _rect: pygame.Rect = ...
    requires_realignment: bool = ...

    def __init__(self, images: tuple[pygame.Surface] | pygame.Surface,
                 mask_image: pygame.Surface | False | None = None,
                 image_align: _Align = None, padding: int = 20):
        self._images = images if isinstance(images, tuple) else (images,) * 3
        self._image = self._images[0]
        self._use_mask = True
        if mask_image is None:
            self._image_mask = pygame.mask.from_surface(self._images[0])
        elif mask_image is False:
            self._use_mask = False
        else:
            self._image_mask = mask_image
        self._image_align = image_align
        self._padding = padding
        self._image_rect = self._image.get_rect()
        self.requires_realignment = True

    def _align_image(self) -> None:
        self._image_rect.center = self._rect.center
        if self._image_align is not None:
            horisontal, vertical = self._image_align
            if horisontal is not None:
                if horisontal == "left":
                    self._image_rect.left = self._rect.left + self._padding
                else:
                    self._image_rect.right = self._rect.right - self._padding
            if vertical is not None:
                if vertical == "top":
                    self._image_rect.top = self._rect.top + self._padding
                else:
                    self._image_rect.bottom = self._rect.bottom - self._padding

    def _align_rect(self) -> None:
        self._align_image()

    def blit(self) -> None:
        screen.blit(self._image, self._image_rect)


class ToggleImageMixin(ToggleInputMixin, ImageLabelMixin):
    def __init__(self, images: tuple[pygame.Surface] | pygame.Surface,
                 mask_image:  pygame.Surface | None = None,
                 image_align: _Align = None, padding: int = 20,
                 on_toggle_on: Callable | None = None,
                 on_toggle_off: Callable | None = None, *,
                 requires_state: bool = False):
        ToggleInputMixin.__init__(self, on_toggle_on, on_toggle_off,
                                  requires_state=requires_state)
        ImageLabelMixin.__init__(self, images, mask_image, image_align,
                                 padding)

    def toggle_on(self) -> None:
        super().toggle_on()
        self._image = self._images[2]

    def update_hover(self) -> None:
        super().update_hover()
        self._image = self._images[1]

    def update_idle(self) -> None:
        super().update_idle()
        self._image = self._images[0]


class ClickImageMixin(ClickInputMixin, ImageLabelMixin):
    def __init__(self, images: tuple[pygame.Surface] | pygame.Surface,
                 image_mask: pygame.Surface | False | None = None,
                 image_align: _Align = None, padding: int = 20,
                 on_click: Callable | None = None,
                 on_release: Callable | None = None):
        ClickInputMixin.__init__(self, on_click, on_release)
        ImageLabelMixin.__init__(self, images, image_mask, image_align,
                                 padding)

    def update_idle(self) -> None:
        super().update_idle()
        self._image = self._images[0]

    def update_hover(self) -> None:
        super().update_hover()
        self._image = self._images[1]

    def update_click(self) -> None:
        super().update_click()
        self._image = self._images[2]
