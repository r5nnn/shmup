from abc import ABC, abstractmethod
from typing import override

import pygame.display
from pygame.sprite import Sprite


class Entity(ABC, Sprite):
    def __init__(self, spawn: tuple[int, int], sprite: pygame.Surface):
        Sprite.__init__(self)
        self.rect = sprite.get_rect()
        self.sprite = sprite
        self.spawn = spawn

    @abstractmethod
    @override
    def update(self):
        ...

    @abstractmethod
    def blit(self):
        ...