import pygame
import sys
from ctypes import windll

# Initialise game assets and variables

pygame.init()  # all pygame modules initialised - not all will be used, but it is simpler this way

# window dimensions
screenx = windll.user32.GetSystemMetrics(0)
screeny = windll.user32.GetSystemMetrics(1)
winx = 600
winy = 800
screen = pygame.display.set_mode([winx, winy], pygame.SCALED, vsync=0)  # creates the window

# window settings
pygame.display.set_caption('shmup alpha 0.0.1')
icon = pygame.image.load('assets\\icon.png')
pygame.display.set_icon(icon)

# window background
backdrop = pygame.image.load('assets\\stage.png')  # blit everything here
backdrop_coords = screen.get_rect()  # blit to these coords

# game speed
fps = 165
clock = pygame.time.Clock()

# useful shorthands and global variables
BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (255, 255, 255)
ALPHA = (0, 255, 0)
BACKGROUND = (8, 8, 8)
PRIMARY = (255, 228, 134)
SECONDARY = (30, 30, 30)
TERTIARY = (35, 35, 35)
QUATERNARY = (85, 85, 85)
ACCENT = (237, 148, 255)
FONT = 'assets\\Raleway.ttf'


# Object for making buttons

class Btn:
    def __init__(self, x, y, width, height, font_size, color_hovered, color_clicked, color_released, text_pressed, text,
                 callback, font=FONT, text_released=WHITE):
        """
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
        """
        self.text = ''
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
        self.btn_coords = self.surface.get_rect()
        self.btn_coords.topleft = (self.x, self.y)
        self.font = pygame.font.Font(font, font_size)  # set font from file path provided, or use default file path
        self.color_hovered = color_hovered
        self.color_released = color_released
        self.color = color_released
        self.text_released = text_released
        self.text_pressed = text_pressed
        self.color_clicked = color_clicked
        self.text_color = text_released
        self.raw_text = text
        self.callback = callback

    def create(self, surface):
        """
        call this method to render the button onto a surface
        :param surface: surface to which button should be blitted to
        :return: n/a
        """
        self.text = self.font.render(self.raw_text, True,
                                     self.text_color)  # create a surface with the specified text drawn on it
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)
        surface.blit(self.text, (
            self.x + (self.width / 2 - self.text.get_width() / 2),
            self.y + (self.height / 2 - self.text.get_height() / 2)))

    def interact(self, event_list):
        """

        :param event_list: list of events from pygame.event.get()
        :return: n/a
        """
        pos = pygame.mouse.get_pos()  # Pos is the mouse position: tuple of (x, y) coordinates
        if self.btn_coords.collidepoint(pos):  # collidepoint returns True if mouse coords match up with button coords
            self.text_color = self.text_pressed
            for events1 in event_list:
                if events1.type == pygame.MOUSEBUTTONDOWN:
                    self.color = self.color_clicked
                    self.callback(self)
                else:
                    self.color = self.color_hovered

        else:
            self.color = self.color_released
            self.text_color = self.text_released


def printOut(text, size, x, y):
    font = pygame.font.Font(FONT, size)
    screen.blit(font.render(text, True, WHITE), (x, y))


def clicked():
    print('click')


run = True
pause = False
button1 = Btn(10, 10, 90, 50, 30, TERTIARY, QUATERNARY, SECONDARY, PRIMARY, 'Home',
              lambda b: clicked())
button2 = Btn(110, 10, 125, 50, 30, TERTIARY, QUATERNARY, SECONDARY, PRIMARY,
              'Test area', lambda b: clicked())

# Game Mainloop

windll.user32.SetCursorPos(screenx // 2, screeny // 2)
while run:
    events = pygame.event.get()
    for event in events:  # iterates through inputs checking if they match the exit event
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False

        if event.type == pygame.KEYDOWN:  # alternative way to exit through keybind
            if event.key == pygame.K_q:
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False
            if event.key == pygame.K_ESCAPE:
                pause = True
            else:
                pause = False
    screen.blit(backdrop, backdrop_coords)
    if not pause:
        printOut('Press esc to pause', 32, winx / 2 - 140, winy / 2 - 20)
    else:
        button1.create(screen)
        button2.create(screen)
        button1.interact(events)
        button2.interact(events)
    mouse = pygame.mouse.get_pos()  # stores the (x,y) coordinates into the variable as a tuple
    pygame.display.flip()  # update the backdrop surface onto the window
    clock.tick(fps)  # update the clock with the delay of the refresh rate
