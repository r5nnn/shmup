import pygame
from classes.img_ import Img


class Enemy(Img):
    def __init__(self, x, y, img, maskimg):
        super().__init__(x, y, img)
        self.mask = pygame.mask.from_surface(maskimg)
        self.rect.move_ip(0, -200)

    def update(self, surface):
        if self.rect.y != 100:
            self.rect.move_ip(0, 1)