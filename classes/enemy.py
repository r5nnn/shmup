import pygame
from classes.img_ import Img
from constants import KILL, sfxKill


class Enemy(Img):
    def __init__(self, x, y, img, maskimg, hp, center=None):
        super().__init__(x, y, img, center)
        self.hp = hp
        self.mask = pygame.mask.from_surface(maskimg)
        self.rect.move_ip(0, -200)

    def update(self, surface):
        if self.rect.y != 100:
            self.rect.move_ip(0, 1)
        if self.hp == 0:
            self.kill()
            sfxKill.play(KILL)

    def hit(self, dmg):
        self.hp -= dmg
