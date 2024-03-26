import pygame
from ctypes import windll

pygame.mixer.pre_init(75100, -16, 8, 512)  # frequency, size, channels and buffer of audio
pygame.init()

# window dimensions
screenx = windll.user32.GetSystemMetrics(0)
screeny = windll.user32.GetSystemMetrics(1)
winx = screenx
winy = screeny
screen = pygame.display.set_mode((winx, winy), pygame.NOFRAME, pygame.SCALED, vsync=0)  # updates the window,
# pygame.NOFRAME makes the window borderless and pygame.SCALED means any textures are scaled proportional to window
# size (4k display compatibility)

previous_time = [pygame.time.get_ticks(), pygame.time.get_ticks()]  # used for a delay when shooting

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

# music
MENULOOP = pygame.mixer.Sound('assets\\music\\menu\\menuloop.wav')
GAME1 = pygame.mixer.Sound('assets\\music\\game\\game1.wav')
CLICK = pygame.mixer.Sound('assets\\music\\sfx\\click.wav')
SHOOT = pygame.mixer.Sound('assets\\music\\sfx\\shoot.wav')
KILL = pygame.mixer.Sound('assets\\music\\sfx\\hit.wav')
DIE = pygame.mixer.Sound('assets\\music\\sfx\\die.wav')

MENULOOP.set_volume(0.2)
GAME1.set_volume(0.2)
CLICK.set_volume(0.2)
SHOOT.set_volume(0.05)
KILL.set_volume(0.2)
DIE.set_volume(0.2)
bg = pygame.mixer.Channel(0)  # channel 0 is for background soundtracks
song = pygame.mixer.Channel(1)  # channel 1 is for in game soundtracks
sfxShoot = pygame.mixer.Channel(2)  # channel 2 is for shoot
sfxKill = pygame.mixer.Channel(3)  # channel 3 is for sfx
sfxDie = pygame.mixer.Channel(4)  # channel 4 is for sfx

# sprite groups
enemy_bullets = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# player
# dict to make referring to file path easy
PLAYER = {
    'idle': pygame.image.load('assets\\textures\\player\\player.png').convert_alpha(),
    'idle_hitbox': pygame.image.load('assets\\textures\\player\\player_hitbox.png').convert_alpha(),
    'left': pygame.image.load('assets\\textures\\player\\playerL.png').convert_alpha(),
    'left_hitbox': pygame.image.load('assets\\textures\\player\\playerL_hitbox.png').convert_alpha(),
    'right': pygame.image.load('assets\\textures\\player\\playerR.png').convert_alpha(),
    'right_hitbox': pygame.image.load('assets\\textures\\player\\playerR_hitbox.png').convert_alpha(),
    'up': pygame.image.load('assets\\textures\\player\\playerU.png').convert_alpha(),
    'up_hitbox': pygame.image.load('assets\\textures\\player\\playerU_hitbox.png').convert_alpha(),
    'down': pygame.image.load('assets\\textures\\player\\playerD.png').convert_alpha(),
    'down_hitbox': pygame.image.load('assets\\textures\\player\\playerD_hitbox.png').convert_alpha(),
}

ENEMY = {
    'idle': pygame.image.load('assets\\textures\\enemy\\enemy.png').convert_alpha(),
    'idlemask': pygame.image.load('assets\\textures\\enemy\\enemy_hitbox.png').convert_alpha()
}

# bullets
BULLETS = {
    'player': pygame.image.load('assets\\textures\\bullets\\bullet.png').convert(),
    'playermask': pygame.image.load('assets\\textures\\bullets\\bullet_hitbox.png').convert(),
    'enemy': pygame.image.load('assets\\textures\\bullets\\bullet.png').convert(),
    'enemymask': pygame.image.load('assets\\textures\\bullets\\bullet_hitbox.png').convert()
}

# game info
STAGE_STRUCTURE = ['home', 'options', 'keybinds']  # array for creating reusable back buttons that work universally
# keybinds and their descriptions are automatically placed in the keybinds menu through a for loop

KEYS = [['W / UP ARROW', 'Move up'], ['A / LEFT ARROW', 'Move left'], ['S / DOWN ARROW', 'Move down'],
        ['D / RIGHT ARROW', 'Move right'], ['SHIFT', 'Slows down the player and displays hitbox'],
        ['ESC', 'Go back/Pause the game'], ['Z', 'Shoot the bullet']]  # iterable 2d array
# which is used to create keybinds screen

KEY_ARRAY = [[50, 270 + (i * 40), KEYS[i][0], 32, FONT, WHITE] for i in range(len(KEYS))]  # generates list of values to
# be iterated through when placing key text

INFO_ARRAY = [[winx - 50, 270 + (i * 40), KEYS[i][1], 32, FONT, WHITE] for i in range(len(KEYS))]  # ... key info
