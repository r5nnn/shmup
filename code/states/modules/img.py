"""Places and blits pygame image surface."""
from typing import Literal
import pygame


class Img(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, img: pygame.Surface, scale: int = 1,
                 ref: Literal['topleft', 'midtop', 'topright',
                              'midleft', 'center', 'midright',
                              'bottomleft', 'midbottom', 'bottomright'] = 'center'):
        """Initialises Img with proper coordinates.

        Scales image surface and sets the attribute of the bounding rect to the coordinates provided, using the refrence provided

        Args:
            x: X coordinate of image.
            y: Y coordinate of image.
            img: Surface of image.
            scale: If not 1, scales image by factor provided, using the nearest neighbor algorithm.
            ref: References which point on the rect the coordinates point to.
        """
        super().__init__()  # pygame.sprite.Sprite is not used in this class, but child classes inheriting from this parent will
        self.image = pygame.transform.scale_by(img, scale) if scale != 1 else img
        self.rect = self.image.get_rect()
        setattr(self.rect, ref, (x, y))

    def update(self, surface: pygame.Surface) -> None:
        """Draws image onto surface.

        Args:
            surface: Surface which image will be blitted to.
        """
        surface.blit(self.image, self.rect)
