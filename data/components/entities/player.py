from collections import deque
from typing import override

import pygame

from .entity import Entity
from .. import inputmanager
from data.core import screen, screen_rect
import data.core.utils


class Player(Entity):
    def __init__(self, spawn: tuple[int, int],
                 sprite: pygame.Surface | dict[str, pygame.Surface],
                 speed: int):
        super().__init__(spawn,
                         sprite if isinstance(sprite, pygame.Surface) else \
                             next(iter(sprite.values())))
        self.keys = deque()
        self.dx, self.dy = 0.0, 0.0
        self.speed = speed
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

    @override
    def update(self):
        # Update keys based on input manager
        for key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            if inputmanager.is_key_down(key):
                if key not in self.keys:
                    self.keys.append(key)
            elif inputmanager.is_key_up(key):
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
