from __future__ import annotations
from dataclasses import dataclass
from typing import override, TYPE_CHECKING, Callable

from src.components.ui.buttons.buttonbases import _BaseButtonArrayConfig, \
    ButtonArrayBase
from src.components.ui.buttons.imagebutton import (
    ImageToggleButton, ImageClickButton, ImageRectToggleButton,
    ImageRectClickButton, ImageButtonConfig)

if TYPE_CHECKING:
    from src.core.types import AnyButton, Images, Colors, Align
    import pygame


@dataclass(kw_only=True)
class _ImageButtonArrayConfig(_BaseButtonArrayConfig):
    images: tuple[tuple[Images, ...], ...]
    scale_by: tuple[tuple[int, ...], ...] | int = 0


@dataclass(kw_only=True)
class ImageToggleButtonArrayConfig(_ImageButtonArrayConfig):
    image_masks: (tuple[tuple[pygame.Surface | str | False | None, ...], ...]
                  | str | None | False) = None
    start_images: tuple[tuple[int, ...], ...] | int = 0
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
                    config: ImageToggleButtonArrayConfig) -> AnyButton:
        scale_by = (config.scale_by
                    if isinstance(config.scale_by, int)
                    else config.scale_by[column][row])
        config_ = ImageButtonConfig(position=(x_pos, y_pos), align=config.align,
                                    audio_tags=config.audio_tags,
                                    sub_widget=True,
                                    images=config.images[column][row],
                                    scale_by=scale_by)
        start_image = (config.start_images[column][row]
                       if not isinstance(config.start_images, int)
                       else config.start_images)
        mask_image = (config.image_masks
                      if not isinstance(config.image_masks, tuple)
                      else config.image_masks[column][row])
        on_toggle_on = (config.on_toggle_on[column][row]
                        if config.on_toggle_on is not None else None)
        on_toggle_off = (config.on_toggle_off[column][row]
                         if config.on_toggle_off is not None else None)

        return ImageToggleButton(config_, start_image, mask_image, on_toggle_on,
                                 on_toggle_off,
                                 requires_state=config.requires_state)


@dataclass(kw_only=True)
class ImageClickButtonArrayConfig(_ImageButtonArrayConfig):
    image_masks: (tuple[tuple[pygame.Surface | str | False | None, ...], ...]
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
                    config: ImageClickButtonArrayConfig) -> AnyButton:
        scale_by = (config.scale_by
                    if isinstance(config.scale_by, int)
                    else config.scale_by[column][row])
        config_ = ImageButtonConfig(
            position=(x_pos, y_pos), align=config.align,
            audio_tags=config.audio_tags, sub_widget=True,
            images=config.images[column][row], scale_by=scale_by)
        mask_image = (config.image_masks
                      if not isinstance(config.image_masks, tuple)
                      else config.image_masks[column][row])
        on_click = (config.on_click[column][row]
                    if config.on_click is not None else None)
        on_release = (config.on_release[column][row]
                      if config.on_release is not None else None)

        return ImageClickButton(config_, mask_image, on_click, on_release)


@dataclass
class ImageRectToggleButtonArrayConfig(ImageToggleButtonArrayConfig):
    sizes: tuple[tuple[tuple[int, int], ...], ...] | tuple[int, int]
    start_image: tuple
    radius: int = 0
    colors: Colors | None = None
    padding: int = 20
    image_align: Align | None = None


class ImageRectToggleButtonArray(ButtonArrayBase):
    def __init__(self, arr_position: tuple[int, int],
                 arr_shape: tuple[int, int], arr_padding: tuple[int, int] | int,
                 config: ImageRectToggleButtonArrayConfig,
                 *, arr_sub_widget: bool = False):
        super().__init__(arr_position, arr_shape, arr_padding, config,
                         arr_sub_widget=arr_sub_widget)

    @override
    def make_button(self, row: int, column: int, x_pos: int, y_pos: int,
                    config: ImageRectToggleButtonArrayConfig) -> AnyButton:
        scale_by = (config.scale_by
                    if isinstance(config.scale_by, int)
                    else config.scale_by[column][row])
        config_ = ImageButtonConfig(
            position=(x_pos, y_pos), align=config.align,
            audio_tags=config.audio_tags, sub_widget=True,
            images=config.images, scale_by=scale_by)
        size = (config.sizes
                if isinstance(config.sizes[0], int)
                else config.sizes[column][row])
        start_image = (config.start_images
                       if isinstance(config.start_images, int)
                       else config.start_images[column][row])
        mask_image = (config.image_masks
                      if not isinstance(config.image_masks, tuple)
                      else config.image_masks[column][row])
        on_toggle_on = (config.on_toggle_on[column][row]
                        if config.on_toggle_on is not None else None)
        on_toggle_off = (config.on_toggle_off[column][row]
                         if config.on_toggle_off is not None else None)

        return ImageRectToggleButton(
            config_, size, config.radius, config.colors, start_image,
            mask_image, config.image_align, config.padding,
            on_toggle_on, on_toggle_off, requires_state=config.requires_state)


@dataclass
class ImageRectClickButtonArrayConfig(ImageClickButtonArrayConfig):
    sizes: tuple[tuple[tuple[int, int], ...], ...] | tuple[int, int]
    radius: int = 0
    colors: Colors | None = None
    image_align: Align | None = None
    padding: int = 20


class ImageRectClickButtonArray(ButtonArrayBase):
    def __init__(self, arr_position: tuple[int, int],
                 arr_shape: tuple[int, int], arr_padding: tuple[int, int] | int,
                 config: ImageRectClickButtonArrayConfig,
                 *, arr_sub_widget: bool = False):
        super().__init__(arr_position, arr_shape, arr_padding, config,
                         arr_sub_widget=arr_sub_widget)

    @override
    def make_button(self, row: int, column: int, x_pos: int, y_pos: int,
                    config: ImageRectClickButtonArrayConfig) -> AnyButton:
        scale_by = (config.scale_by
                    if isinstance(config.scale_by, int)
                    else config.scale_by[column][row])
        config_ = ImageButtonConfig(position=(x_pos, y_pos), align=config.align,
                                    audio_tags=config.audio_tags,
                                    sub_widget=True, images=config.images,
                                    scale_by=scale_by)
        size = (config.sizes
                if isinstance(config.sizes[0], int)
                else config.sizes[column][row])
        on_click = (config.on_click[column][row]
                    if config.on_click is not None else None)
        on_release = (config.on_release[column][row]
                      if config.on_release is not None else None)

        return ImageRectClickButton(
            config_, size, config.radius, config.colors, config.image_masks,
            config.image_align, config.padding, on_click, on_release)
