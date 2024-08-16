import os
from typing import TYPE_CHECKING, override

import pygame

from .state import State
from .modules.txt import Txt
from .modules.btn import BtnTxt, BtnBack
from .modules.img import Img

# avoids relative import error while making pycharm happy
# (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class Keybinds(State):
    def __init__(self, game: 'Game'):
        """
        Class for displaying the keybinds screen.
        Assigns backdrop to whatever was used in the previous state and creates
        all the surfaces to display.
        Iterates through all relevant keybinds and generates the UI.

        Args:
            game: Class that runs the game.
        """
        super().__init__(game)
        if self.game.playing:
            # darkens the background by using a 50% opacity rectangle covering
            # the entire screen
            self.rect = pygame.Rect(0, 0, self.game.WINX, self.game.WINY)
            # create surface compatible with modifying alpha
            self.rect_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            self.rect_surf.set_alpha(128)  # half opacity
            # draw rectangle onto surface
            pygame.draw.rect(self.rect_surf, (0, 0, 0), self.rect)

        # surface
        self.img_keybinds = Img(
            (self.game.WINX / 2, self.game.WINY / 2 * 0.2),
            pygame.image.load(os.path.join(self.game.title_dir, 'keybinds.png'))
            .convert(), scale=4
        )

        # text
        self.txt_keys = Txt(
            (self.game.WINX * 0.02, self.img_keybinds.img_rect.bottom),
            'Keys', size=64
        )
        self.txt_description = Txt(
            (self.game.WINX - self.game.WINX * 0.02,
             self.img_keybinds.img_rect.bottom),
            'Description', allign='topright', size=64
        )

        # buttons
        self.btn_back = BtnBack(
            self.game, (self.game.WINX - self.game.WINX * 0.02,
                        self.img_keybinds.img_rect.centery),
            250, 75, btn_allign='midright', font_size=64
        )
        self.btn_modify = BtnTxt(
            self.game, (self.game.WINX * 0.02,
                        self.img_keybinds.img_rect.centery),
            250, 75, 'Modify', btn_allign='midleft', font_size=64
        )

        self.keys = [
            ['--General--', ''],
            ['ESC', 'Go back/Pause the game'], ['END', 'Force quit game'],
            ['RIGHT CLICK', 'Cancel button click'],
            ['--Game--', ''],
            ['W / UP ARROW', 'Move up'], ['A / LEFT ARROW', 'Move left'],
            ['S / DOWN ARROW', 'Move down'], ['D / RIGHT ARROW', 'Move right'],
            ['SHIFT', 'Slows down the player and displays hitbox']
        ]

        self.objects = [
            [self.img_keybinds, self.txt_keys, self.txt_description],
            [self.btn_back, self.btn_modify]
        ]
        self.objects[0] += (
                [
                    # generates Txt surface for each keybind in self.keys
                    Txt(
                        (self.game.WINX * 0.02,
                         self.img_keybinds.img_rect.bottom * 1.4 + (i * 40)),
                        self.keys[i][0], size=32
                    ) for i in range(len(self.keys))
                ] +
                [
                    # generates Txt surface for each description in self.keys
                    Txt(
                        (self.game.WINX - self.game.WINX * 0.02,
                         self.img_keybinds.img_rect.bottom * 1.4 + (i * 40)),
                        self.keys[i][1], allign='topright', size=32
                    ) for i in range(len(self.keys))
                ]
        )

    @override
    def render_state(self, surface: pygame.Surface) -> None:
        """
        Renders the state to the surface provided.
        Background is used from title screen.

        Args:
            surface: Surface which state will be rendered to.

        """
        if self.game.playing:
            # Stage1
            self.prev_state.prev_state.prev_state.render_state(surface)
            surface.blit(
                self.rect_surf, self.rect_surf.get_rect(
                    center=(self.game.WINX / 2, self.game.WINY / 2)
                )
            )
        else:
            self.backdrop = self.prev_state.backdrop
        super().render_state(surface)
