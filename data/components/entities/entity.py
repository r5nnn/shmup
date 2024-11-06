"""Contains the base class for all the game's entities and a group for managing them."""
from abc import ABC, abstractmethod
from typing import override, Optional

import pygame.display
from pygame.sprite import Sprite

from data.components import RectAlignments


class Entity(ABC, Sprite):
    """Base class for all the game's entities."""
    def __init__(self, spawn: tuple[int, int], sprite: pygame.Surface,
                 sprite_rect: Optional[pygame.Rect] = None,
                 spawn_alignment: RectAlignments = 'center'):
        Sprite.__init__(self)
        self.spawn = spawn
        self.spawn_alignment = spawn_alignment
        self.rect = sprite_rect if sprite_rect is not None else sprite.get_rect()
        self._spawn()
        self.sprite = sprite

    def _spawn(self):
        setattr(self.rect, self.spawn_alignment, self.spawn)

    @override
    def update(self):
        ...

    @abstractmethod
    def blit(self):
        ...

    @abstractmethod
    def on_collide(self, sprite):
        ...


class EntityGroup(pygame.sprite.Group):
    """Child class of `pygame.sprite.Group` that includes a `blit()` method."""
    def __init__(self):
        super().__init__()

    def blit(self):
        for sprite in self.sprites():
            sprite.blit()
