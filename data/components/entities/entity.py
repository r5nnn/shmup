from abc import ABC, abstractmethod
from typing import override

import pygame.display
from pygame.sprite import Sprite

from data.components import RectAlignments


class Entity(ABC, Sprite):
    def __init__(self, spawn: tuple[int, int], sprite: pygame.Surface,
                 spawn_alignments: RectAlignments = 'center'):
        Sprite.__init__(self)
        self.spawn = spawn
        self.rect = sprite.get_rect()
        setattr(self.rect, spawn_alignments, spawn)
        self.sprite = sprite

    @abstractmethod
    @override
    def update(self):
        ...

    @abstractmethod
    def blit(self):
        ...

    @abstractmethod
    def on_collide(self, sprite):
        ...


class EntityGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def blit(self):
        for sprite in self.sprites():
            sprite.blit()