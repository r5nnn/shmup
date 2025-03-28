"""Contains the base class for all the game's players."""

from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TypedDict, override, TYPE_CHECKING

import pygame

from src.components import events
from src.components.entities.entityutils import Entity
from src.components.entities.projectile import SimpleBullet
from src.core.data import system_data

if TYPE_CHECKING:
    from src.core.types import RectAlignments
    from src.states.game import Game


class PlayerStats(TypedDict):
    health: int
    speed: int
    spells: int


class Player(Entity, ABC):
    """Base class for all the game's players."""

    def __init__(
        self,
        game: Game,
        spawnpoint: tuple[int, int],
        sprite: pygame.Surface | str,
        spawn_alignment: RectAlignments = "center",
        sprite_scale: int = 1,
        sprite_rect: pygame.Rect | None = None,
        rect_offset: tuple[int, int] = (0, 0),
        rect_alignment: RectAlignments = "center",
        stats: PlayerStats | None = None,
    ):
        self.game = game
        stats = {} if stats is None else stats
        self.health = stats.get("health", 1)
        self.speed = stats.get("speed", 2)
        super().__init__(
            spawnpoint,
            sprite,
            sprite_scale,
            sprite_rect,
            rect_offset,
            rect_alignment,
            spawn_alignment,
        )

        self.keys = []
        self.dx, self.dy = 0.0, 0.0
        self.x, self.y = spawnpoint

    @override
    def move_to_spawn(self):
        super().move_to_spawn()

    def _set_direction(self):
        self.dx, self.dy = 0.0, 0.0
        direction = None
        self.show_hitbox = False

        for key in self.keys:
            match key:
                case pygame.K_UP:
                    self.dy = -self.speed
                    direction = "up"
                case pygame.K_DOWN:
                    self.dy = self.speed
                    direction = "down"
                case pygame.K_LEFT:
                    self.dx = -self.speed
                    direction = "left"
                case pygame.K_RIGHT:
                    self.dx = self.speed
                    direction = "right"

        if events.is_key_pressed(pygame.K_LSHIFT):
            self.dx /= 2
            self.dy /= 2
            self.show_hitbox = True

        if direction:
            self._set_direction_sprite(direction)
        elif self.sprites:
            self.sprite = self.sprites[0]

    def _set_direction_sprite(self, direction: str):
        if self.sprites:
            direction_map = {
                "default": self.sprites[0],
                "up": self.sprites[1],
                "down": self.sprites[2],
                "left": self.sprites[3],
                "right": self.sprites[4],
            }
            self.sprite = direction_map.get(direction, self.sprite)

    def attack(self): ...

    @override
    def update(self):
        for key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            if events.is_key_down(key) and key not in self.keys:
                self.keys.append(key)
            elif events.is_key_up(key) and key in self.keys:
                self.keys.remove(key)

        self._set_direction()
        self.x += round(self.dx * system_data.dt)
        self.y += round(self.dy * system_data.dt)

        self.rect.topleft = (self.x, self.y)
        if not system_data.abs_window_rect.contains(self.rect):
            self.rect.clamp_ip(system_data.abs_window_rect)
            self.x, self.y = getattr(self.rect, self.rect_alignment)

    @abstractmethod
    def blit(self): ...

    @override
    def on_collide(self, sprite):
        self.health -= 1
        self.move_to_spawn()


class Remi(Player):
    def __init__(self, game: Game):
        super().__init__(
            game,
            spawnpoint=system_data.screen_rect.center,
            sprite="remi",
            sprite_scale=2,
            sprite_rect=pygame.Rect(0, 100, 20, 20),
            rect_offset=(1, -7),
            rect_alignment="center",
            stats={"health": 4, "speed": 40, "spells": 3},
        )
        self.faded_sprite = self.sprite.copy()
        self.faded_sprite.set_alpha(128)
        self.show_hitbox = False
        self.fire_rate = 100
        self.last_shot_time = 0
        self.attacking = False
        self.shift_pressed = False

    @override
    def update(self):
        # Handle base player movement and direction logic
        super().update()
        self.attacking = False
        if events.is_key_pressed(pygame.K_z):
            # Set attacking state and check fire rate cooldown
            self.attacking = True
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.fire_rate:
                self.attack()
                self.last_shot_time = current_time

    @override
    def blit(self) -> None:
        if self.show_hitbox:
            system_data.abs_window.blit(self.faded_sprite, (self.x, self.y))
            pygame.draw.rect(system_data.abs_window, pygame.Color("white"), self.rect)
        else:
            system_data.abs_window.blit(self.sprite, self.x, self.y)

    @override
    def attack(self) -> None:
        """Fires a bullet and triggers an animation frame update."""
        bullet = SimpleBullet(
            owner=self,
            sprite_rect=pygame.Rect(0, 0, 4, 4),
            spawn_location=(0, 0),
            spawn_alignment="midtop",
        )
        self.game.player_bullets.add(bullet)
