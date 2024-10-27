from abc import ABC
from typing import override

import pygame.display
from pygame.sprite import Sprite


class Entity(ABC, Sprite):
    def __init__(self, spawn: tuple[int, int], sprite: pygame.Surface):
        Sprite.__init__(self)
        self.rect = sprite.get_rect()
        self.sprite = sprite
        self.spawn = spawn

    @override
    def update(self):
        ...

    def blit(self):
        ...