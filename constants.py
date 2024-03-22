import pygame
from ctypes import windll

pygame.mixer.pre_init(75100, -16, 2, 2048)  # frequency, size, channels and buffer of audio
pygame.init()

# window dimensions
screenx = windll.user32.GetSystemMetrics(0)
screeny = windll.user32.GetSystemMetrics(1)
winx = screenx
winy = screeny
screen = pygame.display.set_mode((winx, winy), pygame.NOFRAME, pygame.SCALED, vsync=0)  # updates the window,
# pygame.NOFRAME makes the window borderless and pygame.SCALED means any textures are scaled proportional to window
# size (4k display compatibility)

# backgrounds
BACKDROP = pygame.image.load('assets\\textures\\background\\menu.png').convert()  # surface to blit everything to
# from https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit
# blit means to Draw a source Surface onto the current Surface. The draw can be positioned with the dest argument.

# colors
BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (255, 255, 255)
ALPHA = (0, 255, 0)
BACKGROUND = (8, 8, 8)  # almost black
PRIMARY = (255, 228, 134)  # light yellow
SECONDARY = (30, 30, 30)  # dark gray
TERTIARY = (35, 35, 35)  # gray
QUATERNARY = (85, 85, 85)  # light gray
ACCENT = (255, 148, 252)  # light pink

# fonts
FONT = 'assets\\fonts\\editundo.ttf'  # font taken from: https://www.dafont.com/edit-undo.font

# icons
ICON = pygame.image.load('assets\\textures\\icon\\icon.png').convert()
LOGO = pygame.image.load('assets\\textures\\icon\\logo.png').convert()

# bullets
BULLETS = {
    'player': pygame.image.load('assets\\textures\\bullets\\bullet.png').convert()
}

# music
MENULOOP = pygame.mixer.Sound('assets\\music\\menuloop.wav')
GAME1 = pygame.mixer.Sound('assets\\music\\game1.wav')
CLICK = pygame.mixer.Sound('assets\\music\\click.wav')

MENULOOP.set_volume(0.2)
GAME1.set_volume(0.2)
CLICK.set_volume(0.2)
bg = pygame.mixer.Channel(0)  # channel 0 is for background soundtracks
song = pygame.mixer.Channel(1)  # channel 1 is for in game soundtracks
sfx = pygame.mixer.Channel(2)  # channel 2 is for sfx