import os
from typing import TYPE_CHECKING, override

import pygame

from .state import State
from .modules.btn import BtnTxt, BtnBack
from .modules.img import Img
from .keybinds import Keybinds

# avoids relative import error while making pycharm happy
# (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class Options(State):
    def __init__(self, game: 'Game'):
        """
        Class for displaying the options screen.
        Assigns backdrop to whatever was used in the previous state
        and creates all the surfaces to display.

        Args:
            game: Class that runs the game.
        """
        super().__init__(game)
        if self.game.playing:
            # create window background rect
            self.rect = pygame.Rect(0, 0, self.game.WINX, self.game.WINY)
            # create surface compatible with modifying alpha
            self.rect_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            self.rect_surf.set_alpha(128)  # half opacity
            # draw rectangle onto surface
            pygame.draw.rect(self.rect_surf, (0, 0, 0), self.rect)

        # surface
        self.img_options = Img(
            (self.game.WINX / 2, self.game.WINY * 0.1),
            pygame.image.load(os.path.join(self.game.title_dir, 'options.png'))
            .convert_alpha(), scale=4
        )

        # buttons
        self.btn_keybinds = BtnTxt(
            self.game, (self.game.WINX / 2,
                        self.img_options.img_rect.bottom + 30),
            205, 50, 'Keybinds', lambda: self.switch_state(Keybinds),
            btn_allign='midtop', font_size=32
        )
        self.btn_back = BtnBack(
            self.game, (self.game.WINX/2, self.btn_keybinds.rect.bottom + 10),
            205, 50, btn_allign='midtop', font_size=32
        )

        self.objects = [
            [self.img_options],
            [self.btn_keybinds, self.btn_back]
        ]

    @override
    def render_state(self, surface: pygame.Surface) -> None:
        """
        Renders the state to the surface provided.
        Background is used from title screen if not playing,
        and from stage1 if playing.

        Args:
            surface: Surface which state will be rendered to.
        """
        if self.game.playing:
            # prev state of prev state is Stage1
            self.prev_state.prev_state.render_state(surface)
            surface.blit(
                self.rect_surf, self.rect_surf.get_rect(
                    center=(self.game.WINX / 2, self.game.WINY / 2)
                )
            )
        else:
            self.backdrop = self.prev_state.backdrop
        super().render_state(surface)
