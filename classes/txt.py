import pygame


class Txt:
    def __init__(self, x, y, text, size, font, text_color, pos='left', center=None):
        """
        class for making non-interactible text
        :param x: x coord of top left point of text
        :param y: y coord of top left point of text
        :param text: text to be displayed
        :param size: size of font for text
        :param font: what font to use for text
        :param text_color: color of displayed text
        :param center: optional - if you want to place the text using coords of the center
        :param pos: optional - if you want to position text from anything other than top left corner
        """
        self.pos = pos
        self.center = center
        self.text_color = text_color
        self.y = y
        self.x = x
        self.font = pygame.font.Font(font, size)  # updates a font object
        self.text_split = text.split('\n')
        self.text_list = []
        for sentence in self.text_split:
            self.fontRender = self.font.render(sentence, True, self.text_color)  # update a surface with the specified
            # text drawn on it
            self.text_list.append(self.fontRender)
        for lines in self.text_list:
            if self.center is not None:
                self.text_rect = lines.get_rect(center=self.center)  # update a temporary rect the size of the text and
                # set the center to tuple given
                self.text_rect.center = self.center
            else:
                match self.pos:
                    case 'left':
                        self.text_rect = lines.get_rect()  # update a temporary rect the size of the text and specify
                        # the x and y coordinates (since it defaults to 0)
                        self.text_rect.topleft = (self.x, self.y)
                        self.center = self.text_rect.center
                    case 'right':
                        self.text_rect = lines.get_rect()
                        self.text_rect.topright = (self.x, self.y)
                        self.center = self.text_rect.center

    def update(self, surface):
        """
        call this method to display the button on a surface
        """
        for lines in self.text_list:
            surface.blit(lines, self.text_rect)
