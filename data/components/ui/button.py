"""Module for displaying buttons on the screen.

Buttons consist of a base rectangle with a label on top. The label can be text
or an image. The base rectangle can be hidden to use the image label as the
button itself. In this case pixel-perfect collision can also be used.
Buttons can be hovered and interacted with. An attribute of the button can
change or an action can be executed when the button is pressed down or released.
"""
from dataclasses import dataclass
from typing import Callable, override, Optional

import pygame.display

from data.components.audio import button_audio
from data.components.input import inputmanager
from data.core.utils import CustomTypes
from data.core.utils import Mouse
from .text import Text
from .widgetutils import WidgetBase


@dataclass
class ButtonConfig:
    """Dataclass containing arguments to be passed to the `ButtonBase` class.

    :param position: The position of the widget with reference to the `align`
            argument passed.
    :param size: The width and height of the button rect.
    :param align: The point of the widget that the `position` argument is
            referencing. Defaults to `'topleft'`.
    :param colors: A dict of the colors that correspond to the state of the
            button when default, hovered or clicked. Defaults to `None`
            to not display the rect.
    :param border_colors: A dict of the colors that correspond to the state
            of the button border when default, hovered or clicked.
            Defaults to `None` to not display the border rect.
    :param border_thickness: The thickness of the border. Defaults to `0`.
    :param radius: The curvature of the corners of the button rect. Defaults
            to `0`.
    :param on_click: The action to call when the button is clicked. Defaults to
            `lambda *args: None` to not have an action.
    :param on_release: The action to call when the button is released. Defaults to
            `lambda *args: None` to not have an action.
    :param click_audio: The tag of the audio to play when the button is clicked.
            Defaults to `'click'`.
    :param release_audio: The tag of the audio to play when the button is released.
            Defaults to `'click'`.
    :param surface: The surface that the widget should be rendered to. Defaults
            to `None` to use the current display surface.
    """
    position: tuple[int, int]
    size: tuple[int, int]
    align: CustomTypes.rect_alignments = 'topleft'
    colors: Optional[dict[str, tuple[int, ...]]] = None
    border_colors: Optional[dict[str, tuple[int, ...]]] = None
    border_thickness: int = 0
    radius: int = 0
    on_click: Callable = lambda *args: None
    on_release: Callable = lambda *args: None
    click_audio: Optional[str] = 'click'
    release_audio: Optional[str] = 'click'
    surface: Optional[pygame.Surface] = None


class ButtonBase(WidgetBase):
    """Base class for creating buttons."""

    def __init__(self, config: ButtonConfig):
        WidgetBase.__init__(self, config.position, config.align, config.surface)
        self._width, self._height = config.size
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self.colors = config.colors
        self._color = self.colors['default'] if self.colors is not None else None
        self.border_colors = config.border_colors
        self._border_color = self.border_colors['default'] \
            if self.border_colors is not None else None
        self._border_thickness = config.border_thickness
        self._border_rect = pygame.Rect(self._rect.left + self._border_thickness,
                                        self._rect.top + self._border_thickness,
                                        self._width - self._border_thickness * 2,
                                        self._height - self._border_thickness * 2)
        self.on_click_call = config.on_click
        self.on_release_call = config.on_release
        self.click_audio_tag = config.click_audio
        self.release_audio_tag = config.release_audio
        self.radius = config.radius
        self.clicked = False

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
        self._align_rect(self._rect, self._align, self._coords)

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self._rect.height = self._height
        if self.border_colors is not None:
            self._border_rect.height = (self._height - self._border_thickness * 2)
        self._align_rect(self._rect, self._align, self._coords)

    @property
    def border_thickness(self) -> int:
        """How wide the border should be, in pixels."""
        return self._border_thickness

    @border_thickness.setter
    def border_thickness(self, value):
        self._border_thickness = value
        self._border_rect.size = (self._width - self._border_thickness * 2,
                                  self._height - self._border_thickness * 2)
        self._border_rect.topleft = (self._rect.left + self._border_thickness,
                                     self._rect.top + self._border_thickness)

    def _align_rect(self, rect, align, coords):
        setattr(rect, align, coords)
        self._coords = self._x, self._y = getattr(rect, align)

    def contains(self, x: int, y: int) -> bool:
        """Used to check if a point (usually position of the mouse) is inside
        the button."""
        return (self._rect.left < x - self.surface.get_abs_offset()[0] <
                self._rect.left + self._width) and \
               (self._rect.top < y - self.surface.get_abs_offset()[1] <
                self._rect.top + self._height)

    def on_click(self) -> None:
        """Method that is called when the button is clicked."""
        self.clicked = True
        if self.click_audio_tag is not None:
            button_audio.play_audio(self.click_audio_tag, override=True)
        if self.colors is not None:
            self._color = self.colors['clicked']
        if self.border_colors is not None:
            self._border_color = self.border_colors.get('clicked')

    def on_release(self) -> None:
        """Method that is called when the button is released."""
        self.clicked = False
        if self.release_audio_tag is not None:
            button_audio.play_audio(self.release_audio_tag, override=True)

    def on_hover(self) -> None:
        """Method that is called when the button is hovered."""
        if self.colors is not None:
            self._color = self.colors['hovered']
        if self.border_colors is not None:
            self._border_color = self.border_colors.get('hovered')

    def on_idle(self):
        """Method that is called when the button is idle (i.e. not clicked or
        hovered)"""
        self.clicked = False
        if self.colors is not None:
            self._color = self.colors['default']
        if self.border_colors is not None:
            self._border_color = self.border_colors.get('default')

    @override
    def update(self):
        x, y = inputmanager.get_mouse_pos()
        if self.contains(x, y):
            # button is released
            if inputmanager.is_mouse_up(Mouse.LEFTCLICK) and self.clicked:
                self.on_release()
                self.on_release_call()
            # button is clicked
            elif inputmanager.is_mouse_down(Mouse.LEFTCLICK):
                self.on_click()
                self.on_click_call()
            # button hovered
            elif not self.clicked:
                self.on_hover()
        # button not interacted with
        else:
            self.on_idle()

    @override
    def blit(self):
        if self.border_colors is not None:
            pygame.draw.rect(self.surface, self._border_color,
                             self._border_rect, border_radius=self.radius)
        if self.colors is not None:
            pygame.draw.rect(self.surface, self._color,
                             self._rect, border_radius=self.radius)


@dataclass(kw_only=True)
class TextButtonConfig(ButtonConfig):
    """Dataclass containing arguments to be passed to the `TextButton` class.

    :param text_colors: A dict of the colors that correspond to the colors
        of the button text when it is default, hovered or clicked.
    :param text_align: Alignment of the text inside the button. Defaults
        to `()` in order to use center alignment.
    :param margin: The offset of the text in the button (when not using center
        alignment)
    """
    text: str
    text_colors: Optional[dict[str, tuple[int, ...]]] = None
    font: Optional[pygame.font.Font] = None
    font_size: int = 32
    text_align: Optional[tuple[str, str]] = None
    margin: int = 20


class TextButton(ButtonBase):
    """Class for creating buttons with text labels."""

    def __init__(self, config: TextButtonConfig):
        super().__init__(super(TextButtonConfig, config))
        self.text_colors = config.text_colors \
            if config.text_colors is not None else {
                'default': (255, 255, 255),
                'hovered': (255, 255, 255),
                'clicked': (255, 255, 255)
            }
        self._text_color = self.text_colors['default']
        self._text = Text((0, 0), config.text, config.font, config.font_size,
                          color=self._text_color)
        self.text_align = config.text_align
        self.margin = config.margin
        self._align_text(self._text)

    @property
    def surface(self):
        return self.surface

    @surface.setter
    def surface(self, value):
        self.surface = value
        self._text.surface = value

    @property
    def text_align(self):
        return self._text_align

    @text_align.setter
    def text_align(self, value):
        self._text_align = value
        self._align_text(self._text) if self._text is not None else None

    def _align_text(self, surface):
        self.text_rect = surface.rect
        self.text_rect.center = self._rect.center

        if len(self.text_align) == 2:
            if self.text_align[0] == 'left':
                self.text_rect.left = self._rect.left + self.margin
            elif self.text_align[0] == 'right':
                self.text_rect.right = self._rect.right - self.margin
            if self.text_align[1] == 'top':
                self.text_rect.top = self._rect.top + self.margin
            elif self.text_align[1] == 'bottom':
                self.text_rect.bottom = self._rect.bottom - self.margin

        surface.x, surface.y = self.text_rect.left, self.text_rect.top

    @override
    def on_click(self):
        super().on_click()
        self._text.color = self.text_colors['clicked']

    @override
    def on_hover(self):
        self._text.color = self.text_colors['hovered']

    @override
    def on_idle(self):
        self._text.color = self.text_colors['inactive']

    @override
    def update(self):
        """Updates the button and the text color based on mouse state."""
        super().update()
        self._text.update()

    @override
    def blit(self):
        """Draw the button and its text onto the surface."""
        super().blit()
        self._text.blit()


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
    images: tuple
    use_rect_collisions: bool = False
    image_align: tuple[str, str] = ()
    margin: int = 20


class ImageButton(ButtonBase):
    """Button class that includes image rendering and allows for toggling
    between rect-based and pixel-perfect collision detection."""

    def __init__(self, config: ImageButtonConfig):
        super().__init__(config)

        self.images = config.images
        self._current_image = self.images[0]
        self.use_rect_collision = config.use_rect_collisions
        self.image_align = config.image_align
        self.margin = config.margin

        self._align_image()

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

        if len(self.image_align) == 2:
            if self.image_align[0] == 'left':
                self.image_rect.left = self._rect.left + self.margin
            elif self.image_align[0] == 'right':
                self.image_rect.right = self._rect.right - self.margin

            if self.image_align[1] == 'top':
                self.image_rect.top = self._rect.top + self.margin
            elif self.image_align[1] == 'bottom':
                self.image_rect.bottom = self._rect.bottom - self.margin

    @override
    def contains(self, x, y):
        if self.use_rect_collision:
            return super().contains(x, y)  # Use rect-based collision
        else:
            local_x = x - self.image_rect.left
            local_y = y - self.image_rect.top
            try:
                # Pixel-perfect collision
                return self._current_image.get_at((local_x, local_y)).a != 0
            except IndexError:
                return False

    @override
    def on_click(self):
        super().on_click()
        self._current_image = self.images[2]

    @override
    def on_hover(self):
        super().on_hover()
        self._current_image = self.images[1]

    @override
    def on_idle(self):
        super().on_idle()
        self._current_image = self.images[0]

    @override
    def update(self):
        """Updates the button based on mouse state."""
        super().update()

    @override
    def blit(self):
        """Optionally draw the button rect if using rect collision."""
        if self.use_rect_collision:
            pygame.draw.rect(self.surface, self._color, self._rect, border_radius=self.radius)

        self.surface.blit(self._current_image, self.image_rect.topleft)
