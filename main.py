import sys
from img_ import Img
from bullet import Bullet
from txt import Txt
from btn import Btn
from player import Player
from constants import *

# Initialise game assets and variables
pygame.init()

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

# game info
STAGE_STRUCTURE = ['home', 'options', 'keybinds']  # array for creating reusable back buttons that work universally
# keybinds and their descriptions are automatically placed in the keybinds menu through a for loop
KEYS = [['W / UP ARROW', 'Move up'], ['A / LEFT ARROW', 'Move left'], ['S / DOWN ARROW', 'Move down'],
        ['D / RIGHT ARROW', 'Move right'], ['SHIFT', 'Slows down the player and displays hitbox'],
        ['ESC', 'Go back/Pause the game']]  # iterable 2d array
# which is used to create keybinds screen
KEY_ARRAY = [[50, 270 + (i * 40), KEYS[i][0], 32, FONT, WHITE] for i in range(len(KEYS))]  # generates list of values to
# be iterated through when placing key text
INFO_ARRAY = [[winx - 50, 270 + (i * 40), KEYS[i][1], 32, FONT, WHITE] for i in range(len(KEYS))]  # ... key info

# status
STAGE = 'home'
RUN = True
INGAME = False

# window settings
pygame.display.set_caption('shmup alpha 0.0.1')
pygame.display.set_icon(ICON)

# window background
BACKDROP_COORDS = screen.get_rect()  # get_rect() returns coordinates of surface

# game speed
fps = 330
clock = pygame.time.Clock()
previous_time = pygame.time.get_ticks()


def cmd(name):
    """
    call this method to update the stage of the screen
    :param name: the stage you want to switch to
    """
    global STAGE, STAGE_STRUCTURE, main
    match name:
        case 'back':
            # different stage structure if you're ingame
            if INGAME:
                STAGE_STRUCTURE.insert(1, 'paused')  # adds in a paused screen into the structure
                STAGE_STRUCTURE_POINTER = STAGE_STRUCTURE.index(STAGE)  # grabs index of current stage
                STAGE_STRUCTURE[0] = 'game'  # STAGE_STRUCTURE[0] is usually home (main menu screen)
                if STAGE_STRUCTURE_POINTER != 0:
                    # go back a screen if not on default screen
                    STAGE_STRUCTURE_POINTER = STAGE_STRUCTURE.index(STAGE)
                    STAGE = STAGE_STRUCTURE[STAGE_STRUCTURE_POINTER - 1]
                else:
                    # go forward screen if on default screen
                    STAGE = STAGE_STRUCTURE[STAGE_STRUCTURE_POINTER]
            else:
                STAGE_STRUCTURE_POINTER = STAGE_STRUCTURE.index(STAGE)
                if 'paused' in STAGE_STRUCTURE:
                    STAGE_STRUCTURE.remove('paused')  # no paused screen is needed in the main menu
                STAGE_STRUCTURE[0] = 'home'
                if STAGE_STRUCTURE_POINTER != 0:
                    STAGE = STAGE_STRUCTURE[STAGE_STRUCTURE_POINTER - 1]
                else:
                    STAGE = STAGE_STRUCTURE[STAGE_STRUCTURE_POINTER]
        case 'quit':
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False
        case _:
            STAGE = name


def generate(arr):
    """
    iterates through updates all of the objects provided
    :param arr: objects to be iterated through and updated
    """
    for list1 in arr:
        for listObject in list1:
            if arr.index(list1) == 0:
                listObject.update(screen, events)
            else:
                listObject.update(screen)


# buttons
back_btn = Btn(0, 0, 205, 50, 36, TERTIARY, QUATERNARY, SECONDARY, PRIMARY, 'Back',
               lambda b: cmd('back'), center=(winx / 2, 300))
options_btn = Btn(0, 0, 205, 50, 36, TERTIARY, QUATERNARY, SECONDARY, PRIMARY, 'Options',
                  lambda b: cmd('options'), center=(winx / 2, 225))
keybinds_btn = Btn(0, 0, 205, 50, 36, TERTIARY, QUATERNARY, SECONDARY, PRIMARY, 'Keybinds',
                   lambda b: cmd('keybinds'), center=(winx / 2, 225))
play_btn = Btn(0, 0, 300, 75, 64, TERTIARY, QUATERNARY, SECONDARY, PRIMARY, 'Play',
               lambda b: cmd('game'), center=(winx / 2, winy / 2))
exit_btn = Btn(0, 0, 205, 50, 36, TERTIARY, QUATERNARY, SECONDARY, PRIMARY, 'Exit Game',
               lambda b: cmd('home'), center=(winx / 2, 370))
options1_btn = Btn(0, 0, 300, 75, 64, TERTIARY, QUATERNARY, SECONDARY, PRIMARY, 'Options',
                   lambda b: cmd('options'), center=(winx / 2, winy / 2 + 100))
quit_btn = Btn(0, 0, 300, 75, 64, TERTIARY, QUATERNARY, SECONDARY, PRIMARY, 'Quit',
               lambda b: cmd('quit'), center=(winx / 2, winy / 2 + 200))

# display text
paused_txt = Txt(0, 0, 'Paused', 64, FONT, WHITE, center=(winx / 2, 150))
options_txt = Txt(0, 0, 'Options', 64, FONT, WHITE, center=(winx / 2, 150))
keybinds_txt = Txt(0, 0, 'Keybinds', 64, FONT, WHITE, center=(winx / 2, 150))
keybindsKEY_ARRAY_txt = Txt(50, 200, 'Keys', 48, FONT, WHITE)
keybindsInfo_txt = Txt(winx - 50, 200, 'Description', 48, FONT, WHITE, pos='right')
KEY_ARRAY = [Txt(i[0], i[1], i[2], i[3], i[4], i[5]) for i in KEY_ARRAY]
INFO_ARRAY = [Txt(i[0], i[1], i[2], i[3], i[4], i[5], pos='right') for i in INFO_ARRAY]

# images
logo_img = Img(0, 0, LOGO, center=(winx / 2, winy / 2 - 200))

# 2d array of objects for each screen for easy initialising of text and button objects with for loop
# first list contains buttons, while second list contains text
home = [[play_btn, options1_btn, quit_btn], [logo_img]]
paused = [[back_btn, exit_btn, options_btn], [paused_txt]]
options = [[keybinds_btn, back_btn], [options_txt]]
keybinds = [[], [keybinds_txt, keybindsKEY_ARRAY_txt, keybindsInfo_txt]]

# game objects
player = Player(winx / 2, winy / 2, PLAYER, 6, 3)

# sprite groups
bullets = pygame.sprite.Group()

windll.user32.SetCursorPos(screenx // 2, screeny // 2)

# Game Mainloop

while RUN:
    screen.blit(BACKDROP, BACKDROP_COORDS)  # noqa
    events = pygame.event.get()
    for event in events:  # iterates through inputs checking if they match the exit event
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_ESCAPE:
                    CLICK.play()
                    match STAGE:
                        case 'home':
                            cmd('options')
                        case 'game':
                            cmd('paused')
                        case _:
                            cmd('back')

    if pygame.key.get_pressed()[pygame.K_z]:
        current_time = pygame.time.get_ticks()
        if current_time - previous_time > 100:
            previous_time = current_time
            bullet = Bullet(player.rect.center[0], player.rect.y, BULLETS['player'], 16)
            bullets.add(bullet)  # noqa
            bullets.update()

    # match case statement to toggle between multiple stages when navigating menus and options
    match STAGE:
        case 'home':
            INGAME = False
            BACKDROP = pygame.image.load('assets\\textures\\background\\menu.png').convert()
            if song.get_busy():
                song.fadeout(100)
            if not bg.get_busy():
                bg.play(MENULOOP, loops=-1, fade_ms=1000)
            generate(home)
        case 'paused':
            generate(paused)
        case 'options':
            generate(options)
        case 'keybinds':
            generate(keybinds)
            for i in KEY_ARRAY:
                i.update(screen)
            for i in INFO_ARRAY:
                i.update(screen)
        case 'game':
            INGAME = True
            bg.fadeout(500)
            if not song.get_busy():
                song.play(GAME1, loops=-1, fade_ms=1000)
            bullets.draw(screen)
            bullets.update()
            player.update(screen)
            BACKDROP = pygame.image.load('assets\\textures\\background\\stage.png').convert()

    mouse = pygame.mouse.get_pos()  # stores the (x,y) coordinates into the variable as a tuple
    pygame.display.flip()  # update the BACKDROP surface onto the window
    clock.tick(fps)  # update the clock with the delay of the refresh rate
