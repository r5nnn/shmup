from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import pygame

from src.components.ui.buttons.inputmixins import ToggleInputMixin, ClickInputMixin
from src.core import screen, get_sprites, spritesheet_paths

if TYPE_CHECKING:
    from src.components.ui.buttons._types import _Align, _Images


class ImageLabelMixin:
    rect: pygame.Rect = ...
    requires_realignment: bool = ...

    def __init__(self, images: _Images, scale_by: int | None = None,
                 mask_image: pygame.Surface | str | False | None = None,
                 image_align: _Align = None, padding: int = 20):
        if isinstance(images, str):
            images = get_sprites(spritesheet_paths(images))
        self.images = images if isinstance(images, tuple) else (images,) * 3
        if scale_by is not None:
            self.images = tuple(pygame.transform.scale_by(image, scale_by)
                                 for image in self.images)
        self.image = self.images[0]
        self.use_mask = True
        if mask_image is None:
            self.image_mask = pygame.mask.from_surface(self.images[0])
        elif mask_image is False:
            self.use_mask = False
        else:
            self.image_mask = mask_image
        self.image_align = image_align
        self.padding = padding
        self.image_rect = self.image.get_rect()
        self.requires_realignment = True

    def align_image(self) -> None:
        self.image_rect.center = self.rect.center
        if self.image_align is not None:
            horisontal, vertical = self.image_align
            if horisontal is not None:
                if horisontal == "left":
                    self.image_rect.left = self.rect.left + self.padding
                else:
                    self.image_rect.right = self.rect.right - self.padding
            if vertical is not None:
                if vertical == "top":
                    self.image_rect.top = self.rect.top + self.padding
                else:
                    self.image_rect.bottom = self.rect.bottom - self.padding

    def align_rect(self) -> None:
        self.align_image()

    def blit(self) -> None:
        screen.blit(self.image, self.image_rect)


class ToggleImageMixin(ToggleInputMixin, ImageLabelMixin):
    def __init__(self, images: _Images, scale_by: int | None = None,
                 mask_image:  pygame.Surface | None = None,
                 image_align: _Align = None, padding: int = 20,
                 on_toggle_on: Callable | None = None,
                 on_toggle_off: Callable | None = None, *,
                 requires_state: bool = False):
        ToggleInputMixin.__init__(self, on_toggle_on, on_toggle_off,
                                  requires_state=requires_state)
        ImageLabelMixin.__init__(self, images, scale_by, mask_image,
                                 image_align, padding)

    def toggle_on(self) -> None:
        super().toggle_on()
        self.image = self.images[2]

    def update_hover(self) -> None:
        super().update_hover()
        self.image = self.images[1]

    def update_idle(self) -> None:
        super().update_idle()
        self.image = self.images[0]


class ClickImageMixin(ClickInputMixin, ImageLabelMixin):
    def __init__(self, images: _Images, scale_by: int | None = None,
                 image_mask: pygame.Surface | False | None = None,
                 image_align: _Align = None, padding: int = 20,
                 on_click: Callable | None = None,
                 on_release: Callable | None = None):
        ClickInputMixin.__init__(self, on_click, on_release)
        ImageLabelMixin.__init__(self, images, scale_by, image_mask,
                                 image_align, padding)

    def update_idle(self) -> None:
        super().update_idle()
        self.image = self.images[0]

    def update_hover(self) -> None:
        super().update_hover()
        self.image = self.images[1]

    def update_click(self) -> None:
        super().update_click()
        self.image = self.images[2]
