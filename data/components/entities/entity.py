"""Contains the base class for all the game's entities and a group for managing them."""
from typing import override, Optional

import pygame.display
from pygame.sprite import Sprite

from data.components import RectAlignments


class Entity(Sprite):
    """Base class for all the game's entities."""
    def __init__(self, spawn: tuple[int, int], sprite: pygame.Surface,
                 sprite_rect: Optional[pygame.Rect] = None,
                 spawn_alignment: RectAlignments = 'center'):
        Sprite.__init__(self)
        self._spawn = spawn
        self.spawn_alignment = spawn_alignment
        self.sprite = sprite
        self._rect = sprite_rect if sprite_rect is not None else sprite.get_rect()
        self.move_to_spawn()

    @property
    def spawn(self):
        return self._spawn

    @property
    def rect(self):
        return self._rect

    def move_to_spawn(self):
        setattr(self._rect, self.spawn_alignment, self._spawn)

    @override
    def update(self):
        ...

    def blit(self):
        ...

    def on_collide(self, collided_sprite):
        ...

    def __repr__(self):
        return (f"Entity(spawn={self.spawn!r}, sprite={self.sprite!r}, "
                f"sprite_rect={self.rect!r}, spawn_alignment={self.spawn_alignment})")


class EntityGroup(pygame.sprite.Group):
    """Child class of `pygame.sprite.Group` that includes a `blit()` method."""
    def __init__(self):
        super().__init__()

    def blit(self):
        for sprite in self.sprites():
            sprite.blit()
