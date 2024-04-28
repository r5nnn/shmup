import pygame.sprite


class Bullet(pygame.sprite.Sprite):
    def __init__(self, entity, bullet: pygame.Surface, speed: int, atk):
        super().__init__()
        self.atk = atk
        self.image = bullet
        self.rect = self.image.get_rect()
        self.rect.center = (entity.rect.centerx, entity.rect.top)
        self.dx, self.dy = 0, -speed

    def update(self):
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()
        self.rect.move_ip(self.dx, self.dy)
