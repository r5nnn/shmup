"""Module for rendering and wrapping text and blitting it onto a surface"""
import pygame

from .constants import rect_attributes


class Txt:
    def __init__(self, font_path: str, size: int, x: int, y: int, text: str, ref: rect_attributes = 'topleft', wrap: bool = False, wrapwidth: int = None):
        """Initialises Txt by splitting the text and wrapping it.

        Sets coordinates of Txt surface and renders text for each line after wrapping.

        Args:
            font_path: File path to .ttf font file.
            size: Size of font.
            x: X coordinate of font
            y: Y coordinate of font
            text: Text to be displayed, if wrap is True, text will automatically wrap to new line when word is too long, or you can specify when to wrap with
            newline '\n'
            ref: References which point on the rect the coordinates point to.
            wrap: If True, text will wrap words when line is longer than wrapwidth, or if newlines are included, text will only wrap when newline occurs.
            wrapwidth: Width when text should start wrapping in pixels, disregarded if newline included in text
        """
        self.x, self.y = x, y
        self.ref = ref
        self.font = pygame.font.Font(font_path, size)
        self.text = self._wrap(text, wrapwidth) if wrap else [text]
        self.rects = []
        # fonts are rendered (not blit) on init in order to refer to their coordinates using self.rects
        y_offset = 0
        for line in self.text:
            font_height = self.font.size(line)[1]
            font_surface = self.font.render(line, True, (255, 255, 255))
            text_rect = font_surface.get_rect()
            setattr(text_rect, self.ref, (self.x, self.y + y_offset))
            self.rects.append(text_rect)
            y_offset += font_height

    def update(self, surface: object, color: tuple[int, int, int] = (255, 255, 255)) -> None:
        """Handles blitting text onto a surface.

        Args:
            surface: Surface to blit text to.
            color: Color of text.
        """
        y_offset = 0  # this is incremented by the font height for each line
        for line in self.text:
            font_height = self.font.size(line)[1]
            font_surface = self.font.render(line, True, color)
            text_rect = font_surface.get_rect()
            setattr(text_rect, self.ref, (self.x, self.y + y_offset))
            surface.blit(font_surface, text_rect)
            y_offset += font_height

    def _wrap(self, text: str, wrapwidth: int) -> list:
        """Wraps text at wrapwidth.

        If text contains newline instead wraps at newline regardless of wrapwidth.

        Args:
            text: Text to be rendered.
            wrapwidth: Maximum allowed width of text before wrapping.

        Returns: A list containing lines that will fit within the given wrapwidth or returns  a list of text split at newline if text contains newline.
        """
        if '\n' in text:
            return text.split('\n')
        words = text.split()  # split at whitespace
        lines = []
        while len(words) > 0:
            line_words = []
            while len(words) > 0:
                # get as many words as will fit within allowed_width and append to current line
                line_words.append(words.pop(0))
                # get width of current line
                font_width = self.font.size(' '.join(line_words + words[:1]))[0]
                if font_width > wrapwidth:
                    break
            lines.append(' '.join(line_words))
        return lines
