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
backdrop = pygame.image.load('assets\\STAGE.png')  # surface to blit everything to
# from https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit
# blit means to Draw a source Surface onto the current Surface. The draw can be positioned with the dest argument.
backdrop_coords = screen.get_rect()  # coordinates of surface

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
STAGE = 'home'


class Txt:
    def __init__(self, x, y, text, size, font, text_color, center=None):
        self.center = center
        self.text_color = text_color
        self.y = y
        self.x = x
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, self.text_color)  # create a surface with the specified
        # text drawn on it
        if self.center is not None:
            self.text_rect = self.text.get_rect(center=self.center)
            self.text_rect.center = self.center
        else:
            self.text_rect = self.text.get_rect(x=self.x, y=self.y)
            self.center = self.text_rect.center

    def create(self):
        """
        call this method to display the button on a surface
        """
        screen.blit(self.text, self.text_rect)


# Object for making buttons

class Btn:
    def __init__(self, x, y, width, height, font_size, color_hovered, color_clicked, color_released, text_pressed, text,
                 callback, font=FONT, text_released=WHITE, center=None):
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
        :param center: optional - if you want to place the rect using coords of the center
        """
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
        self.text = self.font.render(text, True, self.text_color)  # create a surface with the specified
        # text drawn on it

    def create(self, surface, event_list):
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
                    self.color = self.color_clicked
                    self.callback(self)  # function to be called when button clicked
                # if mouse is hovering over button but not clicking
                else:
                    self.color = self.color_hovered
        # if mouse is not hovering nor clicking
        else:
            self.color = self.color_released
            self.text_color = self.text_released


# temporary function for printing text to center of window
def printOut(text, size):
    """
    blits given string to center of window
    :param text: text to be blit
    :param size: font size
    """
    font = pygame.font.Font(FONT, size)
    text = font.render(text, True, WHITE)
    text_rect = text.get_rect(center=(winx / 2, winy / 2))
    screen.blit(text, text_rect)


def cmd(name):
    """
    call this method to update the stage of the screen
    :param name: the stage you want to switch to
    """
    global STAGE
    STAGE = name


run = True

# buttons

back_btn = Btn(0, 0, 205, 50, 30, TERTIARY, QUATERNARY, SECONDARY, PRIMARY, 'Back',
               lambda b: cmd('home'), center=(winx / 2, 300))
options_btn = Btn(0, 0, 205, 50, 30, TERTIARY, QUATERNARY, SECONDARY, PRIMARY, 'Options',
               lambda b: cmd('options'), center=(winx/2, 225))

# display text
temp_text = Txt(0, 0, 'Press esc to pause', 32, FONT, WHITE, center=(winx/2, winy/2))
paused_text = Txt(0, 0, 'Paused', 64, FONT, WHITE, center=(winx/2, 150))
options_text = Txt(0, 0, 'Options', 64, FONT, WHITE, center=(winx/2, 150))
graphics_txt = Txt(10, 10, 'graphics go here', 32, FONT, WHITE)

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
                if STAGE == 'paused_home':
                    cmd('home')
                else:
                    cmd('paused_home')
    screen.blit(backdrop, backdrop_coords)
    # match case statement to toggle between multiple stages when navigating menus and options
    match STAGE:
        case 'home':
            temp_text.create()
        case 'paused_home':
            paused_text.create()
            options_btn.create(screen, events)
            back_btn.create(screen, events)
        case 'options':
            options_text.create()
        case 'paused_graphics':
            graphics_txt.create()
    mouse = pygame.mouse.get_pos()  # stores the (x,y) coordinates into the variable as a tuple
    pygame.display.flip()  # update the backdrop surface onto the window
    clock.tick(fps)  # update the clock with the delay of the refresh rate
