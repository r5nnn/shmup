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
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)
FONT = 'assets\ARCADECLASSIC.TTF'

'''
    Object for making buttons
'''


class Btn:
    def __init__(self, x, y, width, height, font_size, color_pressed, color_released, text, font=FONT,
                 font_color=WHITE):
        # initialise class attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
        self.btn_coords = self.surface.get_rect()
        self.font = pygame.font.Font(font, font_size)  # set font from file path provided, or use default file path
        self.font_color = font_color
        self.color_pressed = color_pressed
        self.color_released = color_released
        self.color = color_released
        self.text = self.font.render(text, True,
                                     font_color)  # create a surface with the specified text drawn on it

    def create(self, surface):
        # call this method to render the button onto a surface
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)
        surface.blit(self.text, (
            self.x + (self.width / 2 - self.text.get_width() / 2),
            self.y + (self.height / 2 - self.text.get_height() / 2)))

    def interact(self):  # Pos is the mouse position: tuple of (x, y) coordinates
        pos = pygame.mouse.get_pos()
        if self.btn_coords.collidepoint(pos):
            self.color = self.color_pressed
        else:
            self.color = self.color_released


run = True
button1 = Btn(10, 10, 50, 50, 32, (87, 87, 87), (43, 43, 43), 'hi')
'''
    Game Mainloop
'''
print(screenx, screeny)
windll.user32.SetCursorPos(screenx // 2, screeny // 2)
while run:
    for event in pygame.event.get():  # iterates through inputs checking if they match the exit event
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
    button1.interact()
    pygame.display.flip()  # update the backdrop surface onto the window
    clock.tick(fps)  # update the clock with the delay of the refresh rate
