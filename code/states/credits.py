import os

import pygame

from .modules.btn import BtnBack, BtnTxt
from .modules.surfaces import Img
from .modules.txt import Txt
from .state import State
from typing import TYPE_CHECKING, override

# avoids relative import error while making pycharm happy
# (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class CreditsFr(State):
    def __init__(self, game: "Game"):
        super().__init__(game)
        # surface
        self.img_credits = Img(
            (self.game.WINX / 2, self.game.WINY / 2 * 0.2),
            pygame.image.load(
                os.path.join(self.game.title_dir, 'credits.png')
            ).convert(),
            scale=4)

        # buttons
        self.btn_credits = BtnTxt(
            self.game,
            (self.game.WINX / 2 * 1.025, self.game.WINY * 0.98),
            250, 75,
            'actual credits',
            lambda: self.switch_state(Credits),
            font_size=34,
            btn_allign="bottomleft")
        self.btn_back = BtnBack(
            self.game,
            (self.game.WINX / 2 * 0.975, self.game.WINY * 0.98),
            250, 75,
            font_size=64,
            btn_allign="bottomright")

        # text
        self.txt_credits = Txt(
            (self.game.WINX / 2, self.img_credits.img_rect.bottom * 1.1),
            'Gameplay Programmer:\nRene Timantsev\n\nLead Graphical Designer:'
            '\nRene Timantsev\n\nSound Designer:\nRene Timantsev\n\n'
            'Sprite Artist:\nRene Timantsev\n\nGame Designer:\nRene Timantsev'
            '\n\nWriting/Narrative design:\nRene Timantsev\n\nMarketing '
            'Executive:\nRene Timantsev\n\nQuality Assurance:\nRene Timantsev'
            '\n\nGame Tester:\nRene Timantsev',
            size=32,
            allign="midtop",
            wrap_width=self.game.WINX * 0.75
        )

        self.objects = [
            [self.img_credits, self.txt_credits],
            [self.btn_credits, self.btn_back]
        ]

    @override
    def render_state(self, surface: pygame.Surface) -> None:
        self.backdrop = self.prev_state.backdrop
        super().render_state(surface)


class Credits(State):
    def __init__(self, game):
        super().__init__(game)
        # button
        self.btn_back = BtnBack(
            self.game,
            (self.game.WINX/2, self.game.WINY * 0.98),
            250, 75,
            font_size=64,
            btn_allign='midbottom')

        # text
        self.txt_credits = Txt(
            (self.game.WINX/2, self.game.WINY*0.05),
            'Font used:\nEdit Undo BRK (© ÆNIGMA FONTS kentpw@norwich.net)\n\n'
            'Sprite editor used:\nAseprite (paid, or build yourself from '
            'https://github.com/aseprite/aseprite)\n\nMusic:\n'
            'Main menu - Oneiros of Borehole Planet · HOYO-MiX · © 2024 miHoYo'
            '\nStage 1 - Moisture Deficit · Chris Christodoulou · © 2013 Chris '
            'Christodoulou\n\nPlaytesters:\nNone ;( but Dom banzz and Chris '
            'when I force them\n\nSpecial thanks:\nChristof, Milo, Oscar x2, '
            'James, Carlos, the one piece\n\nAnd finally:\nThank you for '
            'playing <3\n\n\n\n\n\n(rate the rizz cmon thats like a 10)',
            size=32,
            allign='midtop',
            wrap_width=self.game.WINX*0.75
        )
        self.objects = [[self.txt_credits], [self.btn_back]]

    @override
    def render_state(self, surface: pygame.Surface) -> None:
        self.backdrop = self.prev_state.backdrop
        super().render_state(surface)