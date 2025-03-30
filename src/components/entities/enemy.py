"""Contains base class for all the game's enemies."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import TypedDict, override

from src.components.entities.entityutils import Entity
from src.components.entities.projectile import Projectile

if TYPE_CHECKING:
    from src.states import Game
    import pygame
    from src.core.types import RectAlignments


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
            self.kill()
