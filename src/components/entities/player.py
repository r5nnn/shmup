"""Contains the base class for all the game's players."""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import override, TYPE_CHECKING

import pygame

from src.components import events
from src.components.entities.entity import Entity
from src.components.entities.projectile import SimpleBullet, SimpleBulletPattern, SimpleBulletConfig
from src.core.data import system_data

if TYPE_CHECKING:
    from src.core.types import RectAlignments
    from src.states.game import Game


@dataclass
class PlayerStats:
    health: int = 1
    speed: int = 30
    spells: int = 3
    fire_rate: int = 100


class Player(Entity, ABC):
    """Base class for all the game's players."""

    direction_map: dict[None | str, list[pygame.Surface]]
    level: int
    def __init__(
        self,
        game: Game,
        spawnpoint: tuple[int, int],
        spawn_alignment: RectAlignments = "center",
        stats: PlayerStats | None = None,
        **kwargs
    ):
        super().__init__(
            spawnpoint,
            spawn_alignment,
            **kwargs
        )
        self.game = game
        if stats is None:
            stats = PlayerStats()
        self.health = stats.health
        self.speed = stats.speed
        self.spells = stats.spells
        self.fire_rate = stats.fire_rate
        self.level = 0
        self.type = "player"
        self.keys = []
        self.dx, self.dy = 0.0, 0.0

        if self.sprites:
            self.direction_map = {
                None: [self.sprites[0]],
                "up": [self.sprites[1]],
                "down": [self.sprites[2]],
                "left": [self.sprites[3]],
                "right": [self.sprites[4]],
            }

    def set_direction(self) -> None:
        self.dx, self.dy = 0.0, 0.0
        direction = None

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

        if self.sprites:
            self.set_sprite(direction)

    def set_sprite(self, direction: str | None) -> None:
        self.sprite = self.direction_map[direction][0]

    def attack(self) -> None: ...

    @override
    def update(self) -> None:
        for key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            if events.is_key_down(key) and key not in self.keys:
                self.keys.append(key)
            elif events.is_key_up(key) and key in self.keys:
                self.keys.remove(key)

        self.set_direction()
        self.abs_rect.move_ip(
            round(self.dx * system_data.dt), round(self.dy * system_data.dt)
        )
        super().update()
        if not system_data.abs_window_rect.contains(self.rect):
            self.rect.clamp_ip(system_data.abs_window_rect)
            setattr(
                self.abs_rect,
                self.rect_alignment,
                self.get_abs_rect_pos(self.rect_alignment),
            )

    @override
    def blit(self) -> None:
        pygame.draw.rect(
            system_data.abs_window, pygame.Color("white"), self.rect
        )

    @override
    def on_collide(self, sprite: Entity) -> None:
        if sprite.type in ("enemy", "enemybullet"):
            self.health -= 1
            self.move_to_spawn()
        elif sprite.type == "item":
            self.level += 1


class FocusPlayer(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_hitbox = False

        def make_faded_sprite(sprite_: pygame.Surface) -> pygame.Surface:
            faded_sprite = sprite_.copy()
            faded_sprite.set_alpha(128)
            return faded_sprite

        self.faded_sprites = []
        if self.sprites:
            for i, sprite_key in enumerate(zip(self.sprites, self.direction_map.keys())):
                self.faded_sprites.append(make_faded_sprite(sprite_key[0]))
                self.direction_map[sprite_key[1]].append(self.faded_sprites[i])
            self.faded_sprite = self.faded_sprites[0]
        else:
            self.faded_sprite = make_faded_sprite(self.sprite)

    @override
    def blit(self) -> None:
        if self.show_hitbox:
            system_data.abs_window.blit(self.faded_sprite, self.abs_rect)
            super().blit()
        else:
            Entity.blit(self)

    @override
    def set_direction(self) -> None:
        self.show_hitbox = False
        super().set_direction()
        if events.is_key_pressed(pygame.K_LSHIFT):
            self.dx /= 2
            self.dy /= 2
            self.show_hitbox = True

    @override
    def set_sprite(self, direction: str | None) -> None:
        super().set_sprite(direction)
        self.faded_sprite = self.direction_map[direction][1]


class Remi(FocusPlayer):
    bullet_patterns = (
        ((1, 0),),
        ((1, 5), (1, -5)),
    )

    def __init__(self, game: Game):
        super().__init__(
            game,
            spawnpoint=system_data.abs_window_rect.center,
            sprite="remi",
            sprite_scale=2,
            sprite_rect=pygame.Rect(0, 100, 20, 20),
            rect_offset=(1, -7),
            stats=PlayerStats(health=4, speed=40),
        )
        self.last_shot_time = 0

    @override
    def update(self) -> None:
        # Handle base player movement and direction logic
        super().update()
        if events.is_key_pressed(pygame.K_z):
            # Set attacking state and check fire rate cooldown
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.fire_rate:
                self.attack()
                self.last_shot_time = current_time

    @override
    def attack(self) -> None:
        """Fires a bullet and triggers an animation frame update."""
        config = SimpleBulletConfig(
            sprite_rect=pygame.Rect(0, 0, 4, 4),
            spawn_location=[0, 0],
            spawn_alignment="midtop")
        bullets = SimpleBulletPattern(self, config, "up", self.level+1)
        self.game.player_bullets.add(*bullets.bullets)

    @override
    def on_collide(self, sprite: Entity) -> None:
        super().on_collide(sprite)
        if self.health <= 0:
            self.game.game_over()
