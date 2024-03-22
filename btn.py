import pygame
from constants import FONT, WHITE, CLICK, sfx


class Btn:
    def __init__(self, x, y, width, height, font_size, color_hovered, color_clicked, color_released, text_pressed, text,
                 callback, font=FONT, text_released=WHITE, center=None, click_sound=CLICK):
        """
        class for making interactible button objects
        :param x: x coord of top left point of rectangle
        :param y: y coord of top left point of rectangle
        :param width: width of rectangle from point x leftwards
        :param height: height of rectangle from point y downwards
        :param font_size: size of font
        :param color_hovered: color of rectangle when mouse is hovering over it
        :param color_clicked: color of rectangle when being clicked
        :param color_released: original color of rectangle
        :param text_pressed: color of text when rectangle being clicked or hovered
        :param text: text to be displayed
        :param callback: function to be executed when button interacted with
        :param font: font used for text
        :param text_released: color of text, defaults to white
        :param center: optional - if you want to place the rect using coords of the center
        """
        self.sfx = click_sound
        self.center = center
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, self.width, self.height)
        # uses provided rectangle center if it is provided, otherwise uses center based on coordinates given
        if self.center is not None:
            self.rect.center = self.center
        else:
            self.center = self.rect.center
        self.surface = pygame.Surface((self.width, self.height))
        self.btn_coords = self.surface.get_rect()
        self.btn_coords.topleft = self.rect.left, self.rect.top  # makes sure that collidepoint() uses correct coords as
        # if center is provided, coords would be 0, 0
        self.font = pygame.font.Font(font, font_size)  # set font from file path provided, or use default file path
        self.color_hovered = color_hovered
        self.color_released = color_released
        self.color = color_released
        self.text_released = text_released
        self.text_pressed = text_pressed
        self.color_clicked = color_clicked
        self.text_color = text_released
        self.callback = callback
        self.text = self.font.render(text, True, self.text_color)  # update a surface with the specified
        # text drawn on it

    def update(self, surface, event_list):
        """
        call this method to display the button on a surface
        :param event_list: list of user input events to be iterated through
        :param surface: surface to which button should be blitted to
        """

        # draws the rect and text inside
        pygame.draw.rect(surface, self.color, self.rect, 0)
        text_rect = self.text.get_rect(center=self.center)  # centers text in button
        surface.blit(self.text, text_rect)  # blits text surface to window

        # handles button interaction
        pos = pygame.mouse.get_pos()  # Pos is the mouse position: tuple of (x, y) coordinates
        if self.btn_coords.collidepoint(pos):  # collidepoint returns True if mouse coords match up with button coords
            self.text_color = self.text_pressed
            for events1 in event_list:
                # if mouse is hovering over button and clicking
                if events1.type == pygame.MOUSEBUTTONDOWN:
                    sfx.play(self.sfx)
                    self.color = self.color_clicked
                elif events1.type == pygame.MOUSEBUTTONUP:
                    self.color = self.color_hovered
                    self.callback(self)  # function to be called when button clicked
                # if mouse is hovering over button but not clicking
                else:
                    self.color = self.color_hovered
        # if mouse is not hovering nor clicking
        else:
            self.color = self.color_released
            self.text_color = self.text_released
