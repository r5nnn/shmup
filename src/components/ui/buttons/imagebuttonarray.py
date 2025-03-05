from __future__ import annotations
from dataclasses import dataclass
from typing import override, TYPE_CHECKING, Callable

from src.components.ui.buttons.buttonbases import _BaseButtonArrayConfig, \
    ButtonArrayBase
from src.components.ui.buttons.imagebutton import (
    ImageToggleButton, ImageClickButton, ImageRectToggleButton,
    ImageRectClickButton, ImageButtonConfig)

if TYPE_CHECKING:
    from src.components.ui.buttons._types import _AnyButton, _Images
    import pygame


@dataclass
class _ImageButtonArrayConfig(_BaseButtonArrayConfig):
    images: tuple[tuple[_Images, ...], ...]
    scale_by: tuple[tuple[int, ...], ...] | int = 0


@dataclass
class ImageToggleButtonArrayConfig(_ImageButtonArrayConfig):
    mask_images: (tuple[tuple[pygame.Surface | str | False | None, ...], ...]
                  | str | None | False) = None
    on_toggle_on: tuple[tuple[Callable | None, ...], ...] | None = None
    on_toggle_off: tuple[tuple[Callable | None, ...], ...] | None = None
    requires_state: bool = False


class ImageToggleButtonArray(ButtonArrayBase):
    def __init__(self, arr_position: tuple[int, int],
                 arr_shape: tuple[int, int], arr_padding: tuple[int, int] | int,
                 config: ImageToggleButtonArrayConfig,
                 *, arr_sub_widget: bool = False):
        super().__init__(arr_position, arr_shape, arr_padding, config,
                         arr_sub_widget=arr_sub_widget)

    @override
    def make_button(self, row: int, column: int, x_pos: int, y_pos: int,
                    config: ImageToggleButtonArrayConfig) -> _AnyButton:
        scale_by = (config.scale_by
                    if isinstance(config.scale_by, int)
                    else config.scale_by[column][row])
        config_ = ImageButtonConfig(position=(x_pos, y_pos), align=config.align,
                                    audio_tags=config.audio_tags,
                                    sub_widget=True,
                                    images=config.images[column][row],
                                    scale_by=scale_by)
        mask_image = (config.mask_images
                      if not isinstance(config.mask_images, tuple)
                      else config.mask_images[column][row])
        on_toggle_on = (config.on_toggle_on[column][row]
                        if config.on_toggle_on is not None else None)
        on_toggle_off = (config.on_toggle_off[column][row]
                         if config.on_toggle_off is not None else None)

        return ImageToggleButton(config_, mask_image, on_toggle_on,
                                 on_toggle_off,
                                 requires_state=config.requires_state)


@dataclass
class ImageClickButtonArrayConfig(_ImageButtonArrayConfig):
    mask_images: (tuple[tuple[pygame.Surface | str | False | None, ...], ...]
                  | str | None | False) = None
    on_click: tuple[tuple[Callable | None, ...], ...] | None = None
    on_release: tuple[tuple[Callable | None, ...], ...] | None = None


class ImageClickButtonArray(ButtonArrayBase):
    def __init__(self, arr_position: tuple[int, int],
                 arr_shape: tuple[int, int], arr_padding: tuple[int, int] | int,
                 config: ImageClickButtonArrayConfig,
                 *, arr_sub_widget: bool = False):
        super().__init__(arr_position, arr_shape, arr_padding, config,
                         arr_sub_widget=arr_sub_widget)

    @override
    def make_button(self, row: int, column: int, x_pos: int, y_pos: int,
                    config: ImageClickButtonArrayConfig) -> _AnyButton:
        scale_by = (config.scale_by
                    if isinstance(config.scale_by, int)
                    else config.scale_by[column][row])
        _config = ImageButtonConfig(
            position=(x_pos, y_pos), align=config.align,
            audio_tags=config.audio_tags, sub_widget=True,
            images=config.images[column][row], scale_by=scale_by)
        mask_image = (config.mask_images
                      if not isinstance(config.mask_images, tuple)
                      else config.mask_images[column][row])
        on_click = (config.on_click[column][row]
                        if config.on_click is not None else None)
        on_release = (config.on_release[column][row]
                         if config.on_release is not None else None)

        return ImageClickButton(_config, mask_image, on_click, on_release)


