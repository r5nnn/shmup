from typing import Callable

import pygame.display
from .text import Text
from data.utils import CustomTypes, Mouse
from data.components.input import InputManager, InputBinder


class _ButtonBase:
    def __init__(self,
                 surface: pygame.Surface,
                 rect: pygame.Rect,
                 align: CustomTypes.rect_alignments = 'topleft',
                 colors: dict[str, tuple] = None,
                 border: bool = False,
                 border_colors: dict[str, tuple] = None,
                 border_thickness: int = 0,
                 on_click: Callable = None,
                 on_release: Callable = None,
                 radius: int = 0):
        """
        Base class for button functionality.

        Handles the basic appearance and interaction such as border, colors,
        and on-click/on-release events. Child classes will add text or
        image-specific logic.
        """
        self.input_manager = InputManager()
        self.input_binder = InputBinder()
        self.surface = surface
        self._rect = rect
        self._width = self._rect.width
        self._height = self._rect.height
        self._align = align
        self._align_rect(self._rect, self._align, self._rect.topleft)
        self._coords = getattr(self._rect, self._align)

        # Color management
        self.colors = colors if colors is not None else None
        self._color = self.colors[
            'inactive'] if self.colors is not None else None

        # Border management
        self.border = border
        self.border_colors = border_colors if border_colors is not None \
            else None
        self._border_color = self.border_colors[
            'inactive'] if self.border_colors else None
        self._border_thickness = border_thickness
        self._border_rect = pygame.Rect(
            self._rect.left + self._border_thickness,
            self._rect.top + self._border_thickness,
            self._width - self._border_thickness * 2,
            self._height - self._border_thickness * 2
        )

        # Event handlers
        self.on_click = on_click if on_click is not None else lambda *args: \
            None
        self.on_release = on_release if on_release is not None else lambda \
            *args: None

        self.radius = radius
        self.clicked = False
        self._disabled = False

    @property
    def rect(self):
        return self._rect

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self._rect.width = self._width
        if self.border:
            self._border_rect.width = self._width - self._border_thickness * 2
        self._align_rect(self._rect, self._align, self._coords)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self._rect.height = self._height
        if self.border:
            self._border_rect.height = (self._height - self._border_thickness *
                                        2)
        self._align_rect(self._rect, self._align, self._coords)

    @property
    def color(self):
        return self._color

    @property
    def border_color(self):
        return self._border_color

    @property
    def border_thickness(self):
        return self._border_thickness

    @border_thickness.setter
    def border_thickness(self, value):
        self._border_thickness = value
        self._border_rect.size = (self._width - self._border_thickness * 2,
                                  self._height - self._border_thickness * 2)
        self._border_rect.topleft = (self._rect.left + self._border_thickness,
                                     self._rect.top + self._border_thickness)

    def contains(self, x, y):
        """Basic collision detection for the button rectangle."""
        return (self._rect.left < x - self.surface.get_abs_offset()[0]
                < self._rect.left + self._width) and \
            (self._rect.top < y - self.surface.get_abs_offset()[1]
             < self._rect.top + self._height)

    def _align_rect(self, rect, align, coords):
        setattr(rect, align, coords)
        self._coords = self._x, self._y = getattr(rect, align)

    def update(self):
        """Updates the button based on mouse state."""
        if not self._disabled:
            x, y = self.input_manager.get_mouse_pos()
            if self.contains(x, y):
                if (self.input_manager.is_mouse_up(Mouse.LEFTCLICK) and
                    self.clicked):
                    self.clicked = False
                    self.on_release()

                elif self.input_manager.is_mouse_down(Mouse.LEFTCLICK):
                    self.clicked = True
                    self.on_click()
                    if self.colors is not None:
                        self._color = self.colors['clicked']
                    if self.border_colors is not None:
                        self._border_color = self.border_colors.get('clicked')

                elif (self.input_manager.is_key_down(Mouse.LEFTCLICK) and
                      self.clicked):
                    if self.colors is not None:
                        self._color = self.colors['clicked']
                    if self.border_colors is not None:
                        self._border_color = self.border_colors.get('clicked')

                else:
                    if self.colors is not None:
                        self._color = self.colors['hovered']
                    if self.border_colors is not None:
                        self._border_color = self.border_colors.get('hovered')

            else:
                self.clicked = False
                if self.colors is not None:
                    self._color = self.colors['inactive']
                if self.border_colors is not None:
                    self._border_color = self.border_colors.get('inactive')

    def blit(self):
        """Draws the button onto the surface."""
        if self.border:
            pygame.draw.rect(
                self.surface, self.border_color, self._border_rect,
                border_radius=self.radius
            )
        if self.colors is not None:
            pygame.draw.rect(
                self.surface, self.color, self._rect,
                border_radius=self.radius
            )


class ButtonText(_ButtonBase):
    def __init__(self,
                 surface: pygame.Surface,
                 rect: pygame.Rect,
                 text: str = "",
                 text_colors: dict[str, tuple] = None,
                 font: pygame.font.Font = None,
                 font_size: int = 32,
                 text_align: tuple[str, str] = (),
                 margin: int = 20,
                 **kwargs):
        """
        Button class that includes text rendering and color management.
        """
        super().__init__(surface, rect, **kwargs)

        self.text_colors = text_colors if text_colors is not None else \
            {'inactive': (255, 255, 255),
             'hovered': (255, 255, 255),
             'clicked': (255, 255, 255)}
        self._text_color = self.text_colors['inactive']

        # Text instance
        self._text = Text(self.surface, text, (0, 0), font_size, font,
                          color=self._text_color)
        self.text_align = text_align
        self.margin = margin

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

        surface.coords = self.text_rect.left, self.text_rect.top

    def blit(self):
        """Draw the button and its text onto the surface."""
        super().blit()
        self._text.blit()

    def update(self):
        """Updates the button and the text color based on mouse state."""
        super().update()
        x, y = self.input_manager.get_mouse_pos()
        if self.contains(x, y):
            self._text.color = self.text_colors[
                'hovered'] if not self.clicked else self.text_colors['clicked']
        else:
            self._text.color = self.text_colors['inactive']
        self._text.update()


class ButtonImage(_ButtonBase):
    def __init__(self,
                 surface: pygame.Surface,
                 rect: pygame.Rect,
                 images: tuple,
                 use_rect_collision: bool = False,
                 image_align: tuple[str, str] = (),
                 **kwargs):
        """
        Button class that includes image rendering and allows for toggling
        between rect-based and pixel-perfect collision detection.
        """
        super().__init__(surface, rect, **kwargs)

        self.images = images
        self._current_image = self.images[0]
        self.use_rect_collision = use_rect_collision
        self.image_align = image_align

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

    def update(self):
        """Updates the button based on mouse state."""
        super().update()
        x, y = self.input_manager.get_mouse_pos()
        if self.contains(x, y):
            if not self.clicked:
                self._current_image = self.images[1]  # Hover
            else:
                self._current_image = self.images[2]  # Clicked
        else:
            self._current_image = self.images[0]  # Idle

    def blit(self):
        """Draw the image onto the surface. Optionally draw the button rect if
        using rect collision."""
        if self.use_rect_collision:
            pygame.draw.rect(self.surface, self._color, self._rect,
                             border_radius=self.radius)

        self.surface.blit(self._current_image, self.image_rect.topleft)
