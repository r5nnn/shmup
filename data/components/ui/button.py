"""Module for displaying buttons on the screen.

Buttons consist of a base rectangle with a label on top. The label can be text
or an image. The base rectangle can be hidden to use the image label as the
button itself. In this case pixel-perfect collision can also be used.
Buttons can be hovered and interacted with. An attribute of the button can
change or an action can be executed when the button is pressed down or released."""

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
class _ButtonConfig:
    """Dataclass containing arguments to be passed to the `_ButtonBase` class.
    
    Args:
        position: The position of the widget with reference to the `align`
            argument passed.
        size: The width and height of the button rect.
        align: The point of the widget that the `position` argument is
            referencing. Defaults to `'topleft'`.
        colors: A dict of the colors that correspond to the state of the
            button when default, hovered or clicked. Defaults to `None`
            to not display the rect.        
        border_colors: A dict of the colors that correspond to the state
            of the button border when default, hovered or clicked.
            Defaults to `None` to not display the border rect.
        border_thickness: The thickness of the border. Defaults to `0`.
        radius: The curvature of the corners of the button rect. Defaults
            to `0`.
        on_click: The action to call when the button is clicked. Defaults to
            `lambda *args: None` to not have an action.
        on_release: The action to call when the button is released. Defaults to
            `lambda *args: None` to not have an action.
        click_audio: The tag of the audio to play when the button is clicked.
            Defaults to `'click'`.
        release_audio: The tag of the audio to play when the button is released.
            Defaults to `'click'`.
        surface: The surface that the widget should be rendered to. Defaults
            to `None` to use the current display surface."""
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


class _ButtonBase(WidgetBase):
    """Base class for creating buttons.

    Includes the button base rectangle and input detection, but no label.
    Rectangle can change color depending on the status of the button (default,
    hovered or clicked).

    Attributes:
        colors: Dictionary of colors that correspond to the state of the button
            when default, hovered or clicked.
        border_colors: Dictionary of colors that correspond to the state of the
            button border when default, hovered or clicked.

    Args:
        config: A `_ButtonConfig` class containing the properties of the button. 
    """

    def __init__(self, config: _ButtonConfig):
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
        """The base button rectangle."""
        return self._rect

    @property
    def width(self) -> int:
        """The width of the button base rectangle."""
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
        """The height of the button base rectangle."""
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
        """The thickness of the border around the button rectangle, in pixels."""
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
        """Basic collision detection for the button rectangle."""
        return (self._rect.left < x - self.surface.get_abs_offset()[0] <
                self._rect.left + self._width) and \
               (self._rect.top < y - self.surface.get_abs_offset()[1] <
                self._rect.top + self._height)

    def on_click(self) -> None:
        """Method that is called when the button is clicked.

        Plays audio if set, updates the color and border colors."""
        self.clicked = True
        if self.click_audio_tag is not None:
            button_audio.play_audio(self.click_audio_tag, override=True)
        if self.colors is not None:
            self._color = self.colors['clicked']
        if self.border_colors is not None:
            self._border_color = self.border_colors.get('clicked')

    def on_release(self) -> None:
        """Method that is called when the button is released.

        Plays audio if set."""
        self.clicked = False
        if self.release_audio_tag is not None:
            button_audio.play_audio(self.release_audio_tag, override=True)

    def on_hover(self) -> None:
        """Method that is called when the button is hovered.

        Updates the color and border colors."""
        if self.colors is not None:
            self._color = self.colors['hovered']
        if self.border_colors is not None:
            self._border_color = self.border_colors.get('hovered')

    def on_idle(self):
        """Method that is called when the button is idle (i.e. not clicked or hovered)

        Updates the color and border colors."""
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
class TextButtonConfig(_ButtonConfig):
    text: str
    text_colors: Optional[dict[str, tuple[int, ...]]] = None
    font: Optional[pygame.font.Font] = None
    font_size: int = 32
    text_align: Optional[tuple[str, str]] = None
    margin: int = 20


class TextButton(_ButtonBase):
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

        # Text instance
        self._text = Text((0, 0), config.text, config.font, config.font_size,
                          color=self._text_color)
        self.text_align = config.text_align
        self.margin = config.margin

        # Align the text inside the button's rect
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
        """Aligns the text relative to the button rect."""
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

    def blit(self):
        """Draw the button and its text onto the surface."""
        super().blit()
        self._text.blit()


@dataclass(kw_only=True)
class ImageButtonConfig(_ButtonConfig):
    images: tuple
    use_rect_collisions: bool = False
    image_align: tuple[str, str] = ()


class ImageButton(_ButtonBase):
    def __init__(self, config: ImageButtonConfig):
        """
        Button class that includes image rendering and allows for toggling
        between rect-based and pixel-perfect collision detection.
        """
        super().__init__(config)

        self.images = config.images
        self._current_image = self.images[0]
        self.use_rect_collision = config.use_rect_collisions
        self.image_align = config.image_align

        self._align_image()

    @property
    def image_align(self):
        return self._image_align

    @image_align.setter
    def image_align(self, value):
        self._image_align = value
        self._align_image()

    def _align_image(self):
        """Aligns the image relative to the button's rect."""
        self.image_rect = self._current_image.get_rect()
        self.image_rect.center = self._rect.center

        if len(self.image_align) == 2:
            if self.image_align[0] == 'left':
                self.image_rect.left = self._rect.left
            elif self.image_align[0] == 'right':
                self.image_rect.right = self._rect.right

            if self.image_align[1] == 'top':
                self.image_rect.top = self._rect.top
            elif self.image_align[1] == 'bottom':
                self.image_rect.bottom = self._rect.bottom

    @override
    def contains(self, x, y):
        """Check if the mouse is over the image or rect, depending on collision
        mode."""
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

    def blit(self):
        """Draw the image onto the surface. Optionally draw the button rect if
        using rect collision."""
        if self.use_rect_collision:
            pygame.draw.rect(self.surface, self._color, self._rect, border_radius=self.radius)

        self.surface.blit(self._current_image, self.image_rect.topleft)
