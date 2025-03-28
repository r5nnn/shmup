from typing import override

import pygame

from src.components import entities
from src.components.entities import EntityGroup, Remi
from src.core.load import Load
from src.states.state import State
from src.components.entities.enemy import Enemy
from src.core import system_data


class Game(State):
    def __init__(self):
        super().__init__()
        self.player = Remi(self)
        self.enemy = Enemy(self,
                           system_data.abs_window_rect.topleft,
                           pygame.transform.scale_by(pygame.image.load(Load("image").path["oscarF"]), 2), 2, "topleft")
        self.enemies = EntityGroup()
        self.enemies.add(self.enemy)
        self.player_bullets = EntityGroup()
        self.enemy_bullets = EntityGroup()

    @override
    def update(self):
        self.player.update()
        self.enemies.update()
        self.player_bullets.update()
        self.enemy_bullets.update()
        entities.update_collisions(self)

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
