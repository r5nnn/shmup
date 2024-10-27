from typing import override

import pygame

from data.components.entities import Player
from .state import State
from ..core.prepare import screen_size


class Game(State):
    def __init__(self):
        super().__init__()
        ing = pygame.Surface((20, 20))
        ing.fill(pygame.Color('white'))
        self.thing = Player(
            tuple(round(coord / 2) for coord in screen_size), ing, 250)

    @override
    def update(self):
        self.thing.update()

    @override
    def render(self):
        super().render()
        self.thing.blit()

    @override
    def startup(self):
        super().startup()

    @override
    def cleanup(self):
        super().cleanup()
