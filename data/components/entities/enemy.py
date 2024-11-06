"""Contains base class for all the game's enemies."""
import logging
from typing import Optional, TypedDict, override

import pygame

from data.components import RectAlignments
from data.components.entities.entity import Entity
from data.core import screen

EnemyStats = TypedDict('EnemyStats', {'health': int})


class Enemy(Entity):
    """Base class for all the game's enemies."""
    def __init__(self, spawn: tuple[int, int], sprite: pygame.Surface,
                 spawn_alignment: RectAlignments = 'center',
                 hitbox: Optional[pygame.Rect] = None,
                 hitbox_offset: tuple[int, int] = (0, 0),
                 stats: Optional[EnemyStats] = None):
        self.hitbox_offset_x, self.hitbox_offset_y = hitbox_offset
        super().__init__(spawn, sprite, hitbox, spawn_alignment)
        self.health = stats.get('health', 1)
        self.x, self.y = float(spawn[0]), float(spawn[1])

    @override
    def _spawn(self):
        spawn = (self.spawn[0] + self.hitbox_offset_x,
                 self.spawn[1] + self.hitbox_offset_y)
        setattr(self.rect, self.spawn_alignment, spawn)
        logging.info(f'{repr(self)} moved to spawnpoint: '
                     f'{getattr(self.rect, self.spawn_alignment)}')

    @override
    def update(self) -> None:
        ...

    @override
    def blit(self) -> None:
        screen.blit(self.sprite, self.rect)

    @override
    def on_collide(self, sprite) -> None:
        self.kill()
        logging.info(f'{repr(self)} collided with {sprite} and killed.')
