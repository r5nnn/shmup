import logging
from typing import Optional, TypedDict, override

import pygame

import data.core.utils
from data.components.entities.entity import Entity
from data.components.input import InputManager
from data.core import screen, screen_rect

PlayerStats = TypedDict('PlayerStats', {'health': int, 'speed': int, 'spells': int})


class Player(Entity):
    def __init__(self, spawn: tuple[int, int],
                 sprite: Optional[pygame.Surface] = None,
                 spritesheet: Optional[list[pygame.Surface]] = None,
                 hitbox: Optional[pygame.Rect] = None,
                 hitbox_offset: tuple[int, int] = (0, 0),
                 stats: Optional[PlayerStats] = None):
        if (sprite is None) == (spritesheet is None):  # if both None or both provided
            raise ValueError("Provide either a single sprite or a spritesheet,"
                             " not both.")
        initial_sprite = sprite or spritesheet[0]
        super().__init__(spawn, initial_sprite, hitbox)

        self.hitbox_offset_x, self.hitbox_offset_y = hitbox_offset
        self.spritesheet = spritesheet
        self.keys = []
        self.show_hitbox = False
        self.dx, self.dy = 0.0, 0.0
        stats = {} if stats is None else stats
        self.health = stats.get('health', 1)
        self.speed = stats.get('speed', 250)
        self.spells = stats.get('spells', 3)

        self.x, self.y = float(spawn[0]), float(spawn[1])
        self._spawn()
        logging.info(f'Created {repr(self)}.')

    def _spawn(self):
        self.rect.center = (self.spawn[0] + self.hitbox_offset_x,
                            self.spawn[1] + self.hitbox_offset_y)

    def _set_direction(self):
        self.dx, self.dy = 0.0, 0.0
        direction = None
        self.show_hitbox = False

        for key in self.keys:
            match key:
                case pygame.K_UP:
                    self.dy = -self.speed
                    direction = 'up'
                case pygame.K_DOWN:
                    self.dy = self.speed
                    direction = 'down'
                case pygame.K_LEFT:
                    self.dx = -self.speed
                    direction = 'left'
                case pygame.K_RIGHT:
                    self.dx = self.speed
                    direction = 'right'

        if direction:
            self._set_direction_sprite(direction)
        elif self.spritesheet:
            self.sprite = self.spritesheet[0]

        if InputManager.is_key_pressed(pygame.K_LSHIFT):
            self.dx /= 2
            self.dy /= 2
            self.show_hitbox = True

        logging.debug(f'Direction of player set as x: {self.dx}, y: {self.dy}.')

    def _set_direction_sprite(self, direction: str):
        if self.spritesheet:
            direction_map = {'default': self.spritesheet[0], 'up': self.spritesheet[1], 'down': self.spritesheet[2],
                             'left': self.spritesheet[3], 'right': self.spritesheet[4]}
            self.sprite = direction_map.get(direction, self.spritesheet[0])

    @override
    def update(self):
        for key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            if InputManager.is_key_down(key):
                if key not in self.keys:
                    self.keys.append(key)
            elif InputManager.is_key_up(key):
                if key in self.keys:
                    self.keys.remove(key)

        self._set_direction()
        dt = data.core.utils.dt
        self.x += self.dx * dt
        self.y += self.dy * dt

        self.rect.center = (round(self.x) + self.hitbox_offset_x,
                            round(self.y) + self.hitbox_offset_y)
        if not screen_rect.contains(self.rect):
            self.rect.clamp_ip(screen_rect)

            self.x = float(self.rect.centerx - self.hitbox_offset_x)
            self.y = float(self.rect.centery - self.hitbox_offset_y)

    @override
    def blit(self):
        sprite_position = (round(self.x) - self.sprite.get_width() // 2,
                           round(self.y) - self.sprite.get_height() // 2)

        if self.show_hitbox:
            faded_sprite = self.sprite.copy()
            faded_sprite.set_alpha(128)
            screen.blit(faded_sprite, sprite_position)
            pygame.draw.rect(screen, pygame.Color('white'), self.rect)
        else:
            screen.blit(self.sprite, sprite_position)

    @override
    def on_collide(self, sprite):
        self.health -= 1
        self._spawn()
