"""Module for displaying buttons on the screen.

Buttons consist of a base rectangle with a label on top. The label can be text
or an image. The base rectangle can be hidden to use the image label as the
button itself. In this case pixel-perfect collision can also be used.
Buttons can be hovered and interacted with. An attribute of the button can
change or an action can be executed when the button is pressed down or released.
"""
from __future__ import annotations

import logging
from abc import ABC
from dataclasses import dataclass
from functools import wraps
from typing import Callable, override, TypeVar, Any
from typing import TYPE_CHECKING

import pygame.display

import src.components.input as InputManager
from src.components.ui import widgethandler
from src.core.constants import LEFTCLICK
from src.components import RectAlignments, button_audio
from src.components.ui.text import Text
from src.components.ui.widgetutils import WidgetBase, AlignmentNeeded
from src.core import screen, sprites

if TYPE_CHECKING:
    import types

_T = TypeVar("_T", bound=Callable[..., Any])


def button_from_images(name: str, position: tuple[int, int],
                       on_click: Callable | None = None,
                       on_release: Callable | None = None) -> ImageButton:
    """Create buttons where the image IS the button itself rather than a label."""
    config = ImageButtonConfig(
        position=position, size=(0, 0),
        images=[pygame.transform.scale_by(images, 3) for images in sprites(name)],
        on_click=on_click, on_release=on_release)
    return ImageButton(config)


@dataclass
class ButtonConfig:
    position: tuple[int, int]
    size: tuple[int, int]
    align: RectAlignments = "topleft"
    colors: tuple[tuple | pygame.Color] | None = None
    border_colors: tuple[tuple | pygame.Color] | None = None
    border_thickness: int = 0
    radius: int = 0
    click_audio: str = "click"
    release_audio: str = "click"
    sub_widget: bool = False


class _ButtonMixinFields:
    _x: int
    _y: int
    _requires_realignment: bool
    _align_rect: types.FunctionType
    _align: RectAlignments
    _rect: pygame.Rect
    contains: types.FunctionType
    click_audio_tag = str | None
    release_audio_tag = str | None
    colors: tuple[tuple | pygame.Color] | None
    color: tuple | pygame.Color | None
    border_colors:  tuple[tuple | pygame.Color] | None
    border_color: tuple | pygame.Color | None


class ClickInputMixin(_ButtonMixinFields):
    def __init__(self, on_click: Callable | None = None,
                 on_release: Callable | None = None):
        self.on_click_call = on_click
        self.on_release_call = on_release
        self.clicked = False

    def update_click(self) -> None:
        self.clicked = True
        if self.click_audio_tag is not None:
            button_audio.play_audio(self.click_audio_tag, override=True)
        if self.colors is not None:
            self.color = self.colors[2]
        if self.border_colors is not None:
            self.border_color = self.border_colors[2]

    def update_release(self) -> None:
        """Method that is called when the button is released."""
        self.clicked = False
        if self.release_audio_tag is not None:
            button_audio.play_audio(self.release_audio_tag, override=True)

    def update_hover(self) -> None:
        """Method that is called when the button is hovered."""
        if self.colors is not None:
            self.color = self.colors[1]
        if self.border_colors is not None:
            self.border_color = self.border_colors[1]

    def update_idle(self) -> None:
        """Method that is called when the button is idle."""
        self.clicked = False
        if self.colors is not None:
            self.color = self.colors[0]
        if self.border_colors is not None:
            self.border_color = self.border_colors[0]

    def update(self) -> None:
        x, y = InputManager.get_mouse_pos()
        if self.contains(x, y):
            # button is released
            if InputManager.is_mouse_up(LEFTCLICK) and self.clicked:
                self.update_release()
                self.on_release_call() if self.on_release_call is not None else None
            # button is clicked
            elif InputManager.is_mouse_down(LEFTCLICK):
                self.update_click()
                if self.on_click_call is not None:
                    self.clicked = False
                    self.on_click_call()
            # button hovered
            elif not self.clicked:
                self.update_hover()
        # button not interacted with
        else:
            self.update_idle()


class ToggleInputMixin(_ButtonMixinFields):
    def __init__(self, on_toggle_on, on_toggle_off, on_toggle, on_toggle_arg=False):
        self.on_toggle_off = on_toggle_off
        self.on_toggle_on = on_toggle_on
        self.on_toggle = on_toggle
        self.on_toggle_arg = on_toggle_arg
        self.toggled = False
        self.sub_widget = False

    @staticmethod
    def checktoggle(method: _T) -> _T:
        @wraps(method)
        def wrapper(self, *args, **kwargs):  # noqa: ANN001, ANN202
            if not self.toggled:
                method(self, *args, **kwargs)

        return wrapper

    def toggle_on(self) -> None:
        """Turn the toggle state on."""
        self.toggled = True
        if self.colors is not None:
            self.color = self.colors[2]
        if self.border_colors is not None:
            self.border_color = self.border_colors[2]

    def toggle_on_call(self, *, silent: bool = False) -> None:
        self.toggle_on()
        if not silent:
            button_audio.play_audio(self.click_audio_tag, override=True)
        self.on_toggle_on() if self.on_toggle_on is not None else None
        if self.on_toggle is not None:
            if self.on_toggle_arg:
                self.on_toggle(True)
            else:
                self.on_toggle()

    def toggle_off(self) -> None:
        """Turn the toggle state off."""
        self.toggled = False
        # no need to toggle colors off since that is handled by update hover and idle

    def toggle_off_call(self, *, silent: bool = False) -> None:
        self.toggle_off()
        if not silent:
            button_audio.play_audio(self.release_audio_tag, override=True)
        self.on_toggle_off() if self.on_toggle_off is not None else None
        if self.on_toggle is not None:
            if self.on_toggle_arg:
                self.on_toggle(False)
            else:
                self.on_toggle()

    @checktoggle
    def update_hover(self) -> None:
        if self.colors is not None:
            self.color = self.colors[1]
        if self.border_colors is not None:
            self.border_color = self.border_colors[1]

    @checktoggle
    def update_idle(self) -> None:
        if self.colors is not None:
            self.color = self.colors[0]
        if self.border_colors is not None:
            self.border_color = self.border_colors[0]

    def update(self) -> None:
        x, y = InputManager.get_mouse_pos()
        if self.contains(x, y):
            if InputManager.is_mouse_down(LEFTCLICK) and not self.toggled:
                self.toggle_on_call()
            elif not self.sub_widget and InputManager.is_mouse_down(LEFTCLICK) and self.toggled:
                self.toggle_off_call()
            elif not self.toggled:
                self.update_hover()
        else:
            self.update_idle()


class ButtonBase(WidgetBase, ABC):
    """Base class for creating buttons."""

    def __init__(self, config: ButtonConfig):
        WidgetBase.__init__(self, config.position, config.align,
                            sub_widget=config.sub_widget)
        self._width, self._height = config.size
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._align_rect(self._rect, self._align, (self._x, self._y))
        self.colors = config.colors
        self.color = self.colors[0] if self.colors is not None else None
        self.border_colors = config.border_colors
        self.border_color = self.border_colors[0] \
            if self.border_colors is not None else None
        self._border_thickness = config.border_thickness
        self._border_rect = pygame.Rect(
            self._rect.left + self._border_thickness,
            self._rect.top + self._border_thickness,
            self._width - self._border_thickness * 2,
            self._height - self._border_thickness * 2)
        self.click_audio_tag = config.click_audio
        self.release_audio_tag = config.release_audio
        self.radius = config.radius

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value
        self._rect.width = self._width
        if self.border_colors is not None:
            self._border_rect.width = self._width - self._border_thickness * 2
        self._align_rect(self._rect, self._align, (self._x, self._y))

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = value
        self._rect.height = self._height
        if self.border_colors is not None:
            self._border_rect.height = (self._height - self._border_thickness * 2)
        self._align_rect(self._rect, self._align, (self._x, self._y))

    @property
    def border_thickness(self) -> int:
        """How wide the border should be, in pixels."""
        return self._border_thickness

    @border_thickness.setter
    def border_thickness(self, value: int) -> None:
        self._border_thickness = value
        self._border_rect.size = (
            self._width - self._border_thickness * 2,
            self._height - self._border_thickness * 2)
        self._border_rect.topleft = (
            self._rect.left + self._border_thickness,
            self._rect.top + self._border_thickness)

    def _align_rect(self, rect: pygame.Rect, align: RectAlignments,
                    coords: tuple[int, int]) -> None:
        setattr(rect, align, coords)
        self._x, self._y = getattr(rect, align)

    @override
    def contains(self, x: int, y: int) -> bool:
        super().contains(x, y)
        return (self._rect.left < x - screen.get_abs_offset()[0] <
                self._rect.left + self._width) and \
            (self._rect.top < y - screen.get_abs_offset()[1] <
             self._rect.top + self._height)

    @override
    def blit(self) -> None:
        if self.border_colors is not None:
            pygame.draw.rect(screen, self.border_color, self._border_rect,
                             border_radius=self.radius)
        if self.colors is not None:
            pygame.draw.rect(screen, self.color, self._rect,
                             border_radius=self.radius)

    def update(self) -> None:
        if self.requires_realignment:
            self._align_rect(self._rect, self._align, (self._x, self._y))


class ToggleGroup:
    def __init__(self, *buttons):
        self.sub_widget = False
        self.hidden = False
        self.disabled = False
        self.requires_realignment = False
        self.buttons = list(buttons)
        for button in self.buttons:
            button.sub_widget = True
        if self.buttons:
            # Automatically toggle on the first button
            self.buttons[0].toggle_on_call(silent=True)

    def update(self) -> None:
        for button in self.buttons:
            button.update()

            # If a button is toggled on, ensure others are toggled off
            if button.toggled:
                for other_button in self.buttons:
                    if other_button != button and other_button.toggled:
                        other_button.toggle_off_call(silent=True)

    def blit(self) -> None:
        for button in self.buttons:
            button.blit()

    def contains(self, x: int, y: int) -> bool:
        if self.disabled:  # noqa: RET503
            return False

    def hide(self) -> None:
        self.hidden = True
        if not self.sub_widget:
            for button in self.buttons:
                widgethandler.move_to_bottom(button)

    def show(self) -> None:
        self.hidden = False
        if not self.sub_widget:
            for button in self.buttons:
                widgethandler.move_to_top(button)


@dataclass(kw_only=True)
class ToggleableTextButtonConfig(ButtonConfig):
    text: tuple | str
    start_text: int = 0
    text_colors: tuple[tuple | pygame.Color] | None = None
    font: pygame.font.Font | None = None
    font_size: int = 32
    text_align: tuple[str, str] = None
    margin: int = 20
    on_toggle_on: Callable | None = None
    on_toggle_off: Callable | None = None
    on_toggle: Callable | None = None
    on_toggle_arg: bool = False


class TextButtonBase(ButtonBase, ABC):
    """Class for creating buttons with text labels."""

    text = AlignmentNeeded()

    def __init__(self, config: ToggleableTextButtonConfig):
        self.text_colors = (config.text_colors or
                            tuple(pygame.Color("White") for _ in range(3)))
        self._text_color = self.text_colors[0]
        self.text = Text((0, 0), config.text, config.font, config.font_size,
                         color=self._text_color, sub_widget=True)

        self.text_align = config.text_align
        self.margin = config.margin
        super().__init__(config)
        logging.info("Created %r.", self)

    def _align_text(self, text_object: Text) -> None:
        self.text_rect = text_object.rect
        self.text_rect.center = self._rect.center  # Start with centered alignment

        if self.text_align:
            if self.text_align[0] == "left":
                self.text_rect.left = self._rect.left + self.margin
            elif self.text_align[0] == "right":
                self.text_rect.right = self._rect.right - self.margin
            if self.text_align[1] == "top":
                self.text_rect.top = self._rect.top + self.margin
            elif self.text_align[1] == "bottom":
                self.text_rect.bottom = self._rect.bottom - self.margin

        # Update text surface position
        text_object.x, text_object.y = self.text_rect.topleft

    @override
    def _align_rect(self, rect: pygame.Rect, align: RectAlignments,
                    coords: tuple[int, int]) -> None:
        super()._align_rect(rect, align, coords)
        self._align_text(self._text)

    @override
    def blit(self) -> None:
        super().blit()
        self._text.blit()

    @override
    def update(self) -> None:
        if self._text.requires_realignment:
            self.requires_realignment = True
        super().update()
        self._text.update()


class TextButtonConfig(ToggleableTextButtonConfig):
    on_click: Callable | None = None
    on_release: Callable | None = None


class TextButton(TextButtonBase, ClickInputMixin):
    def __init__(self, config: TextButtonConfig):
        ClickInputMixin.__init__(self, on_click=config.on_click,
                                 on_release=config.on_release)
        TextButtonBase.__init__(self, config)

    def update(self) -> None:
        super().update()
        ClickInputMixin.update(self)


class ToggleableTextButton(TextButtonBase, ToggleInputMixin):
    def __init__(self, config: ToggleableTextButtonConfig):
        ToggleInputMixin.__init__(self, config.on_toggle_on, config.on_toggle_off, config.on_toggle, config.on_toggle_arg)
        self.text_tuple = config.text if isinstance(config.text, tuple) else (config.text, config.text)
        config.text = self.text_tuple[config.start_text]
        TextButtonBase.__init__(self, config)

    def toggle_on(self) -> None:
        super().toggle_on()
        self.text.text = self.text_tuple[0]

    def toggle_off(self) -> None:
        super().toggle_off()
        self.text.text = self.text_tuple[1]

    def update(self) -> None:
        super().update()
        ToggleInputMixin.update(self)


@dataclass(kw_only=True)
class ToggleableImageButtonConfig(ButtonConfig):
    images: list
    use_rect_collisions: bool = False
    image_align: tuple[str, str] | None = None
    margin: int = 20


@dataclass(kw_only=True)
class ImageButtonConfig(ToggleableImageButtonConfig):
    on_click: Callable | None = None
    on_release: Callable | None = None


class ImageButtonBase(ButtonBase, ABC):
    def __init__(self, config: ImageButtonConfig):
        ButtonBase.__init__(self, config)
        self.images = config.images
        self._current_image = self.images[0]
        self.use_rect_collision = config.use_rect_collisions
        self.image_align = config.image_align
        self.margin = config.margin
        self._align_image()
        logging.info("Created %r.", self)

    @property
    def image_align(self) -> tuple[str, str] | None:
        return self._image_align

    @image_align.setter
    def image_align(self, value: tuple[str, str] | None) -> None:
        self._image_align = value
        self._align_image()

    def _align_image(self) -> None:
        self.image_rect = self._current_image.get_rect()
        self.image_rect.center = self._rect.center

        if self.image_align:
            if self.image_align[0] == "left":
                self.image_rect.left = self._rect.left + self.margin
            elif self.image_align[0] == "right":
                self.image_rect.right = self._rect.right - self.margin

            if self.image_align[1] == "top":
                self.image_rect.top = self._rect.top + self.margin
            elif self.image_align[1] == "bottom":
                self.image_rect.bottom = self._rect.bottom - self.margin

    @override
    def contains(self, x: int, y: int) -> bool:
        if self.use_rect_collision:
            return super().contains(x, y)
        local_x = x - self.image_rect.left
        local_y = y - self.image_rect.top
        try:
            return self._current_image.get_at((local_x, local_y)).a != 0
        except IndexError:
            return False

    def update_click(self) -> None:
        self._current_image = self.images[2]

    def update_hover(self) -> None:
        self._current_image = self.images[1]

    def update_idle(self) -> None:
        self._current_image = self.images[0]

    @override
    def blit(self) -> None:
        if self.use_rect_collision:
            pygame.draw.rect(screen, self.color, self._rect, border_radius=self.radius)

        screen.blit(self._current_image, self.image_rect.topleft)

    def update(self) -> None:
        super().update()


class ImageButton(ImageButtonBase, ClickInputMixin):
    def __init__(self, config: ImageButtonConfig):
        ImageButtonBase.__init__(self, config)
        ClickInputMixin.__init__(self, config.on_click, config.on_release)

    @override
    def update(self) -> None:
        ClickInputMixin.update(self)

    @override
    def update_idle(self) -> None:
        ClickInputMixin.update_idle(self)
        ImageButtonBase.update_idle(self)

    @override
    def update_click(self) -> None:
        ClickInputMixin.update_click(self)
        ImageButtonBase.update_click(self)

    @override
    def update_hover(self) -> None:
        ClickInputMixin.update_hover(self)
        ImageButtonBase.update_hover(self)
