import os

import pygame

from .modules.btn import BtnBack
from .modules.img import Img
from .state import State
from typing import TYPE_CHECKING

# avoids relative import error while making pycharm happy (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class Credits(State):
    def __init__(self, game: "Game"):
        super().__init__(game)
        # surface
        self.img_credits = Img(self.game.WINX / 2, self.game.WINY / 2 * 0.2, pygame.image.load(os.path.join(self.game.title_dir, 'credits.png')).convert(),
                               scale=4)

        # buttons
        self.btn_back = BtnBack(self.game, 64, self.game.WINX - self.game.WINX * 0.02, self.img_credits.img_rect.centery, 250, 75, btn_ref='midright')

        self.objects = [[self.img_credits], [self.btn_back]]

    def render_state(self, surface: pygame.Surface) -> None:
        self.backdrop = self.prev_state.backdrop
        super().render_state(surface)