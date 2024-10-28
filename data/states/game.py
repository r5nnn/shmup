from typing import override

import pygame

from data.components.entities import Player, EntityGroup
from .state import State
from data.core.prepare import screen_size
from data.components.entities import CollisionManager


class Game(State):
    def __init__(self):
        super().__init__()
        self.collision_manager = CollisionManager(self)
        ing = pygame.Surface((100, 100))
        ing.fill(pygame.Color('white'))
        # noinspection PyTypeChecker
        self.player = Player(
            tuple(round(coord / 2) for coord in screen_size), ing)
        self.enemies = EntityGroup()
        self.player_bullets = EntityGroup()
        self.enemy_bullets = EntityGroup()

    @override
    def update(self):
        self.player.update()
        self.enemies.update()
        self.player_bullets.update()
        self.enemy_bullets.update()
        self.collision_manager.update()

    @override
    def render(self):
        super().render()
        self.player.blit()
        self.enemies.blit()
        self.enemy_bullets.blit()
        self.player_bullets.blit()

    @override
    def startup(self):
        super().startup()

    @override
    def cleanup(self):
        super().cleanup()
