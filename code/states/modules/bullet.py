from typing import TYPE_CHECKING, override

import pygame.sprite

# avoids relative import error while making pycharm happy
# (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from .entity import Entity


class Bullet(pygame.sprite.Sprite):
    def __init__(self, entity: "Entity",
                 bullet: pygame.Surface, speed: int):
        """
        Creates bullets that shoot out of the entity specified.
        Bullets store attack value from entity

        Args:
            entity: The entity that will shoot the bullet.
            bullet: Surface of the bullet.
            speed: Speed at which the bullet will travel at.
        """
        super().__init__()
        self.atk = entity.atk
        self.image = bullet
        self.rect = self.image.get_rect()
        self.rect.center = (entity.rect.centerx, entity.rect.top)
        self.dx, self.dy = 0, -speed

    @override
    def update(self):
        """Moves the bullet and destroys it if it leaves screen boundaries."""
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()
        self.rect.move_ip(self.dx, self.dy)
