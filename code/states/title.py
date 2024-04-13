"""Handles the title screen"""
import sys
import os
import webbrowser
from typing import TYPE_CHECKING, override

import pygame

from .modules.eventmanager import generalEventManager
from .options import Options
from .popup import Popup
from .stage1 import Stage1
from .state import State
from .modules.img import Img
from .modules.btn import BtnImg, BtnTxt
from .modules.txt import Txt

# avoids relative import error while making pycharm happy (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class Title(State):
    def __init__(self, game: 'Game'):
        """Uses parent State. Creates all the object to display."""
        super().__init__(game)
        self.stage1 = Stage1(self.game)  # load stage1 here since for some reason loading it when clicking a button lags

        # surfaces
        self.backdrop = pygame.image.load(os.path.join(self.game.background_dir, 'menu.png')).convert()
        if game.YIPEE < 999:  # 1/1000
            self.logo_img = Img(self.game.WINX / 2, self.game.WINY / 2 * 0.55,
                                pygame.image.load(os.path.join(self.game.title_dir, 'logo.png')).convert(), scale=4)
        else:
            self.logo_img = Img(self.game.WINX / 2, self.game.WINY / 2 * 0.55,
                                pygame.image.load(os.path.join(self.game.title_dir, 'logoo.png')).convert(), scale=4)

        # buttons
        self.btn_play = BtnTxt(self.game, 64, self.game.WINX / 2, self.game.WINY / 2, 300, 75, 'Play', self.play)
        self.btn_options = BtnTxt(self.game, 64, self.game.WINX / 2, self.btn_play.rect.bottom * 1.02, 300, 75, 'Options', self.options, btn_ref='midtop')
        self.btn_quit = BtnTxt(self.game, 64, self.game.WINX / 2, self.btn_options.rect.bottom * 1.02, 300, 75, 'Quit', self.quit, btn_ref='midtop')
        self.btn_github = BtnImg(self.game, 0, self.game.WINY, 50, 50,
                                 pygame.image.load(os.path.join(self.game.icon_dir, "github.png")).convert_alpha(),
                                 btn_ref='bottomleft', scale=2, func=self.github)
        self.btn_trello = BtnImg(self.game, self.btn_github.rect.right * 1.1, self.game.WINY, 50, 50,
                                 pygame.image.load(os.path.join(self.game.icon_dir, "trello.png")).convert_alpha(), btn_ref='bottomleft', scale=2,
                                 func=self.trello)
        self.btn_info = BtnImg(self.game, self.btn_github.rect.right * 2.2, self.game.WINY, 50, 50,
                               pygame.image.load(os.path.join(self.game.icon_dir, "info.png")).convert_alpha(), btn_ref='bottomleft', scale=2)

        # text
        self.ver_txt = Txt(self.game.font_dir, 32, self.game.WINX, self.game.WINY, self.game.game_ver,
                           ref='bottomright')

        self.objects = [self.logo_img, self.ver_txt, self.btn_play, self.btn_options, self.btn_quit, self.btn_github, self.btn_trello, self.btn_info]

        self.bgm = pygame.mixer.Sound(file=self.game.menu_music)  # make sure to keep file=self.filepath as stated by the pygame docs:
        # From https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound: A Unicode string can only be a file pathname. A bytes object can be either a
        # pathname or a buffer object. Use the 'file' or 'buffer' keywords to
        self.bgm.set_volume(0.2)
        # avoid ambiguity; otherwise Sound may guess wrong.

    @override
    def on_enter(self) -> None:
        """Registers click detection for all the buttons, starts playing title music."""
        for i in [self.btn_options, self.btn_play, self.btn_quit, self.btn_github, self.btn_trello, self.btn_info]:
            generalEventManager.register(pygame.MOUSEBUTTONDOWN, i.on_click)
            generalEventManager.register(pygame.MOUSEBUTTONUP, i.on_release)
        self.game.playing = False
        pygame.mixer.Channel(2).fadeout(1000)
        if not self.game.channel_bgm.get_busy():
            self.game.channel_bgm.play(self.bgm, loops=-1, fade_ms=4000)

    @override
    def on_exit(self) -> None:
        """Deregisters all of the click detection done by EventManager for all of the buttons."""
        for i in [self.btn_options, self.btn_play, self.btn_quit, self.btn_github, self.btn_trello, self.btn_info]:
            generalEventManager.deregister(pygame.MOUSEBUTTONDOWN, i.on_click)
            generalEventManager.deregister(pygame.MOUSEBUTTONUP, i.on_release)

    def options(self) -> None:
        """Calls the exit method of Title, Creates and appends Options state to the top of the state stack and calls its on enter method."""
        self.on_exit()
        new_state = Options(self.game, self.game.state_stack[-1])
        new_state.on_enter()
        new_state.enter_state()

    def play(self) -> None:
        """Calls the exit method of Title, the enter method of Stage1 and appends the Stage1 state to the top of the state stack."""
        self.on_exit()
        self.stage1.on_enter()
        self.stage1.enter_state()

    def quit(self) -> None:
        """Attempts to quit the game via pygame, sys and stopping the game mainloop."""
        pygame.quit()
        try:
            sys.exit()
        finally:
            self.game.running = False

    def github(self) -> None:
        popup = Popup(self.game, 'Open https://github.com/r5nnn/shmup in your browser?', 'Open', 'Cancel', self.github_click)
        self.on_exit()
        popup.enter_state()
        popup.on_enter()

    def github_click(self) -> None:
        webbrowser.open("https://github.com/r5nnn/shmup")
        self.game.back(play_sfx=False)

    def trello(self) -> None:
        popup = Popup(self.game, 'Open https://trello.com/b/xCHQx3Uu/shmup-trello in your browser?', 'Open', 'Cancel', self.trello_click)
        self.on_exit()
        popup.enter_state()
        popup.on_enter()

    def trello_click(self) -> None:
        webbrowser.open("https://trello.com/b/xCHQx3Uu/shmup-trello")
        self.game.back(play_sfx=False)