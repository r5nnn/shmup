from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING, override


from src.components.ui.buttons.imagemixins import (
    ToggleImageMixin, ClickImageMixin)
from src.components.ui.buttons.basemixins import (
    ImageButtonBaseMixin, RectButtonMixin, _BaseButtonConfig)
from src.components.ui.buttons.inputmixins import checktoggle
from src.components.ui.widgetutils import WidgetBase

if TYPE_CHECKING:
    import pygame
    from src.components.ui.buttons._types import _Align, _Colors, _Images


@dataclass(kw_only=True)
class ImageButtonConfig(_BaseButtonConfig):
    images: _Images
    scale_by: int | None = None


class ImageToggleButton(ImageButtonBaseMixin, ToggleImageMixin):
    def __init__(self, config: ImageButtonConfig,
                 mask_image: pygame.Surface | None = None,
                 on_toggle_on: Callable | None = None,
                 on_toggle_off: Callable | None = None, *,
                 requires_state: bool = False):
        ImageButtonBaseMixin.__init__(self, config.position,
                                      config.align[0] + config.align[1],
                                      config.audio_tags,
                                      sub_widget=config.sub_widget)
        ToggleImageMixin.__init__(self, config.images, config.scale_by,
                                  mask_image, config.align, 0, on_toggle_on,
                                  on_toggle_off, requires_state=requires_state)
        self.rect = self.image_rect
        self.align_rect()
        self._width, self._height = self.rect.size

    @override
    def blit(self) -> None:
        ToggleImageMixin.blit(self)

    @override
    def update(self) -> None:
        WidgetBase.update(self)
        if self.requires_realignment:
            self.requires_realignment = False
            self.align_rect()
        ToggleImageMixin.update(self)

    def update_hover(self) -> None:
        super().update_hover()

    @checktoggle
    def update_idle(self) -> None:
        super().update_idle()

    def align_rect(self) -> None:
        ImageButtonBaseMixin.align_rect(self)


class ImageClickButton(ImageButtonBaseMixin, ClickImageMixin):
    def __init__(self, config: ImageButtonConfig,
                 image_mask: pygame.Surface | False | None = None,
                 on_click: Callable | None = None,
                 on_release: Callable | None = None):
        ImageButtonBaseMixin.__init__(self, config.position,
                                      config.align[0] + config.align[1],
                                      config.audio_tags,
                                      sub_widget=config.sub_widget)
        ClickImageMixin.__init__(self, config.images, config.scale_by,
                                 image_mask, config.align, 0, on_click,
                                 on_release)
        self.rect = self.image_rect
        self.align_rect()
        self._width, self._height = self.rect.size

    @override
    def blit(self) -> None:
        ToggleImageMixin.blit(self)

    @override
    def update(self) -> None:
        WidgetBase.update(self)
        if self.requires_realignment:
            self.requires_realignment = False
            self.align_rect()
        ClickImageMixin.update(self)

    def align_rect(self) -> None:
        ImageButtonBaseMixin.align_rect(self)


class ImageRectToggleButton(RectButtonMixin, ToggleImageMixin):
    def __init__(self, config: ImageButtonConfig, size: tuple[int, int],
                 radius: int = 0, colors: _Colors = None,
                 mask_image: pygame.Surface | None = None,
                 image_align: _Align = None, padding: int = 20,
                 on_toggle_on: Callable | None = None,
                 on_toggle_off: Callable | None = None, *,
                 requires_state: bool = False):
        RectButtonMixin.__init__(self, config.position, size,
                                 config.align[0] + config.align[1], radius,
                                 colors, config.audio_tags,
                                 sub_widget=config.sub_widget)
        ToggleImageMixin.__init__(self, config.images, config.scale_by,
                                  mask_image, image_align, padding,
                                  on_toggle_on, on_toggle_off,
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
        ToggleImageMixin.update(self)

    def blit(self) -> None:
        RectButtonMixin.blit(self)
        ToggleImageMixin.blit(self)

    def align_rect(self) -> None:
        RectButtonMixin.align_rect(self)
        ToggleImageMixin.align_rect(self)


class ImageRectClickButton(RectButtonMixin, ClickImageMixin):
    def __init__(self, config: ImageButtonConfig, size: tuple[int, int],
                 radius: int = 0, colors: _Colors = None,
                 image_mask: pygame.Surface | False | None = None,
                 image_align: _Align = None, padding: int = 20,
                 on_click: Callable | None = None,
                 on_release: Callable | None = None):
        RectButtonMixin.__init__(self, config.position, size,
                                 config.align[0] + config.align[1], radius,
                                 colors, config.audio_tags,
                                 sub_widget=config.sub_widget)
        ClickImageMixin.__init__(self, config.images, config.scale_by,
                                 image_mask, image_align, padding, on_click,
                                 on_release)
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
        ClickImageMixin.update(self)

    def blit(self) -> None:
        RectButtonMixin.blit(self)
        ClickImageMixin.blit(self)

    def align_rect(self) -> None:
        RectButtonMixin.align_rect(self)
        ToggleImageMixin.align_rect(self)
