import os
from typing import TYPE_CHECKING, override

import pygame

from .credits import CreditsFr
from .editor import EditorHome
from .options import Options
from .popup import PopupLink
from .stage1 import Stage1
from .state import State
from .modules.img import Img
from .modules.btn import BtnImg, BtnTxt
from .modules.txt import Txt

# avoids relative import error while making pycharm happy
# (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class Title(State):
    def __init__(self, game: 'Game'):
        """
        Class for displaying the title screen.
        Can be loaded in and out of the state stack.
        Back button leads to options state.

        Args:
            game: Class that runs the game.
        """
        super().__init__(game)
        # preload stage1 here since for some reason initialising it lags
        self.stage1 = Stage1(self.game)

        # surfaces
        self.backdrop = pygame.image.load(
            os.path.join(self.game.background_dir, 'menu.png')
        ).convert()
        if game.YIPEE < 950:  # 0.005%
            self.logo_img = Img(
                (self.game.WINX / 2, self.game.WINY / 2 * 0.55),
                pygame.image.load(os.path.join(
                    self.game.title_dir, 'logo.png')).convert(),
                scale=4
            )
        else:
            self.logo_img = Img(
                (self.game.WINX / 2, self.game.WINY / 2 * 0.55),
                pygame.image.load(os.path.join(
                    self.game.title_dir, 'logoo.png')).convert(),
                scale=4
            )

        # buttons
        self.btn_play = BtnTxt(
            self.game, (self.game.WINX / 2, self.game.WINY / 2),
            300, 75, 'Play', self.play, font_size=64
        )
        self.btn_editor = BtnTxt(
            self.game, (self.game.WINX / 2, self.btn_play.rect.bottom + 15),
            300, 75, 'Editor', lambda: self.switch_state(EditorHome),
            btn_allign='midtop', font_size=64
        )
        self.btn_options = BtnTxt(
            self.game, (self.game.WINX / 2, self.btn_editor.rect.bottom + 15),
            300, 75, 'Options', lambda: self.switch_state(Options),
            btn_allign='midtop', font_size=64
        )
        self.btn_quit = BtnTxt(
            self.game, (self.game.WINX / 2, self.btn_options.rect.bottom + 15),
            300, 75, 'Quit', self.game.on_quit, btn_allign='midtop',
            font_size=64
        )
        self.btn_github = BtnImg(
            self.game, (0, self.game.WINY), 50, 50,
            pygame.image.load(os.path.join(self.game.icon_dir, 'github.png'))
            .convert_alpha(), btn_allign='bottomleft', scale=2,
            func=lambda: self.switch_state(
                PopupLink, 'https://github.com/r5nnn/shmup')
        )
        self.btn_trello = BtnImg(
            self.game, (self.btn_github.rect.right * 1.1, self.game.WINY),
            50, 50, pygame.image.load(
                os.path.join(self.game.icon_dir, 'trello.png')).convert_alpha(),
            btn_allign='bottomleft', scale=2, func=lambda: self.switch_state(
                PopupLink, 'https://trello.com/b/xCHQx3Uu/shmup-trello')
        )
        self.btn_credits = BtnImg(
            self.game, (self.btn_github.rect.right * 2.2, self.game.WINY),
            50, 50, pygame.image.load(
                os.path.join(self.game.icon_dir, 'credits.png'))
            .convert_alpha(), btn_allign='bottomleft', scale=2,
            func=lambda: self.switch_state(CreditsFr))

        # text
        self.ver_txt = Txt(
            (self.game.WINX, self.game.WINY), self.game.game_ver,
            allign='bottomright', size=32
        )

        self.objects = [
            [self.logo_img, self.ver_txt],
            [self.btn_play, self.btn_editor, self.btn_options, self.btn_quit,
             self.btn_github, self.btn_trello, self.btn_credits]
        ]

    @override
    def enter_state(self) -> None:
        """
        Registers click detection for all the buttons,
        starts playing title music.
        """
        super().enter_state()
        self.game.playing = False
        self.game.bgm.play_audio("menuloop", loops=-1)

    @override
    def back(self, play_sfx: bool = True):
        """Opens the options screen and plays the click audio."""
        self.game.btn_sfx.play_audio('click', override=True) \
            if play_sfx else None
        self.switch_state(Options)

    def play(self) -> None:
        """
        Enters stage1 without using self.switch_state since that loads
        the state in the gameloop which causes lag.
        Instead stage1 is loaded upon the title being loaded.
        """
        self.stage1.enter_state()
