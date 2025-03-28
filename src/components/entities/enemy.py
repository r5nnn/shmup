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
        game: Game,
        spawnpoint: tuple[int, int],
        sprite: pygame.Surface | str,
        sprite_scale: int = 1,
        spawn_alignment: RectAlignments = "center",
        sprite_rect: pygame.Rect | None = None,
        rect_offset: tuple[int, int] = (0, 0),
        rect_alignment: RectAlignments = "center",
        stats: EnemyStats | None = None,
    ):
        super().__init__(spawnpoint, sprite, sprite_scale, sprite_rect,
                         rect_offset, rect_alignment, spawn_alignment)
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
