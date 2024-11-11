from typing import override

from data.components import entities
from data.components.entities import EntityGroup, Remi
from .state import State


class Game(State):
    def __init__(self):
        super().__init__()
        self.player = Remi(self)
        self.enemies = EntityGroup()
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
