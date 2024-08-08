#!/usr/bin/env python3
# pylint: disable=missing-module-docstring
# code wraps at 160

import os
import random
import sys

from operator import attrgetter

import pygame

from states.title import Title
from states.options import Options
from states.paused import Paused
from states.modules.eventmanager import generalEventManager, keyEventManager
from states.modules.audio import Audio


class Game:
    """
    Attributes:
        SCREENX: Width of display
        SCREENY: Height of display.
        WINX: Width of game window.
        WINY: Height of game window.
        YIPEE: Random number that triggers random events, only changes on full restart of game.
        FPS: FPS cap of game.
    """
    pygame.mixer.pre_init(75100, channels=8)  # frequency, size, channels and buffer of audio
    # initialise all pygame classes
    pygame.init()
    SCREENX, SCREENY = pygame.display.Info().current_w, pygame.display.Info().current_h
    WINX, WINY = SCREENX, SCREENY
    YIPEE = random.randint(1, 1000)
    FPS = 165

    def __init__(self):
        """Initialises Game and pygame.

        Defines attributes to use while game is running."""

        # default surface image
        self.backdrop = pygame.Surface((Game.WINX, Game.WINY))  # blit to here and NOT to self.screen:
        # backdrop is blitted to screen

        # other variables
        self.game_ver = "running version 0.0.2"
        self.clock = pygame.time.Clock()
        self.vsync = 0
        self.dt_res = 8
        self.dt, self.prev_time = 0, 0
        self.state_stack = []
        self.screen = pygame.display.set_mode((self.WINX, self.WINY), pygame.NOFRAME, pygame.SCALED,
                                              vsync=self.vsync)  # creates display surface, pygame.NOFRAME makes the
        # window borderless and pygame.SCALED means any textures are scaled proportional to window size
        self.screen_rect = self.screen.get_rect()  # get_rect() returns rect of size of surface given
        self.pressed_keys = []
        self.relevant_keys = [pygame.K_ESCAPE, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                              pygame.K_LSHIFT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]

        self.load_assets()  # updates surface images and directories with correct file paths
        pygame.display.set_caption("shmup alpha " + self.game_ver)
        pygame.display.set_icon(self.win_icon)

        # load audio channels
        self.bgm = Audio()
        self.bgm.add_audio(self.menu_music)
        self.bgm.add_audio(self.stage1_music)
        self.bgm.set_volume(0.2)
        self.btn_sfx = Audio()
        self.btn_sfx.add_audio(self.click_btn_sfx_dir)
        self.btn_sfx.set_volume(0.2)
        self.bullet_sfx = Audio()
        self.bullet_sfx.set_volume(0.05)
        self.bullet_sfx.add_audio(self.bullet_sfx_dir)
        self.player_sfx = Audio()
        self.enemy_sfx = Audio()
        self.enemy_sfx.set_volume(0.1)
        self.enemy_sfx.add_audio(self.enemy_die_sfx)

        self.load_states()  # update all screens with correct objects and loads first screen into stack (title)

        # register all global input handlers
        generalEventManager.register(pygame.QUIT, self.on_quit)
        generalEventManager.register(pygame.KEYDOWN, self.on_keydown)
        keyEventManager.register(pygame.K_END, self.on_quit)
        keyEventManager.register(pygame.K_ESCAPE, self.back)

        self.running, self.playing, self.debug = True, False, False

    def gameloop(self) -> None:
        """loops through and runs game"""
        while self.running:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()
        self.on_quit()

    def get_events(self) -> None:
        """handles user input"""
        self.pos = pygame.mouse.get_pos()
        self.keys = pygame.mouse.get_pressed()
        self.pressed_keys.remove(pygame.MOUSEBUTTONUP) if pygame.MOUSEBUTTONUP in self.pressed_keys else None
        self.pressed_keys.remove("pygame.MOUSEBUTTONDOWN") if "pygame.MOUSEBUTTONDOWN" in self.pressed_keys else None

        for event in pygame.event.get():

            generalEventManager.notify(event)

            match event.type:
                case pygame.KEYDOWN:
                    if event.key in self.relevant_keys:
                        self.pressed_keys.append(event.key)

                case pygame.KEYUP:
                    # ditto
                    if event.key in self.relevant_keys:
                        self.pressed_keys.remove(event.key)

    def update(self) -> None:
        """updates top item in stack"""
        self.state_stack[-1].update_state()

    def render(self) -> None:
        """renders top item in stack"""
        self.state_stack[-1].render_state(self.backdrop)  # renders top item in the stack
        self.screen.blit(pygame.transform.scale(self.backdrop, (self.SCREENX, self.SCREENY)), (0, 0))  # blits
        # backdrop to 0, 0 on screen, which is the main surface displaying everything
        pygame.display.update()  # update game window
        self.clock.tick(Game.FPS)  # sets fps cap

    def get_dt(self) -> None:
        """calculates delta time"""
        now = pygame.time.get_ticks() / 1000
        self.dt = round(now - self.prev_time, self.dt_res)
        self.prev_time = now

    def load_assets(self) -> None:
        """create pointers to directories"""
        os.chdir("..")  # move up a directory

        # ..\shmup\

        self.assets_dir = os.path.join("assets")  # ..\assets

        self.textures_dir = os.path.join(self.assets_dir, "textures")  # assets\textures
        self.title_dir = os.path.join(self.textures_dir, "title")  # assets\textures\title
        self.icon_dir = os.path.join(self.textures_dir, "icon")  # assets\textures\title\icon
        self.win_icon = pygame.image.load(os.path.join(self.icon_dir, "shmup.png")).convert()  # ..\title.png
        self.background_dir = os.path.join(self.textures_dir, "background")  # assets\textures\background
        self.player_dir = os.path.join(self.textures_dir, "player")  # assets\textures\player
        self.bullet_dir = os.path.join(self.textures_dir, "bullet")  # assets\textures\bullet
        self.enemy_dir = os.path.join(self.textures_dir, "enemy")  # assets\textures\enemy

        self.fonts_dir = os.path.join(self.assets_dir, "fonts")  # assets\fonts
        self.font_dir = os.path.join(self.fonts_dir, "editundo.ttf")  # ..\editundo.ttf

        self.music_dir = os.path.join(self.assets_dir, "music")  # assets\music
        self.menu_dir = os.path.join(self.music_dir, "menu")  # assets\music\menu
        self.menu_music = os.path.join(self.menu_dir, "menuloop.wav")  # assets\music\menu
        self.game_dir = os.path.join(self.music_dir, "game")  # assets\music\menu\game
        self.stage1_music = os.path.join(self.game_dir, "stage1.wav")  # assets\music\menu\game
        self.sfx_dir = os.path.join(self.music_dir, "sfx")  # assets\music\sfx
        self.click_btn_sfx_dir = os.path.join(self.sfx_dir, "click.wav")  # ..\click.wav
        self.bullet_sfx_dir = os.path.join(self.sfx_dir, "shoot.wav")  # ..\shoot.wav
        self.player_die_sfx_dir = os.path.join(self.sfx_dir, "player_die.wav")  # ..\player_die.wav
        self.enemy_die_sfx = os.path.join(self.sfx_dir, "enemy_die.wav")  # ..\enemy_die.wav

    def load_states(self) -> None:
        """loads first state"""
        self.title_screen = Title(self)
        self.title_screen.enter_state()
        self.title_screen.on_enter()

    def on_quit(self) -> None:
        pygame.quit()
        try:
            sys.exit()
        finally:
            self.running = False

    def back(self, play_sfx=True) -> None:
        """Pops top item out of state stack.

        Enters options if in the title screen, and pauses the game if ingame."""
        self.btn_sfx.force_play_audio('click') if play_sfx else None
        self.state_stack[-1].on_exit()
        if (not self.playing or len(self.state_stack) != 2) and len(self.state_stack) > 1:
            self.state_stack[-1].exit_state()
            self.state_stack[-1].on_enter()
        elif self.playing:
            paused = Paused(self)
            paused.enter_state()
            paused.on_enter()
        else:
            options = Options(self)
            options.enter_state()
            options.on_enter()

    @staticmethod
    def on_keydown(event) -> None:
        """Triggers on keypress, calls key handler."""
        keyEventManager.notify(event, selector=attrgetter("key"))


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.gameloop()
