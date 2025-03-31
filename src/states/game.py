from typing import override

import pygame

from src.components import entities
from src.components.entities import EntityGroup, Remi
from src.components.managers import statemanager
from src.components.ui import Text, widgethandler
from src.core.load import Load
from src.states.state import State
from src.components.entities.enemy import Enemy
from src.core import system_data


class Game(State):
    def __init__(self):
        super().__init__()
        self.player = Remi(self)
        self.health_txt = Text(system_data.abs_window_rect.topright,
                               text=f"Health: {self.player.health}", align="topright")
        self.enemy = Enemy(self, (500, 500), "topleft",
                           sprite=pygame.image.load(Load("image").path["oscarF"]),
                                                    sprite_scale=2, rect_alignment="center")
        self.enemies = EntityGroup()
        self.enemies.add(self.enemy)
        self.player_bullets = EntityGroup()
        self.enemy_bullets = EntityGroup()
        self.enemy_drops = EntityGroup()
        self.widgets = [self.health_txt]

    @override
    def update(self) -> None:
        self.player.update()
        self.enemies.update()
        self.player_bullets.update()
        self.enemy_bullets.update()
        self.enemy_drops.update()
        entities.update_collisions(self)
        self.health_txt.text = f"Health: {self.player.health}"
        super().update()

    @override
    def render(self) -> None:
        super().render()
        widgethandler.blit()
        self.player.blit()
        self.enemies.blit()
        self.enemy_bullets.blit()
        self.player_bullets.blit()
        self.enemy_drops.blit()

    @override
    def startup(self) -> None:
        super().startup()

    @override
    def cleanup(self) -> None:
        super().cleanup()

    def game_over(self) -> None:
        statemanager.pop()
