import sys
from classes.img_ import Img
from classes.bullet import Bullet
from classes.txt import Txt
from classes.btn import Btn
from classes.player import Player
from classes.enemy import Enemy
from constants import *

# Initialise game assets and variables
pygame.init()

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


def cmd(name):
    """
    call this method to update the stage of the screen
    :param name: the stage you want to switch to
    """
    global STAGE, main
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

ENEMY_ARRAY = [Enemy(i[0], i[1], i[2], i[3]) for i in ENEMY_ARRAY]
for i in ENEMY_ARRAY:
    enemies.add(i)  # noqa

windll.user32.SetCursorPos(screenx // 2, screeny // 2)

pygame.time.set_timer(1, 1000)

# Game Mainloop

while RUN:
    screen.blit(BACKDROP, BACKDROP_COORDS)  # noqa
    events = pygame.event.get()
    for event in events:  # iterates through inputs checking if they match the exit event
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False

            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        sfx.play(CLICK)
                        match STAGE:
                            case 'home':
                                cmd('options')
                            case 'game':
                                cmd('paused')
                            case _:
                                cmd('back')

    if pygame.key.get_pressed()[pygame.K_z]:
        current_time = pygame.time.get_ticks()
        if current_time - previous_time[0] > 100:
            previous_time[0] = current_time
            sfx.play(SHOOT)
            bulletp = Bullet(player.rect.center[0], player.rect.y, BULLETS['player'], ENEMY['idlemask'], 16)
            player_bullets.add(bulletp)  # noqa
            player_bullets.update('player')

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
            enemies.draw(screen)
            enemies.update(screen)
            player_bullets.draw(screen)
            player_bullets.update('player')
            player.update(screen)
            hit_list = pygame.sprite.groupcollide(enemies, player_bullets, False, False)
            for enemy in hit_list:
                enemy.kill()
            BACKDROP = pygame.image.load('assets\\textures\\background\\stage.png').convert()

    mouse = pygame.mouse.get_pos()  # stores the (x,y) coordinates into the variable as a tuple
    pygame.display.flip()  # update the BACKDROP surface onto the window
    clock.tick(fps)  # update the clock with the delay of the refresh rate
