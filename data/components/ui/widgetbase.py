from abc import ABC, abstractmethod
from typing import override

import pygame

from data.components import InputManager, InputBinder
from data.components.ui import widgethandler
from data.core.utils import CustomTypes, Validator

class RenderNeeded(Validator):
    @override
    def _validate(self, instance, value):
        instance._requires_render = True
        instance._requires_rect_update = True


class RectUpdateNeeded(Validator):
    @override
    def _validate(self, instance, value):
        instance._requires_rect_update = True


class WidgetBase(ABC):
    """Base class for widgets."""
    def __init__(self, x: int, y: int, width: int, height: int,
                 align: CustomTypes.rect_alignments = 'topleft',
                 sub_widget: bool = False):
        """"""
        self._surface = pygame.display.get_surface()
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._align = align
        self._align_rect(self._rect, self._align, self._rect.topleft)
        self._coords = getattr(self._rect, self._align)
        self._input_manager = InputManager()
        self._input_binder = InputBinder()

        if not sub_widget:
            widgethandler.add_widget(self)

    def _align_rect(self, rect, align, coords):
        setattr(rect, align, coords)
        self._coords = self._x, self._y = getattr(rect, align)

    def contains(self, x: int, y: int):
        """Basic collision detection for the widget rectangle."""
        return (self._rect.left < x - self._surface.get_abs_offset()[0] <
                self._rect.left + self._width) and (
                self._rect.top < y - self._surface.get_abs_offset()[1] <
                self._rect.top + self._height)

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def blit(self):
        ...