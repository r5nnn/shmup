from collections import deque
from typing import override, TypedDict

import pygame

from .entity import Entity
from .. import InputManager
from data.core import screen, screen_rect
import data.core.utils

PlayerStats = TypedDict('PlayerStats',
                        {'health': int, 'speed': int, 'spells': int})


class Player(Entity):
    def __init__(self, spawn: tuple[int, int],
                 sprite: pygame.Surface | dict[str, pygame.Surface],
                 stats: PlayerStats = None):
        super().__init__(spawn, sprite if isinstance(sprite, pygame.Surface) \
            else next(iter(sprite.values())))
        self.keys = deque()
        self.dx, self.dy = 0.0, 0.0
        stats = {} if stats is None else stats
        self.health = stats.get('health', 1)
        self.speed = stats.get('speed', 250)
        self.spells = stats.get('spells', 3)
        self.x, self.y = float(self.rect.x), float(self.rect.y)
        self.rect.move_ip(self.spawn)

    def _set_direction(self):
        self.dx, self.dy = 0.0, 0.0

        for key in self.keys:
            match key:
                case pygame.K_UP:
                    self.dy = -self.speed
                case pygame.K_DOWN:
                    self.dy = self.speed
                case pygame.K_LEFT:
                    self.dx = -self.speed
                case pygame.K_RIGHT:
                    self.dx = self.speed
        if InputManager.is_key_pressed(pygame.K_LSHIFT):
            self.dx /= 2
            self.dy /= 2

    @override
    def update(self):
        self.sprite.fill(pygame.Color('white'))
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
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        if not screen_rect.contains(self.rect):
            self.rect.clamp_ip(screen_rect)
            self.x = self.rect.x
            self.y = self.rect.y

    @override
    def blit(self):
        screen.blit(self.sprite, self.rect)

    @override
    def on_collide(self, sprite):
        ...