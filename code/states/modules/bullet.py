"""Module for placing and blitting bullets."""
from typing import TYPE_CHECKING, override

import pygame.sprite

if TYPE_CHECKING:
    from .entity import Enemy, Entity


class Bullet(pygame.sprite.Sprite):
    def __init__(self, entity: "Entity", bullet: pygame.Surface, speed: int, atk: int):
        """Parent class for all types of bullets.

        Initialises the bullet image and grabs coordinates from specified surface

        Args:
            entity: The entity that will shoot the bullet.
            bullet: Surface of the bullet.
            speed: Speed at which the bullet will travel at.
            atk: Damage that bullet should do on contact.
        """
        super().__init__()
        self.atk = atk
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
