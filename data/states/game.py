from typing import override

import pygame

from data.components import entities
from data.components.entities import Player, EntityGroup
from data.core.prepare import screen_size
from .state import State
from ..core import sprites


class Game(State):
    def __init__(self):
        super().__init__()
        # noinspection PyTypeChecker
        self.player = Player(tuple(round(coord / 2) for coord in screen_size),
                             spritesheet=[pygame.transform.scale_by(image, 2) \
                                          for image in sprites('remi')],
                             hitbox=pygame.Rect(0, 0, 20, 20), hitbox_offset=(1, -7))
        self.enemies = EntityGroup()
        self.player_bullets = EntityGroup()
        self.enemy_bullets = EntityGroup()

    @override
    def update(self):
        self.player.update()
        self.enemies.update()
        self.player_bullets.update()
        self.enemy_bullets.update()
        entities.update(self)

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
