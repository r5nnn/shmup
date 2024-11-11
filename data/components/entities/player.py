"""Contains the base class for all the game's players."""
import logging
from typing import Optional, TypedDict, override, TYPE_CHECKING

import pygame

from data.core.prepare import screen_center, sprites
from data.core.utils import Singleton, dt
from data.components import RectAlignments
from data.components.entities.entity import Entity
from data.components.entities.projectile import SimpleBullet
import data.components.input as InputManager
from data.core import screen, screen_rect

if TYPE_CHECKING:
    from data.states.game import Game

PlayerStats = TypedDict("PlayerStats", {"health": int, "speed": int, "spells": int,
                                        "atk delay": int})


class Player(Entity):
    """Base class for all the game's players."""
    def __init__(self, game :"Game",
                 spawn: tuple[int, int],
                 spawn_alignment: RectAlignments = "center",
                 sprite: Optional[pygame.Surface] = None,
                 spritesheet: Optional[list[pygame.Surface]] = None,
                 sprite_rect: Optional[pygame.Rect] = None,
                 rect_offset: tuple[int, int] = (0, 0),
                 stats: Optional[PlayerStats] = None):
        if (sprite is None) == (spritesheet is None):  # if both None or both provided
            msg = "Provide either a single sprite or a spritesheet, not both."
            raise ValueError(msg)
        self.game = game
        self.rect_offset_x, self.rect_offset_y = rect_offset
        self.spritesheet = spritesheet
        stats = {} if stats is None else stats
        self.health = stats.get("health", 1)
        self.speed = stats.get("speed", 2)
        super().__init__(
            (spawn[0] + rect_offset[0], spawn[1] + rect_offset[1]),
            sprite or spritesheet[0], sprite_rect, spawn_alignment)

        self.keys = []
        self.show_hitbox = False
        self.dx, self.dy = 0.0, 0.0
        self.x, self.y = float(spawn[0]), float(spawn[1])
        self._abs_rect.center = round(self.x), round(self.y)

        self.fire_rate = 100
        self.last_shot_time = 0  # Tracks the last time a bullet was shot
        logging.info("Created %r.", self)

    @override
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

        if direction:
            self._set_direction_sprite(direction)
        elif self.spritesheet:
            self.sprite = self.spritesheet[0]

        if InputManager.is_key_pressed(pygame.K_LSHIFT):
            self.dx /= 2
            self.dy /= 2
            self.show_hitbox = True

        logging.debug("Direction of player set as x: %f, y: %f.", self.dx, self.dy)

    def _set_direction_sprite(self, direction: str):
        if self.spritesheet:
            direction_map = {
                "default": self.spritesheet[0],
                "up": self.spritesheet[1],
                "down": self.spritesheet[2],
                "left": self.spritesheet[3],
                "right": self.spritesheet[4],
            }
            self.sprite = direction_map.get(direction, self.spritesheet[0])

    def attack(self):
        ...

    @override
    def update(self):
        for key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            if InputManager.is_key_down(key) and key not in self.keys:
                self.keys.append(key)
            elif InputManager.is_key_up(key) and key in self.keys:
                self.keys.remove(key)

        self._set_direction()
        self.x += self.dx * dt
        self.y += self.dy * dt

        self.rect.center = (round(self.x) + self.rect_offset_x,
                            round(self.y) + self.rect_offset_y)
        if not screen_rect.contains(self.rect):
            self.rect.clamp_ip(screen_rect)
            self.x = float(self.rect.centerx - self.rect_offset_x)
            self.y = float(self.rect.centery - self.rect_offset_y)

        self._abs_rect.center = (round(self.x), round(self.y))

        if InputManager.is_key_pressed(pygame.K_z):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.fire_rate:
                self.attack()
                self.last_shot_time = current_time

    @override
    def blit(self):
        sprite_position = (round(self.x) - self.sprite.get_width() // 2,
                           round(self.y) - self.sprite.get_height() // 2)

        if self.show_hitbox:
            faded_sprite = self.sprite.copy()
            faded_sprite.set_alpha(128)
            screen.blit(faded_sprite, sprite_position)
            pygame.draw.rect(screen, pygame.Color("white"), self.rect)
        else:
            screen.blit(self.sprite, sprite_position)

    @override
    def on_collide(self, sprite):
        self.health -= 1
        logging.info("%r collided with %r", self, sprite)
        self.move_to_spawn()

    def __repr__(self):
        parent_repr = super().__repr__()
        return (f"{parent_repr}, Player(spritesheet={self.spritesheet!r}, "
                f"rect_offset=({self.rect_offset_x!r}, {self.rect_offset_y!r}),"
                f" stats={{'health': {self.health!r},'speed': {self.speed!r}}})")


class Remi(Player, metaclass=Singleton):
    def __init__(self, game: "Game"):
        super().__init__(game, spawn=screen_center,
                         spritesheet=[pygame.transform.scale_by(image, 2)
                                      for image in sprites("remi")],
                         sprite_rect=pygame.Rect(0, 0, 20, 20), rect_offset=(1, -7),
                         stats={"Health": 4, "speed": 2, "spells": 3, "atk delay": 100})

    @override
    def attack(self):
        bullet = SimpleBullet(owner=self, sprite_rect=pygame.Rect(0, 0, 4, 4))
        self.game.player_bullets.add(bullet)
