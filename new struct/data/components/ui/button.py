from typing import Callable

import pygame.display

from . import RectUpdateNeeded
from .text import Text
from ..events import Mouse
from ...globals import button_colors, rect_alignments


class Button:
    coords = RectUpdateNeeded()
    align = RectUpdateNeeded()

    def __init__(self,
                 surface: pygame.Surface,
                 rect: pygame.Rect,
                 align: rect_alignments = 'topleft',
                 colors: dict[str, tuple] = None,
                 border: bool = False,
                 border_colors: dict[str, tuple] = None,
                 border_thickness: int = 0,
                 on_click: Callable = None,
                 on_release: Callable = None,
                 text: str = "",
                 text_align: tuple[str, str] = (),
                 text_colors: dict[str, tuple] = None,
                 font: pygame.font.Font = None,
                 font_size: int = 32,
                 image: pygame.Surface = None,
                 image_align: tuple[str, str] = (),
                 margin: int = 20,
                 radius: int = 0):
        """
        Class for creating and updating buttons.
        
        Button consists of a background rect, optional border and text or image
        surface.
        Allows for customising the button and text color when clicked and 
        hovered as well as calling functions on click and on release.

        :param surface: Surface which the text surface will be blit onto.
        :param align: Alignment of the button background rect coordinates.
        :param colors: Dictionary of colors that the button background rect will
        cycle through upon clicking or hovering the button.
        :param border_colors: Dictionary of colors that the button border rect
        will cycle through upon clicking or hovering the button.
        :param border_thickness: Thickness of the border around the button
        background rect.
        :param on_click: Function to call when clicking the button.
        :param on_release: Function to call when releasing the button after
        clicking.
        :param text: Text to display on the button.
        :param text_align: Alignment of the text in the button.
        :param text_colors: Dictionary of colors that the button text will
        cycle through upon clicking or hovering the button.
        :param font: Font of the text to display.
        :param image: Image to display on the button
        :param image_align: Alignment of the image in the button.
        :param margin: Margin to use when aligning text or images on the button.
        :param radius: The amount of curve the button background rect should
        have on the corners.
        """
        self._surface = surface
        self._rect = rect
        self._width = self._rect.width
        self._height = self._rect.height
        self._align = align
        self._align_rect(self._rect, self._align, self._rect.topleft)
        self._coords = getattr(self._rect, self._align)
        self.colors = colors if colors is not None else button_colors
        self._color = self.colors['inactive']
        self.border = border
        self.border_colors = border_colors if border_colors is not None \
            else button_colors
        self._border_color = self.border_colors['inactive']
        self._border_thickness = border_thickness
        # no need to align border rect as button rect already aligned.
        self._border_rect = pygame.Rect(
            self._rect.left + self._border_thickness,
            self._rect.top + self._border_thickness,
            self._width - self._border_thickness * 2,
            self._height - self._border_thickness * 2)
        self.on_click = on_click if on_click is not None else lambda *args: None
        self.on_release = on_release if on_release is not None else \
            lambda *args: None
        self.text_colors = text_colors if text_colors is not None else \
            {'inactive': (255, 255, 255),
             'hovered': (255, 255, 255),
             'clicked': (255, 255, 255)}
        self._text_color = self.text_colors['inactive']
        self._text = Text(self._surface, text, (0, 0), font, font_size,
                          color=self._text_color)
        self.text_align = text_align
        self.image = image if image is not None else None
        self.image_align = image_align
        self.margin = margin
        self.radius = radius

        self.clicked = False
        self._disabled = False

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value):
        self._surface = value
        self._text.surface = value

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
            self._border_rect.height = self._height - self._border_thickness * 2
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

    @property
    def text_align(self):
        return self._text_align

    @text_align.setter
    def text_align(self, value):
        self._text_align = value
        self._align_text(self._text) if self._text is not None else None

    @property
    def image_align(self):
        return self._image_align

    @image_align.setter
    def image_align(self, value):
        self._image_align = value
        self._align_image(self.image) if self.image is not None else None

    def contains(self, x, y):
        return (self._rect.left < x - self._surface.get_abs_offset()[0]
                < self._rect.left + self._width) and \
               (self._rect.top < y - self._surface.get_abs_offset()[1]
                < self._rect.top + self._height)

    def _align_rect(self, rect, align, coords):
        self._requires_rect_update = False
        setattr(rect, align, coords)

    def _align_text(self, surface):
        self.text_rect = surface.rect
        self.text_rect.center = self._rect.center

        if len(self.text_align) == 2:
            if self.text_align[0] == 'left':
                self.text_rect.left = self.x + self.margin
            elif self.text_align[0] == 'right':
                self.text_rect.right = self.x + self.width - self.margin

            if self.text_align[1] == 'top':
                self.text_rect.top = self.y + self.margin
            elif self.text_align[1] == 'bottom':
                self.text_rect.bottom = self.y + self.height - self.margin

        surface.coords = self.text_rect.left, self.text_rect.top

    def _align_image(self, surface):
        self._image_rect = surface.get_rect()
        self._image_rect.center = (self.x + self.width // 2, self.y +
                                   self.height // 2)

        if len(self.image_align) == 2:
            if self.image_align[0] == 'left':
                self._image_rect.left = self.x + self.margin
            elif self.image_align[0] == 'right':
                self._image_rect.right = self.x + self.width - self.margin

            if self.image_align[1] == 'top':
                self._image_rect.top = self.y + self.margin
            elif self._image_align[1] == 'bottom':
                self._image_rect.bottom = self.y + self.height - self.margin

    def update(self):
        if not self._disabled:
            mouse_state = Mouse.get_mouse_state()
            x, y = Mouse.get_mouse_pos()
            if self.contains(x, y):
                if mouse_state == mouse_state.RELEASE and self.clicked:
                    self.clicked = False
                    self.on_release()

                elif mouse_state == mouse_state.CLICK:
                    self.clicked = True
                    self.on_click()
                    self._color = self.colors['clicked']
                    self._text_color = self.text_colors['clicked']
                    self._border_color = self.border_colors.get('clicked')

                elif mouse_state == mouse_state.DRAG and self.clicked:
                    self._color = self.colors['clicked']
                    self._border_color = self.border_colors['clicked']

                elif (mouse_state == mouse_state.HOVER or
                      mouse_state == mouse_state.DRAG):
                    self._color = self.colors['hovered']
                    self._border_color = self.border_colors.get('hovered')

            else:
                self.clicked = False
                self._color = self.colors['inactive']
                self._border_color = self.border_colors.get('inactive')

    def blit(self):
        if self._requires_rect_update:
            self._align_rect(self._rect, self._align, self._coords)
        if self.border:
            pygame.draw.rect(
                self._surface, self.border_color, self._border_rect,
                border_radius=self.radius)
        pygame.draw.rect(
            self._surface, self.color, self._rect,
            border_radius=self.radius)
        if self.image is not None:
            self._surface.blit(self.image, self._image_rect)
        self._text.blit() if self._text is not None else None
