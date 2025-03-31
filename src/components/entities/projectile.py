from __future__ import annotations

import math
from typing import TYPE_CHECKING
from typing import override

import pygame

from src.components.entities.entity import Entity
from src.core.data import system_data

if TYPE_CHECKING:
    from src.core.types import RectAlignments


class Projectile(Entity):
    def __init__(
        self,
        owner: Entity,
        sprite: pygame.Surface | str | None = None,
        sprite_scale: int = 1,
        spawn_location: RectAlignments | tuple[int, int] = "midtop",
        spawn_alignment: RectAlignments = "midbottom",
        sprite_rect: pygame.Rect | None = None,
    ):
        self.type = f"{owner}bullet"
        if not (sprite or sprite_rect):
            msg = "Must provide either sprite or sprite_rect, not neither."
            raise ValueError(msg)

        if sprite is None:
            current_sprite = pygame.Surface(sprite_rect.size)
            current_sprite.fill(pygame.Color("white"))
        else:
            current_sprite = sprite

        if isinstance(spawn_location, tuple):
            x_offset, y_offset = spawn_location
            spawn_x, spawn_y = getattr(owner.abs_rect, spawn_alignment)
            calculated_spawn = (spawn_x + x_offset, spawn_y + y_offset)
        else:
            calculated_spawn = getattr(owner.abs_rect, spawn_location)

        super().__init__(
            calculated_spawn,
            sprite=current_sprite, sprite_scale=sprite_scale,
            sprite_rect=(
                sprite.get_rect() if sprite_rect is None else sprite_rect
            ),
            spawn_alignment=spawn_alignment,
        )

    @override
    def update(self) -> None:
        super().update()
        if not system_data.abs_window_rect.contains(self.rect):
            self.kill()


class SimpleBullet(Projectile):
    def __init__(
        self,
        owner: Entity,
        sprite: pygame.Surface | str = None,
        sprite_scale: int = 1,
        spawn_location: RectAlignments | tuple[int, int] = "midtop",
        spawn_alignment: RectAlignments = "midbottom",
        sprite_rect: pygame.Rect | None = None,
        speed: int = 100,
        direction: int = 0,
    ):
        super().__init__(
            owner, sprite, sprite_scale, spawn_location, spawn_alignment, sprite_rect
        )
        angle_radians = math.radians(direction)
        self.dx = speed * math.sin(angle_radians)
        self.dy = -speed * math.cos(angle_radians)
        print(self.dx)

    @override
    def update(self) -> None:
        dtx = self.dx * system_data.dt
        dty = self.dy * system_data.dt
        print(math.ceil(dtx) if dtx >= 0 else math.floor(dtx),
            math.ceil(dty) if dty >= 0 else math.floor(dty))
        self.abs_rect.move_ip(
            math.ceil(dtx) if dtx >= 0 else math.floor(dtx),
            math.ceil(dty) if dty >= 0 else math.floor(dty)
        )
        super().update()

    @override
    def blit(self) -> None:
        super().blit()
