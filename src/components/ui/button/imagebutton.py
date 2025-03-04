from __future__ import annotations
from typing import Callable, TYPE_CHECKING, override


from src.components.ui.button.imagemixins import (
    ToggleImageMixin, ClickImageMixin)
from src.components.ui.button.basemixins import (
    ImageButtonBaseMixin, RectButtonMixin)
from src.components.ui.button.inputmixins import checktoggle
from src.components.ui.widgetutils import WidgetBase

if TYPE_CHECKING:
    import pygame
    from src.components.ui.button._types import _Align, _Colors
    from src.core.constants import RectAlignments


class ImageToggleButton(ImageButtonBaseMixin, ToggleImageMixin):
    def __init__(self, position: tuple[int, int],
                 images: tuple[pygame.Surface] | pygame.Surface,
                 align: RectAlignments = "topleft",
                 click_audio_tag: str = "click",
                 release_audio_tag: str = "click",
                 mask_image: pygame.Surface | None = None,
                 image_align: _Align = None, padding: int = 20,
                 on_toggle_on: Callable | None = None,
                 on_toggle_off: Callable | None = None, *,
                 requires_state: bool = False, sub_widget: bool = False):
        ImageButtonBaseMixin.__init__(self, position, align, click_audio_tag,
                                      release_audio_tag, sub_widget=sub_widget)
        ToggleImageMixin.__init__(self, images, mask_image, image_align,
                                  padding, on_toggle_on, on_toggle_off,
                                  requires_state=requires_state)
        self._rect = self._image_rect
        self._width, self._height = self._rect.size

    @override
    def blit(self) -> None:
        ToggleImageMixin.blit(self)

    @override
    def update(self) -> None:
        WidgetBase.update(self)
        ToggleImageMixin.update(self)
        if self.requires_realignment:
            self._align_rect()

    @checktoggle
    def update_idle(self) -> None:
        super().update_idle()

    @checktoggle
    def update_hover(self) -> None:
        super().update_hover()

    def _align_rect(self) -> None:
        ImageButtonBaseMixin._align_rect(self)


class ImageClickButton(ImageButtonBaseMixin, ClickImageMixin):
    def __init__(self, position: tuple[int, int],
                 images: tuple[pygame.Surface] | pygame.Surface,
                 align: RectAlignments = "topleft",
                 click_audio_tag: str = "click",
                 release_audio_tag: str = "click",
                 image_mask: pygame.Surface | False | None = None,
                 image_align: _Align = None, padding: int = 20,
                 on_click: Callable | None = None,
                 on_release: Callable | None = None, *,
                 sub_widget: bool = False):
        ImageButtonBaseMixin.__init__(self, position, align, click_audio_tag,
                                      release_audio_tag, sub_widget=sub_widget)
        ClickImageMixin.__init__(self, images, image_mask, image_align,
                                 padding, on_click, on_release)
        self._rect = self._image_rect
        self._width, self._height = self._rect.size

    @override
    def blit(self):
        ToggleImageMixin.blit(self)

    @override
    def update(self) -> None:
        WidgetBase.update(self)
        ClickImageMixin.update(self)
        if self.requires_realignment:
            self._align_rect()

    def _align_rect(self) -> None:
        ImageButtonBaseMixin._align_rect(self)


class ImageRectToggleButton(RectButtonMixin, ToggleImageMixin):
    def __init__(self, position: tuple[int, int], size: tuple[int, int],
                 images: tuple[pygame.Surface] | pygame.Surface,
                 align: RectAlignments = "topleft", radius: int = 0,
                 colors: _Colors = None, click_audio_tag: str = "click",
                 release_audio_tag: str = "click",
                 mask_image: pygame.Surface | None = None,
                 image_align: _Align = None, padding: int = 20,
                 on_toggle_on: Callable | None = None,
                 on_toggle_off: Callable | None = None, *,
                 requires_state: bool = False, sub_widget: bool = False):
        RectButtonMixin.__init__(self, position, size, align, radius, colors,
                                 click_audio_tag, release_audio_tag,
                                 sub_widget=sub_widget)
        ToggleImageMixin.__init__(self, images, mask_image, image_align,
                                  padding, on_toggle_on, on_toggle_off,
                                  requires_state=requires_state)

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
        ToggleImageMixin.update(self)
        RectButtonMixin.update(self)
        if self.requires_realignment:
            self._align_rect()

    def blit(self) -> None:
        RectButtonMixin.blit(self)
        ToggleImageMixin.blit(self)

    def _align_rect(self) -> None:
        RectButtonMixin._align_rect(self)
        self._align_image()


class ImageRectClickButton(RectButtonMixin, ClickImageMixin):
    def __init__(self, position: tuple[int, int], size: tuple[int, int],
                 images: tuple[pygame.Surface] | pygame.Surface,
                 align: RectAlignments = "topleft", radius: int = 0,
                 colors: _Colors = None, click_audio_tag: str = "click",
                 release_audio_tag: str = "click",
                 image_mask: pygame.Surface | False | None = None,
                 image_align: _Align = None, padding: int = 20,
                 on_click: Callable | None = None,
                 on_release: Callable | None = None, *,
                 sub_widget: bool = False):
        RectButtonMixin.__init__(self, position, size, align, radius, colors,
                                 click_audio_tag, release_audio_tag,
                                 sub_widget=sub_widget)
        ClickImageMixin.__init__(self, images, image_mask, image_align,
                                 padding, on_click, on_release)

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
        ClickImageMixin.update(self)
        RectButtonMixin.update(self)
        if self.requires_realignment:
            self._align_rect()

    def blit(self) -> None:
        RectButtonMixin.blit(self)
        ClickImageMixin.blit(self)

    def _align_rect(self) -> None:
        RectButtonMixin._align_rect(self)
        self._align_image()
