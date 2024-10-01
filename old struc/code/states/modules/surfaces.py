import warnings

import pygame

from .constants import rect_allignments


class Surf:
    def __init__(self,
                 surface: pygame.Surface,
                 color: tuple[int, int, int] | tuple[int, int, int, int] = None,
                 alpha: int = None,
                 coords: tuple[int, int] = None,
                 allign: rect_allignments = None):
        """
        Class for managing pygame surface objects.
        Option to use surface alpha or per pixel alpha keys.
        There is no point of using this class for creating rects if transparency
        isn't used.

        Args:
            surface: The pygame surface object.
            color: The color of the surface, if unspecified surface is black.
            Accepts RGB or RGBA formats. If RGBA is provided, pygame.SRCALPHA
            must be included in the surface arguments. RGBA uses per pixel
            alpha.
            alpha: The surface alpha value.
        """
        if color is not None and len(color) == 4:
            if alpha is not None:
                warnings.warn(
                     f"Both surface alpha: {alpha} and per pixel alpha: "
                     f"{color[4]} specified."
                )
            if surface.get_flags() != 65536:
                warnings.warn(
                    f"Per pixel alpha provided: {color}, but surface is missing"
                    f" the pygame.SRCALPHA flag."
                )
        self.surface = surface
        self.coords = coords
        if color is not None: self.surface.fill(color)
        if alpha is not None: self.surface.set_alpha(alpha)
        if allign is not None:
            self.rect = surface.get_rect()
            setattr(self.rect, allign, coords)

    def blit(self,
             surface: pygame.Surface,
             coords: tuple[int, int] = None,
             allign: rect_allignments = None) -> None:
        """
        Places the surface onto another surface.
        Allows for specifying the allignment of the surface coordinates.

        Args:
            surface: The surface to place the object's surface on.
            coords: The coordinates of the surface to place.
            allign: The allignment of the surface coordinates,
            if top left, leave unspecified.
        """
        if coords and self.coords is not None:
            warnings.warn(f"Specifying coordinates at blit: {coords} "
                          f"unneccessary when specified at init: {self.coords}")
        if allign and self.rect is not None:
            warnings.warn(f"Specifying allign: {allign} when coordinates "
                          f"already alligned is unnecessary.")
        coords = self.coords if self.coords is not None else coords
        if coords and self.rect is None:
            raise TypeError("Coordinates must be specified if not specified at "
                            "init.")

        if allign is None:
            self.surface.blit(
                surface, coords if coords is not None else self.rect)
        else:
            rect = self.surface.get_rect()
            setattr(rect, allign, coords)
            self.surface.blit(surface, rect)


class Img(Surf):
    def __init__(self,
                 image: pygame.Surface,
                 scale: int | tuple[int, int] = 1,
                 alpha: bool | int = False,
                 coords: tuple[int, int] = None,
                 allign: rect_allignments = None):
        """
        Class for managing pygame surface objects containing images.
        Can apply per pixel alpha and surface alpha to an existing image.
        Can also scale the image using nearest neighbor interpolation.

        Args:
            image: The pygame surface object.
            scale: The scale of the image, uses nearest neighbor interpolation.
            alpha: If true applies per pixel alpha, or if an integer sets the
            alpha of the image to the value provided.
            coords: The coordinates of the image to place.
            allign: The allignment of the surface coordinates,
            if top left, leave unspecified.
        """
        if scale != 1:
            image = pygame.transform.scale_by(image, scale)
        if alpha:
            image.convert_alpha()
        else:
            image.convert()
        super().__init__(image, alpha=alpha if type(alpha is int) else None,
                         coords=coords, allign=allign)
