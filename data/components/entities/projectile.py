import math
from typing import Optional, override, Union

import pygame

from data.components import RectAlignments
from data.components.entities.entityutils import Entity
from data.core import screen_rect
import data.core.utils


class Projectile(Entity):
    def __init__(self, owner: Entity, sprite: Optional[pygame.Surface] = None,
                 spawn_location: Union[RectAlignments, tuple[int, int]] = "midtop",
                 spawn_alignment: RectAlignments = "midbottom",
                 sprite_rect: Optional[pygame.Rect] = None):

        if not (sprite or sprite_rect):
            raise ValueError("Must provide either sprite or sprite_rect, not neither.")

        if sprite is None:
            current_sprite = pygame.Surface(sprite_rect.size)
            current_sprite.fill(pygame.Color("white"))
        else:
            current_sprite = sprite

        # Determine spawn position based on type of spawn_location
        if isinstance(spawn_location, tuple):
            # Use (x, y) coordinates relative to owner's alignment position
            x_offset, y_offset = spawn_location
            spawn_x, spawn_y = getattr(owner.abs_rect, spawn_alignment)
            calculated_spawn = (spawn_x + x_offset, spawn_y + y_offset)
        else:
            # Assume spawn_location is a RectAlignment string; align directly
            calculated_spawn = getattr(owner.abs_rect, spawn_location)

        print(current_sprite)
        # Initialize Entity with calculated spawn position
        super().__init__(calculated_spawn, sprite=current_sprite,
                         sprite_rect=sprite.get_rect() if sprite_rect is None else sprite_rect,
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
                 spawn_location: Union[RectAlignments, tuple[int, int]] = "midtop",
                 spawn_alignment: RectAlignments = "midbottom",
                 sprite_rect: Optional[pygame.Rect] = None, speed: int = 1000,
                 direction: int = 0):
        super().__init__(owner, sprite, spawn_location, spawn_alignment,
                         sprite_rect)

        # Calculate dx and dy based on direction and speed
        angle_radians = math.radians(direction)
        self.dx = speed * math.sin(angle_radians)
        self.dy = -speed * math.cos(angle_radians)

    def update(self):
        # Move bullet based on direction and delta time
        self._rect.move_ip(self.dx * data.core.utils.dt, self.dy * data.core.utils.dt)
        super().update()

    def blit(self):
        super().blit()
