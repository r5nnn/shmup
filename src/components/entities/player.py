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
        self.show_hitbox = False
        if self.sprites:
            self.direction_map = {
                None: (self.sprites[0]),
                "up": self.sprites[1],
                "down": self.sprites[2],
                "left": self.sprites[3],
                "right": self.sprites[4],
            }

    def set_direction(self) -> None:
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

        if self.sprites:
            self.set_current_sprites(direction)

    def set_current_sprites(self, direction: str | None) -> None:
        self.sprite = self.direction_map[direction]

    def attack(self) -> None: ...

    @override
    def update(self) -> None:
        for key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            if events.is_key_down(key) and key not in self.keys:
                self.keys.append(key)
            elif events.is_key_up(key) and key in self.keys:
                self.keys.remove(key)

        self.set_direction()
        self.abs_rect.topleft = tuple(map(lambda i, j: i + j, self.abs_rect.topleft, (round(self.dx * system_data.dt),
                                  round(self.dy * system_data.dt))))
        super().update()
        if not system_data.abs_window_rect.contains(self.rect):
            self.rect.clamp_ip(system_data.abs_window_rect)
            setattr(self.abs_rect, self.rect_alignment,
                    self.get_abs_rect_pos(self.rect_alignment))

    @abstractmethod
    def blit(self) -> None:
        pygame.draw.rect(system_data.abs_window, pygame.Color("white"), self.rect)

    @override
    def on_collide(self, sprite: Entity) -> None:
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
            stats={"health": 4, "speed": 40, "spells": 3},
        )
        def make_faded_sprite(sprite_: pygame.Surface) -> pygame.Surface:
            faded_sprite = sprite_.copy()
            faded_sprite.set_alpha(128)
            return faded_sprite
        self.faded_sprites = []
        if self.sprites:
            for sprite in self.sprites:
                self.faded_sprites.append(make_faded_sprite(sprite))
            self.faded_sprite = self.faded_sprites[0]
            self.direction_map = {
                None: (self.sprites[0], self.faded_sprites[0]),
                "up": (self.sprites[1], self.faded_sprites[1]),
                "down": (self.sprites[2], self.faded_sprites[2]),
                "left": (self.sprites[3], self.faded_sprites[3]),
                "right": (self.sprites[4], self.faded_sprites[4]),
            }
        else:
            self.faded_sprite = make_faded_sprite(self.sprite)
        self.show_hitbox = False
        self.fire_rate = 100
        self.last_shot_time = 0
        self.attacking = False
        self.shift_pressed = False

    @override
    def update(self) -> None:
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
            system_data.abs_window.blit(self.faded_sprite, self.abs_rect)
            super().blit()
        else:
            Entity.blit(self)

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

    def set_current_sprites(self, direction: str | None) -> None:
        self.sprite = self.direction_map[direction][0]
        self.faded_sprite = self.direction_map[direction][1]
