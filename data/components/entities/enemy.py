"""Contains base class for all the game's enemies."""
import logging
from typing import Optional, TypedDict, override

import pygame

from data.components import RectAlignments
from data.components.entities.entity import Entity
from data.core import screen

class EnemyStats(TypedDict):
    health: int


class Enemy(Entity):
    """Base class for all the game's enemies."""
    def __init__(self, spawn: tuple[int, int], sprite: pygame.Surface,
                 spawn_alignment: RectAlignments = "center",
                 sprite_rect: Optional[pygame.Rect] = None,
                 rect_offset: tuple[int, int] = (0, 0),
                 stats: Optional[EnemyStats] = None):
        self.rect_offset_x, self.rect_offset_y = rect_offset
        super().__init__(
            (spawn[0] + rect_offset[0], spawn[1] + rect_offset[1]),
            sprite, sprite_rect, spawn_alignment)
        self.health = stats.get("health", 1)
        self.x, self.y = float(spawn[0]), float(spawn[1])
        logging.info("Spawned %r.", self)

    @property
    def spawn(self):
        return (self._spawn[0] - self.rect_offset_x,
                self._spawn[1] - self.rect_offset_y)

    @spawn.setter
    def spawn(self, value):
        self._spawn = (value[0] + self.rect_offset_x,
                       value[1] + self.rect_offset_y)

    @override
    def move_to_spawn(self):
        super().move_to_spawn()
        logging.info("%r moved to spawnpoint: %d", self,
                     getattr(self.rect, self.spawn_alignment))

    @override
    def update(self) -> None:
        ...

    @override
    def blit(self) -> None:
        screen.blit(self.sprite, self.rect)

    @override
    def on_collide(self, sprite) -> None:
        self.kill()
        logging.info("%r collided with %r and killed.", self, sprite)

    @override
    def __repr__(self):
        parent_repr = super().__repr__()
        return (f"{parent_repr}, Enemy("
                f"rect_offset={(self.rect_offset_x, self.rect_offset_y)!r}, "
                f"stats={{'health': {self.health!r}}})")
