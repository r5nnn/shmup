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

# useful shorthands and global variables

# colors
BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (255, 255, 255)
ALPHA = (0, 255, 0)
BACKGROUND = (8, 8, 8)
PRIMARY = (255, 228, 134)  # light yellow
SECONDARY = (30, 30, 30)  # dark gray
TERTIARY = (35, 35, 35)  # gray
QUATERNARY = (85, 85, 85)  # light gray
ACCENT = (255, 148, 252)  # light pink

# assets
FONT = 'assets\\fonts\\Raleway.ttf'  # font taken from: https://fonts.google.com/specimen/Raleway
PLAYER = pygame.image.load('assets\\textures\\player.png').convert()
ICON = pygame.image.load('assets\\textures\\icon.png').convert()
backdrop = pygame.image.load('assets\\textures\\STAGE.png').convert()  # surface to blit everything to
# from https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit
# blit means to Draw a source Surface onto the current Surface. The draw can be positioned with the dest argument.

# game info
STAGE_STRUCTURE = ['home', 'paused', 'options', 'keybinds']
INGAME_STRUCTURE = ['game', 'paused', 'options', 'keybinds']
KEYS = [['ESC', 'Return to previous screen']]
KEY_ARRAY = [[50, 270 + (i * 40), KEYS[i][0], 32, FONT, WHITE] for i in range(len(KEYS))]
INFO_ARRAY = [[winx - 50, 270 + (i * 40), KEYS[i][1], 32, FONT, WHITE] for i in range(len(KEYS))]

# status
STAGE = 'home'
RUN = True
INGAME = False

# window settings
pygame.display.set_caption('shmup alpha 0.0.1')
pygame.display.set_icon(ICON)

# window background
backdrop_coords = screen.get_rect()  # coordinates of surface

# game speed
fps = 165
clock = pygame.time.Clock()


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
        self.font = pygame.font.Font(font, size)  # creates a font object
        self.text = self.font.render(text, True, self.text_color)  # create a surface with the specified
        # text drawn on it
        if self.center is not None:
            self.text_rect = self.text.get_rect(center=self.center)  # create a temporary rect the size of the text and
            # set the center to tuple given
            self.text_rect.center = self.center
        else:
            match self.pos:
                case 'left':
                    self.text_rect = self.text.get_rect()  # create a temporary rect the size of the text and specify
                    # the x and y coordinates (since it defaults to 0)
                    self.text_rect.topleft = (self.x, self.y)
                    self.center = self.text_rect.center
                case 'right':
                    self.text_rect = self.text.get_rect()
                    self.text_rect.topright = (self.x, self.y)
                    self.center = self.text_rect.center

    def create(self):
        """
        call this method to display the button on a surface
        """
        screen.blit(self.text, self.text_rect)


class Btn:
    def __init__(self, x, y, width, height, font_size, color_hovered, color_clicked, color_released, text_pressed, text,
                 callback, font=FONT, text_released=WHITE, center=None):
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
                elif events1.type == pygame.MOUSEBUTTONUP:
                    self.callback(self)  # function to be called when button clicked
                # if mouse is hovering over button but not clicking
                else:
                    self.color = self.color_hovered
        # if mouse is not hovering nor clicking
        else:
            self.color = self.color_released
            self.text_color = self.text_released


class Player:
    def __init__(self, x, y, width, height, speed, img):
        self.img = img
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(x, y, self.width, self.height)
        self.rect_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.speed = speed
        self.bounds = None

    def create(self, bounds):
        border = bounds.get_rect()
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if key[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if key[pygame.K_UP]:
            self.rect.move_ip(0, -self.speed)
        if key[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed)
        self.rect.clamp_ip(border)
        pygame.draw.rect(self.rect_surf, ACCENT, self.rect_surf.get_rect())
        screen.blit(self.img, self.rect)


def cmd(name):
    """
    call this method to update the stage of the screen
    :param name: the stage you want to switch to
    """
    global STAGE, STAGE_STRUCTURE, INGAME_STRUCTURE
    STAGE_STRUCTURE_POINTER = STAGE_STRUCTURE.index(STAGE)
    if name == 'back':
        if STAGE_STRUCTURE_POINTER != 0:
            STAGE = STAGE_STRUCTURE[STAGE_STRUCTURE_POINTER - 1]
        else:
            if INGAME:
                INGAME_STRUCTURE_POINTER = INGAME_STRUCTURE.index(STAGE)
                STAGE = INGAME_STRUCTURE[INGAME_STRUCTURE_POINTER]
            else:
                STAGE = STAGE_STRUCTURE[STAGE_STRUCTURE_POINTER]
    else:
        STAGE = name


# buttons
back_btn = Btn(0, 0, 205, 50, 30, TERTIARY, QUATERNARY, SECONDARY, PRIMARY, 'Back',
               lambda b: cmd('back'), center=(winx / 2, 300))
options_btn = Btn(0, 0, 205, 50, 30, TERTIARY, QUATERNARY, SECONDARY, PRIMARY, 'Options',
                  lambda b: cmd('options'), center=(winx / 2, 225))
keybinds_btn = Btn(0, 0, 205, 50, 30, TERTIARY, QUATERNARY, SECONDARY, PRIMARY, 'Keybinds',
                   lambda b: cmd('keybinds'), center=(winx / 2, 225))
play_btn = Btn(0, 0, 300, 75, 35, TERTIARY, QUATERNARY, SECONDARY, PRIMARY, 'Play',
               lambda b: cmd('game'), center=(winx / 2, winy / 2))

# display text
temp_txt = Txt(0, 0, 'Press esc to pause', 32, FONT, WHITE, center=(winx / 2, winy / 2 - 100))
paused_txt = Txt(0, 0, 'Paused', 64, FONT, WHITE, center=(winx / 2, 150))
options_txt = Txt(0, 0, 'Options', 64, FONT, WHITE, center=(winx / 2, 150))
keybinds_txt = Txt(0, 0, 'Keybinds', 64, FONT, WHITE, center=(winx / 2, 150))
keybindsKEY_ARRAY_txt = Txt(50, 200, 'Keys', 48, FONT, WHITE)
keybindsInfo_txt = Txt(winx - 50, 200, 'Description', 48, FONT, WHITE, pos='right')
KEY_ARRAY = [Txt(i[0], i[1], i[2], i[3], i[4], i[5]) for i in KEY_ARRAY]
INFO_ARRAY = [Txt(i[0], i[1], i[2], i[3], i[4], i[5], pos='right') for i in INFO_ARRAY]

# game objects
player = Player(winx/2, winy/2, 27, 19, 2, PLAYER)

windll.user32.SetCursorPos(screenx // 2, screeny // 2)

# Game Mainloop

while RUN:
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
                if STAGE == 'home' or STAGE == 'game':
                    STAGE = 'paused'
                else:
                    cmd('back')
    screen.blit(backdrop, backdrop_coords)

    # match case statement to toggle between multiple stages when navigating menus and options
    match STAGE:
        case 'home':
            temp_txt.create()
            play_btn.create(screen, events)
        case 'paused':
            paused_txt.create()
            options_btn.create(screen, events)
            back_btn.create(screen, events)
        case 'options':
            options_txt.create()
            keybinds_btn.create(screen, events)
            back_btn.create(screen, events)
        case 'keybinds':
            keybinds_txt.create()
            keybindsKEY_ARRAY_txt.create()
            keybindsInfo_txt.create()
            for i in KEY_ARRAY:
                i.create()
            for i in INFO_ARRAY:
                i.create()
        case 'game':
            INGAME = True
            player.create(screen)

    mouse = pygame.mouse.get_pos()  # stores the (x,y) coordinates into the variable as a tuple
    pygame.display.flip()  # update the backdrop surface onto the window
    clock.tick(fps)  # update the clock with the delay of the refresh rate
