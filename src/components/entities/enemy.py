"""Contains base class for all the game's enemies."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import TypedDict, override

import pygame

from src.components.entities.entity import Entity
from src.components.entities.item import FallingItem
from src.components.entities.projectile import Projectile
from src.core.load import Load

if TYPE_CHECKING:
    from src.states import Game


class EnemyStats(TypedDict):
    health: int


class Enemy(Entity):
    """Base class for all the game's enemies."""

    def __init__(
        self,
        game: Game, *args, stats: EnemyStats | None = None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.type = "enemy"
        self.game = game
        stats = {} if stats is None else stats
        self.health = stats.get("health", 1)

    @override
    def update(self) -> None: ...

    @override
    def blit(self) -> None:
        super().blit()

    @override
    def on_collide(self, sprite: Entity) -> None:
        if isinstance(sprite, Projectile):
            self.drop_item()
            self.kill()

    def drop_item(self) -> None:
        self.game.enemy_drops.add(FallingItem(
            50, self.abs_rect.center,
            sprite=pygame.image.load(Load("image").path["level"]).convert(),
            sprite_scale=2))
