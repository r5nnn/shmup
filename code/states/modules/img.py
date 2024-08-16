import pygame

from .constants import rect_allignments


class Img:
    def __init__(self,
                 coords: tuple[int, int],
                 img: pygame.Surface,
                 scale: int = 1,
                 allign: rect_allignments = 'center'):
        """
        Class for rendering images to the screen.
        Can also scale images and allows alligning the text.

        Args:
            coords: X and Y coordinates of image.
            img: Surface of image.
            scale: If not 1, scales image by factor provided, using the nearest
            neighbor algorithm.
            allign: References which point on the rect the coordinates point to.
        """
        self.image = pygame.transform.scale_by(img, scale) \
            if scale != 1 else img
        self.img_rect = self.image.get_rect()
        setattr(self.img_rect, allign, (coords[0], coords[1]))

    def update(self, surface: pygame.Surface) -> None:
        """
        Renders image onto surface.

        Args:
            surface: Surface which image will be blitted to.
        """
        surface.blit(self.image, self.img_rect)
