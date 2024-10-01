import warnings

import pygame

from .constants import rect_allignments


class Txt:
    """
    Attributes:
        default_font_dir: Set to a font directory else font object must be
        passed each time a Txt class or any of its child classes is created.
        """
    default_font_dir = None

    def __init__(self,
                 coords: tuple[int, int],
                 text: str,
                 font: pygame.font.Font = None,
                 size: int = None,
                 allign: rect_allignments = 'topleft',
                 wrap_width: int = None):
        """
        Class for creating and managing text surfaces.
        Allows for wrapping text at a specific pixel
        width or manually with a newline character.
        Additionally allows alligning the text.

        Examples:
            Txt.default_font_dir = "font.ttf"
            # size argument must be included as font object was not included
            t1 = Txt(500, 500, "text", size=32, allign="center")
            # size and wrap_width can be omitted
            # sincefont object and newline included
            t2 = Txt(0, 0, "line 1\nline 2", pygame.font.Font("font.ttf", 32))

            while True:
                t1.update(screen)
                t2.update(screen)

        Args:
            coords: X and Y coordinates of font.
            font: The pygame.font.Font object to use.
            text: Text to be displayed, include \n for new line.
            allign: Alligns the rectangle coordinates to the specified position.
            Check rect_allignments in constants.py for all the options.
            wrap_width: Width when text should start wrapping in pixels.
            Cannot be used when newline character included.
        """
        if font and size is None:
            raise TypeError("size attribute must be specified"
                            " if default font used.")
        elif (font and size) is not None:
            warnings.warn("size parameter is not needed"
                          " when pygame.font.Font used")

        self.x = coords[0]
        self.y = coords[1]
        self.allign = allign
        self.font = font if font is not None else \
            pygame.font.Font(Txt.default_font_dir, size)
        self.text = self._wrap(text, wrap_width) \
            if wrap_width is not None else [text]
        self.rects = []
        # fonts are rendered (not blit) on init in order
        # to refer to their coordinates using self.rects
        y_offset = 0
        for line in self.text:
            font_height = self.font.size(line)[1]
            font_surface = self.font.render(line, True, (255, 255, 255))
            text_rect = font_surface.get_rect()
            setattr(text_rect, self.allign, (self.x, self.y + y_offset))
            self.rects.append(text_rect)
            y_offset += font_height

    def blit(self,
             surface: pygame.surface.Surface,
             color: tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Displays and updates the text.

        Args:
            surface: Surface to blit text to.
            color: Color of the text.
        """
        y_offset = 0  # this is incremented by the font height for each line
        for line in self.text:
            font_height = self.font.size(line)[1]
            font_surface = self.font.render(line, True, color)
            text_rect = font_surface.get_rect()
            setattr(text_rect, self.allign, (self.x, self.y + y_offset))
            surface.blit(font_surface, text_rect)
            y_offset += font_height

    def _wrap(self, text: str, wrap_width: int) -> list:
        """
        Wraps text at wrap_width.
        If text contains newline instead wraps at newline regardless of
        wrap_width.

        Args:
            text: Text to be rendered.
            wrap_width: Maximum allowed width of text before wrapping.

        Returns: A list containing lines that will fit within the given
        wrap_width or returns a list of text split at newline if text contains
        newline.
        """
        if '\n' in text:
            return text.split('\n')
        words = text.split()  # split at whitespace
        lines = []
        while len(words) > 0:
            line_words = []
            while len(words) > 0:
                # get as many words as will fit within
                # allowed_width and append to current line
                line_words.append(words.pop(0))
                # get width of current line
                font_width = self.font.size(' '.join(line_words + words[:1]))[0]
                if font_width > wrap_width:
                    break
            lines.append(' '.join(line_words))
        return lines
