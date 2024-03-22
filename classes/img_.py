import pygame


class Img(pygame.sprite.Sprite):
    def __init__(self, x, y, img, center=None):
        """
        creates an image sprite
        :param x: topleft x coordinate of where image should be placed on screen
        :param y: topleft y coordinate of where image should be placed on screen
        :param img: image file path
        :param center: optional argument incase image should be placed via center coordinates instead of topleft
        """
        pygame.sprite.Sprite.__init__(self)  # initialise the constructor of the pygame.sprite.Sprite class
        self.image = img
        self.bounds = None
        self.border = None
        self.rect = self.image.get_rect()
        if center is not None:
            self.rect.center = center
        else:
            self.rect.x, self.rect.y = x, y

    def update(self, surface):
        surface.blit(self.image, self.rect)
