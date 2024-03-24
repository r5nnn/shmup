import pygame
from classes.img_ import Img


class Bullet(Img):
    def __init__(self, x, y, img, maskimg, speed):
        super().__init__(x, y, img)
        self.mask = pygame.mask.from_surface(maskimg)
        self.speed = speed

    def update(self, type):  # noqa
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()
        self.rect.move_ip(0, -self.speed)