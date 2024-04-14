"""Module for placing and blitting pygame image surfaces."""
import pygame

from .constants import rect_attributes


class Img:
    def __init__(self, x: int, y: int, img: pygame.Surface, scale: int = 1, ref: rect_attributes = 'center'):
        """Class for blitting image surfaces onto the screen.

        Scales image surface and sets the attribute of the bounding rect to the coordinates provided, using the refrence provided

        Args:
            x: X coordinate of image.
            y: Y coordinate of image.
            img: Surface of image.
            scale: If not 1, scales image by factor provided, using the nearest neighbor algorithm.
            ref: References which point on the rect the coordinates point to.
        """
        self.image = pygame.transform.scale_by(img, scale) if scale != 1 else img
        self.img_rect = self.image.get_rect()
        setattr(self.img_rect, ref, (x, y))

    def update(self, surface: pygame.Surface) -> None:
        """Draws image onto surface.

        Args:
            surface: Surface which image will be blitted to.
        """
        surface.blit(self.image, self.img_rect)
