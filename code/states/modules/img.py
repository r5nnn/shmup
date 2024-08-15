import pygame

from .constants import rect_allignments


class Img:
    def __init__(self, x: int, y: int, img: pygame.Surface,
                 scale: int = 1, allign: rect_allignments = 'center'):
        """
        Class for rendering images to the screen.
        Can also scale images and allows alligning the text.

        Args:
            x: X coordinate of image.
            y: Y coordinate of image.
            img: Surface of image.
            scale: If not 1, scales image by factor provided, using the nearest
            neighbor algorithm.
            allign: References which point on the rect the coordinates point to.
        """
        self.image = pygame.transform.scale_by(img, scale) \
            if scale != 1 else img
        self.img_rect = self.image.get_rect()
        setattr(self.img_rect, allign, (x, y))

    def update(self, surface: pygame.Surface) -> None:
        """
        Renders image onto surface.

        Args:
            surface: Surface which image will be blitted to.
        """
        surface.blit(self.image, self.img_rect)
