import os
from typing import TYPE_CHECKING

import pygame.sprite

from .constants import rect_attributes
from .spritesheet import Spritesheet

# avoids relative import error while making pycharm happy (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ...game import Game
    from ..stage1 import Stage1


class Entity(pygame.sprite.Sprite):
    def __init__(self, game: 'Game', img_dir: str = None):
        super().__init__()
        self.game = game
        self.img_dir = img_dir if img_dir is not None else os.path.join(self.game.textures_dir, 'null')
        self.spritesheet = Spritesheet(self.img_dir)

    def update(self) -> None:
        ...

    def collided(self, collider):
        ...


class Enemy(Entity):
    def __init__(self, stage: 'Stage1', x: int, y: int, ref: rect_attributes = 'center', img_dir: str = None, scale: int = 1):
        super().__init__(stage.game, img_dir)
        self.image = pygame.transform.scale_by(self.spritesheet.parse_sprite(f'{self.img_dir.split('\\')[-1]} sprite.png'), scale)
        self.rect = self.image.get_rect()
        setattr(self.rect, ref, (x, y))
        self.mask = pygame.mask.from_surface(pygame.transform.scale_by(self.spritesheet.parse_sprite(f'{self.img_dir.split('\\')[-1]} mask.png'), scale))
        self.stage = stage

    def collided(self, collider):
        if self.stage.player.bullets.has(collider):
            collider.kill()