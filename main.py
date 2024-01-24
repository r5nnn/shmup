import pygame
import sys
from ctypes import windll

'''
    Initialise game assets and variables
'''
pygame.init()  # pygame modules loaded

# window dimensions
screenx = windll.user32.GetSystemMetrics(0)
screeny = windll.user32.GetSystemMetrics(1)
worldx = 600
worldy = 800
world = pygame.display.set_mode([worldx, worldy], pygame.SCALED, vsync=0)  # initialises the window

pygame.display.set_caption('shmup alpha 0.0.0')  # set window title
icon = pygame.image.load('assets\icon.png')  # load image from file path
pygame.display.set_icon(icon)  # set image as window icon
fps = 60  # number of times game refreshes per second
backdrop = pygame.image.load('assets\stage.png')  # load window background
backdropbox = world.get_rect()  # get coords of window
clock = pygame.time.Clock()  # object to help track time

# useful shorthands
BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (255, 255, 255)
ALPHA = (0, 255, 0)
BACKGROUND = (8, 8, 8)
PRIMARY = (255, 228, 134)
SECONDARY = (30, 30, 30)
TERTIARY = (35, 35, 35)
ACCENT = (237, 148, 255)
FONT = 'assets\Guazhiru.ttf'

'''
    Object for making buttons
'''


class Btn:
    def __init__(self, x, y, width, height, font_size, color_pressed, color_released, text_pressed, text, callback,
                 font=FONT,
                 text_released=WHITE):
        # initialise class attributes
        self.text = ''
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
        self.btn_coords = self.surface.get_rect()
        self.font = pygame.font.Font(font, font_size)  # set font from file path provided, or use default file path
        self.color_pressed = color_pressed
        self.color_released = color_released
        self.color = color_released
        self.outline_color = self.color
        self.text_released = text_released
        self.text_pressed = text_pressed
        self.text_color = text_released
        self.raw_text = text
        self.callback = callback

    def create(self, surface):
        # call this method to render the button onto a surface
        self.text = self.font.render(self.raw_text, True,
                                     self.text_color)  # create a surface with the specified text drawn on it
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(surface, self.outline_color, (self.x, self.y, self.width, self.height), 2, border_radius=1)
        surface.blit(self.text, (
            self.x + (self.width / 2 - self.text.get_width() / 2),
            self.y + (self.height / 2 - self.text.get_height() / 2)))

    def interact(self, event_list):  # Pos is the mouse position: tuple of (x, y) coordinates
        pos = pygame.mouse.get_pos()
        if self.btn_coords.collidepoint(pos):
            self.color = self.color_pressed
            self.text_color = self.text_pressed
            for events in event_list:
                if events.type == pygame.MOUSEBUTTONDOWN:
                    self.outline_color = self.text_pressed
                    self.callback(self)
                else:
                    self.outline_color = self.color

        else:
            self.outline_color = self.color
            self.color = self.color_released
            self.text_color = self.text_released


def clicked():
    print('click!')


run = True
button1 = Btn(10, 10, 90, 50, 32, TERTIARY, SECONDARY, PRIMARY, 'paused', lambda b: clicked())
'''
    Game Mainloop
'''
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
            if event.key == ord('q'):
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False
    world.blit(backdrop, backdropbox)
    mouse = pygame.mouse.get_pos()  # stores the (x,y) coordinates into the variable as a tuple
    button1.create(world)
    button1.interact(events)
    pygame.display.flip()  # update the backdrop surface onto the window
    clock.tick(fps)  # update the clock with the delay of the refresh rate
