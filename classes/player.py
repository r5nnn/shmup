import pygame
from classes.img_ import Img


class Player(Img):
    def __init__(self, x, y, img, speed, slo_speed):
        """
        child of Img class, specific class for creating player
        :param x: check parent class
        :param y: ...
        :param speed: speed at which player moves
        :param slo_speed: speed at which player moves when holding shift
        """
        self.imgState = None
        self.fast = speed
        self.slow = slo_speed
        self.speed = self.fast
        super().__init__(x, y, img=img['idle'])
        self.image = img

    def update(self, bounds):  # noqa
        border = bounds.get_rect()
        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            self.speed = self.slow
            self.imgState = self.image['idle_hitbox']
        else:
            self.speed = self.fast
            self.imgState = self.image['idle']
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            if key[pygame.K_LSHIFT]:
                self.imgState = self.image['left_hitbox']
            else:
                self.imgState = self.image['left']
            self.rect.move_ip(-self.speed, 0)
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            if key[pygame.K_LSHIFT]:
                self.imgState = self.image['right_hitbox']
            else:
                self.imgState = self.image['right']
            self.rect.move_ip(self.speed, 0)
        if key[pygame.K_UP] or key[pygame.K_w]:
            if key[pygame.K_LSHIFT]:
                self.imgState = self.image['up_hitbox']
            else:
                self.imgState = self.image['up']
            self.rect.move_ip(0, -self.speed)
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            if key[pygame.K_LSHIFT]:
                self.imgState = self.image['down_hitbox']
            else:
                self.imgState = self.image['down']
            self.rect.move_ip(0, self.speed)
        self.rect.clamp_ip(border)
        bounds.blit(self.imgState, self.rect)
