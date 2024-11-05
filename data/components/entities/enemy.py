from typing import Optional, TypedDict, override

import pygame

from data.components.entities.entity import Entity
from data.core import screen

EnemyStats = TypedDict('EnemyStats', {'health': int})


class Enemy(Entity):
    def __init__(self, spawn: tuple[int, int],
                 sprite: pygame.Surface,
                 hitbox: Optional[pygame.Rect] = None,
                 hitbox_offset: tuple[int, int] = (0, 0),
                 stats: Optional[EnemyStats] = None):
        super().__init__(spawn, sprite, hitbox)
        self.hitbox_offset_x, self.hitbox_offset_y = hitbox_offset
        self.health = stats.get('health', 1)
        self.x, self.y = float(spawn[0]), float(spawn[1])
        self._spawn()

    def _spawn(self):
        self.rect.center = (self.spawn[0] + self.hitbox_offset_x,
                            self.spawn[1] + self.hitbox_offset_y)

    @override
    def update(self):
        ...

    @override
    def blit(self):
        screen.blit(self.sprite, self.rect)

    @override
    def on_collide(self, sprite):
        self.kill()
