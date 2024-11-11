import math
from typing import Optional, override

import pygame

from data.components import RectAlignments
from data.components.entities.entity import Entity
from data.core import screen_rect
from data.core.utils import dt


class Projectile(Entity):
    def __init__(self, owner: Entity,
                 sprite: Optional[pygame.Surface] = None,
                 spawn_location: RectAlignments = 'midtop',
                 spawn_alignment: RectAlignments = 'midbottom',
                 sprite_rect: Optional[pygame.Rect] = None):
        if not (sprite or sprite_rect):
            raise ValueError('Must provide either sprite or sprite_rect, not '
                             'neither.')
        if sprite is None:
            current_sprite = pygame.Surface(sprite_rect.size)
            current_sprite.fill(pygame.Color('white'))
        else:
            current_sprite = sprite
        super().__init__(getattr(owner.abs_rect, spawn_location),
                         sprite=current_sprite, sprite_rect=sprite.get_rect() \
                            if sprite_rect is None else sprite_rect,
                         spawn_alignment=spawn_alignment)

    @override
    def update(self):
        if not screen_rect.contains(self._rect):
            self.kill()

    @override
    def blit(self):
        super().blit()

    @override
    def on_collide(self, collided_sprite):
        ...


class SimpleBullet(Projectile):
    def __init__(self, owner: Entity, sprite: Optional[pygame.Surface] = None,
                 spawn_location: RectAlignments = 'midtop', spawn_alignment: RectAlignments = 'midbottom',
                 sprite_rect: Optional[pygame.Rect] = None, speed: int = 10,
                 direction: int = 0):
        super().__init__(owner, sprite, spawn_location, spawn_alignment, sprite_rect)

        angle_radians = math.radians(direction)
        self.dx = speed * math.sin(angle_radians)
        self.dy = -speed * math.cos(angle_radians)

    def update(self):
        self._rect.move_ip(self.dx * dt, self.dy * dt)
        super().update()

    def blit(self):
        super().blit()