import pygame.sprite

from data.core import Singleton


class CollisionManager(metaclass=Singleton):
    def __init__(self, groups):
        self.groups = groups

    def _check_collisions(self, ):
        ...