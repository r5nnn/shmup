"""Module for displaying buttons on the screen.

Buttons consist of a base rectangle with a label on top. The label can be text
or an image. The base rectangle can be hidden to use the image label as the
button itself. In this case pixel-perfect collision can also be used.
Buttons can be hovered and interacted with. An attribute of the button can
change or an action can be executed when the button is pressed down or released.
"""
import logging
from dataclasses import dataclass
from functools import wraps
from typing import Callable, override, Optional

import pygame.display

import data.components.input as InputManager
from data.components import RectAlignments
from data.components.audio import button_audio
from data.components.ui.text import Text
from data.components.ui.widgetutils import WidgetBase
from data.core import screen, sprites
from data.core.utils import Mouse


def button_from_images(name: str, position: tuple[int, int],
                       on_click: Optional[Callable] = None,
                       on_release: Optional[Callable] = None):
    config = ImageButtonConfig(
        position=position, size=(0, 0),
        images=[pygame.transform.scale_by(images, 3) for images in sprites(name)],
        on_click=on_click, on_release=on_release)
    return ImageButton(config)


def checktoggle(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.toggled:
            method(self, *args, **kwargs)
    return wrapper


@dataclass
class ButtonConfig:
    position: tuple[int, int]
    size: tuple[int, int]
    align: RectAlignments = "topleft"
    colors: Optional[tuple[tuple | pygame.Color]] = None
    border_colors: Optional[tuple[tuple | pygame.Color]] = None
    border_thickness: int = 0
    radius: int = 0
    click_audio: Optional[str] = None
    release_audio: Optional[str] = None
    sub_widget: bool = False


class ClickInputMixin:
    def __init__(self, on_click: Optional[Callable] = None,
                 on_release: Optional[Callable] = None):
        self.on_click_call = on_click
        self.on_release_call = on_release
        self.clicked = False

    def update_click(self):
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

    def update_idle(self):
        """Method that is called when the button is idle."""
        self.clicked = False
        if self.colors is not None:
            self.color = self.colors[0]
        if self.border_colors is not None:
            self.border_color = self.border_colors[0]

    def update(self):
        if self._requires_realignment:
            self._align_rect(self._rect, self._align, (self._x, self._y))
        x, y = InputManager.get_mouse_pos()
        if self.contains(x, y):
            # button is released
            if InputManager.is_mouse_up(Mouse.LEFTCLICK) and self.clicked:
                self.update_release()
                self.on_release_call() if self.on_release_call is not None else None
            # button is clicked
            elif InputManager.is_mouse_down(Mouse.LEFTCLICK):
                self.update_click()
                self.on_click_call() if self.on_click_call is not None else None
            # button hovered
            elif not self.clicked:
                self.update_hover()
        # button not interacted with
        else:
            self.update_idle()


class ToggleInputMixin:
    def __init__(self):
        self.toggled = False

    def toggle_on(self):
        """Turn the toggle state on."""
        self.toggled = True
        if self.click_audio_tag is not None:
            button_audio.play_audio(self.click_audio_tag, override=True)
        if self.colors is not None:
            self.color = self.colors[2]
        if self.border_colors is not None:
            self.border_color = self.border_colors[2]

    def toggle_off(self):
        """Turn the toggle state off."""
        self.toggled = False
        if self.release_audio_tag is not None:
            button_audio.play_audio(self.release_audio_tag, override=True)

    @checktoggle
    def update_hover(self):
        if self.colors is not None:
            self.color = self.colors[1]
        if self.border_colors is not None:
            self.border_color = self.border_colors[1]

    @checktoggle
    def update_idle(self):
        if self.colors is not None:
            self.color = self.colors[0]
        if self.border_colors is not None:
            self.border_color = self.border_colors[0]

    def update(self):
        if self._requires_realignment:
            self._align_rect(self._rect, self._align, (self._x, self._y))
        x, y = InputManager.get_mouse_pos()
        if self.contains(x, y):
            if InputManager.is_mouse_down(Mouse.LEFTCLICK) and not self.toggled:
                self.toggle_on()
            elif InputManager.is_mouse_down(Mouse.LEFTCLICK) and self.toggled:
                self.toggle_off()
            elif not self.toggled:
                self.update_hover()
        else:
            self.update_idle()


class ButtonBase(WidgetBase):
    """Base class for creating buttons."""

    def __init__(self, config: ButtonConfig):
        WidgetBase.__init__(self, config.position, config.align, config.sub_widget)
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
    def width(self, value):
        self._width = value
        self._rect.width = self._width
        if self.border_colors is not None:
            self._border_rect.width = self._width - self._border_thickness * 2
        self._align_rect(self._rect, self._align, (self._x, self._y))

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value):
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
    def border_thickness(self, value):
        self._border_thickness = value
        self._border_rect.size = (
            self._width - self._border_thickness * 2,
            self._height - self._border_thickness * 2)
        self._border_rect.topleft = (
            self._rect.left + self._border_thickness,
            self._rect.top + self._border_thickness)

    def _align_rect(self, rect: pygame.Rect, align: RectAlignments,
                    coords: tuple[int, int]):
        setattr(rect, align, coords)
        self._x, self._y = getattr(rect, align)

    def contains(self, x: int, y: int) -> bool:
        return (self._rect.left < x - screen.get_abs_offset()[0] <
                self._rect.left + self._width) and \
               (self._rect.top < y - screen.get_abs_offset()[1] <
                self._rect.top + self._height)

    def blit(self):
        if self.border_colors is not None:
            pygame.draw.rect(screen, self.border_color, self._border_rect,
                             border_radius=self.radius)
        if self.colors is not None:
            pygame.draw.rect(screen, self.color, self._rect,
                             border_radius=self.radius)


@dataclass(kw_only=True)
class ToggleableTextButtonConfig(ButtonConfig):
    """Dataclass containing arguments to be passed to the `TextButton` class.

    :param text_colors: A dict of the colors that correspond to the colors
        of the button text when it is default, hovered or clicked.
    :param text_align: Alignment of the text inside the button. Defaults
        to `()` in order to use center alignment.
    :param margin: The offset of the text in the button (when not using center
        alignment)
    """
    text: str
    text_colors: Optional[tuple[tuple | pygame.Color]] = None
    font: Optional[pygame.font.Font] = None
    font_size: int = 32
    text_align: tuple[str, str] = None
    margin: int = 20


class TextButtonBase(ButtonBase):
    """Class for creating buttons with text labels."""
    def __init__(self, config: ToggleableTextButtonConfig):
        self.text_colors = (config.text_colors or
                            tuple(pygame.Color("White") for _ in range(3)))
        self._text_color = self.text_colors[0]
        self._text = Text((0, 0), config.text, config.font, config.font_size,
                          color=self._text_color, sub_widget=True)

        self.text_align = config.text_align
        self.margin = config.margin
        super().__init__(config)
        logging.info("Created %r.", self)

    def _align_text(self, text_surface):
        """Align the text within the button's rect based on the specified text
        alignment."""
        self.text_rect = text_surface.rect
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
        text_surface.x, text_surface.y = self.text_rect.topleft

    @property
    def text(self):
        return self._text

    @override
    def _align_rect(self, rect, align, coords):
        super()._align_rect(rect, align, coords)
        self._align_text(self._text)

    @override
    def blit(self):
        super().blit()
        self._text.blit()


class TextButtonConfig(ToggleableTextButtonConfig):
    on_click: Optional[Callable] = None
    on_release: Optional[Callable] = None


class TextButton(TextButtonBase, ClickInputMixin):
    def __init__(self, config: TextButtonConfig):
        TextButtonBase.__init__(self, config)
        ClickInputMixin.__init__(self, on_click=config.on_click,
                                 on_release=config.on_release)

    def update(self) -> None:
        ClickInputMixin.update(self)


class ToggleableTextButton(TextButtonBase, ToggleInputMixin):
    def __init__(self, config: ToggleableTextButtonConfig):
        TextButtonBase.__init__(self, config)
        ToggleInputMixin.__init__(self)

    def update(self) -> None:
        ToggleInputMixin.update(self)

class ToggleGroup:
    def __init__(self, *buttons):
        self.buttons = list(buttons)
        if self.buttons:
            # Automatically toggle on the first button
            self.buttons[0].toggle_on()

    def update(self):
        for button in self.buttons:
            button.update()

            # If a button is toggled on, ensure others are toggled off
            if button.toggled:
                for other_button in self.buttons:
                    if other_button != button and other_button.toggled:
                        other_button.toggle_off()

    def add_button(self, button):
        """Add more buttons to the group if needed."""
        self.buttons.append(button)
        if len(self.buttons) == 1:
            # Toggle the first button if it's the only one
            button.toggle_on()


@dataclass(kw_only=True)
class ImageButtonConfig(ButtonConfig):
    """Dataclass containing arguments to be passed to the `ImageButton` class.
    :param images: A tuple of images that correspond to the state of the button
        when default, hovered or clicked.
    :param use_rect_collisions: Whether to use the base rectangle for collision
        or if `False` will use the image to perform pixel-perfect collision
        checking.
    :param image_align: The alignment of the image inside the button. Defaults
        to `()` in order to use center alignment.
    :param margin: The offset of the image in the button (when not using center
        alignment)"""
    on_click: Optional[Callable] = None
    on_release: Optional[Callable] = None
    images: list
    use_rect_collisions: bool = False
    image_align: tuple[str, str] = None
    margin: int = 20


class ImageButton(ButtonBase, ClickInputMixin):
    """Button class that includes image rendering and allows for toggling
    between rect-based and pixel-perfect collision detection."""

    def __init__(self, config: ImageButtonConfig):
        ButtonBase.__init__(self, config)
        ClickInputMixin.__init__(self, on_click=config.on_click, on_release=config.on_release)
        self.images = config.images
        self._current_image = self.images[0]
        self.use_rect_collision = config.use_rect_collisions
        self.image_align = config.image_align
        self.margin = config.margin
        self._align_image()
        logging.info("Created %r.", self)

    @property
    def image_align(self):
        return self._image_align

    @image_align.setter
    def image_align(self, value):
        self._image_align = value
        self._align_image()

    def _align_image(self):
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
    def contains(self, x, y):
        if self.use_rect_collision:
            return super().contains(x, y)
        local_x = x - self.image_rect.left
        local_y = y - self.image_rect.top
        try:
            return self._current_image.get_at((local_x, local_y)).a != 0
        except IndexError:
            return False

    def on_click(self):
        ClickInputMixin.update_click(self)
        self._current_image = self.images[2]

    def on_hover(self):
        ClickInputMixin.update_hover(self)
        self._current_image = self.images[1]

    def on_idle(self):
        ClickInputMixin.update_idle(self)
        self._current_image = self.images[0]

    @override
    def update(self):
        ClickInputMixin.update(self)

    @override
    def blit(self):
        if self.use_rect_collision:
            pygame.draw.rect(screen, self.color, self._rect, border_radius=self.radius)

        screen.blit(self._current_image, self.image_rect.topleft)
