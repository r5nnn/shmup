import pygame
from img_ import Img


class Bullet(Img):
    def __init__(self, x, y, img, speed):
        super().__init__(x, y, img)
        self.speed = speed

    def update(self):  # noqa
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()
        self.rect.move_ip(0, -self.speed)
