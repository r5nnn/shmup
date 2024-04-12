"""Used for anything related to the keybinds state"""
import os
from typing import TYPE_CHECKING

import pygame

from .modules.eventmanager import generalEventManager
from .state import State
from .modules.txt import Txt
from .modules.btn import Btn, BtnBack
from .modules.img import Img

# avoids relative import error while making pycharm happy (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class Keybinds(State):

    def __init__(self, game: 'Game', prev_state: State):
        """Initialises Keybinds with parent class State

        Assigns backdrop to whatever was used in the previous state and creates all the surfaces to display. Iterates through all relevant keybinds and
        generates the UI.

        Args:
            prev_state: Previous State in the state stack, used for inheriting properties e.g. backgrounds

        For additional info on args, view help on parent class State.
        """
        super().__init__(game)
        self.backdrop = prev_state.backdrop  # copy backdrop of previous screen
        # surface
        self.img_keybinds = Img(self.game.WINX / 2, self.game.WINY / 2 * 0.2, pygame.image.load(os.path.join(self.game.title_dir, 'keybinds.png')).convert(),
                                scale=4)

        # text
        self.txt_keys = Txt(self.game.font_dir, 64, self.game.WINX * 0.02, self.img_keybinds.rect.bottom, 'Keys')
        self.txt_description = Txt(self.game.font_dir, 64, self.game.WINX - self.game.WINX * 0.02, self.img_keybinds.rect.bottom, 'Description', ref='topright')

        # buttons
        self.btn_back = BtnBack(self.game, 64, self.game.WINX - self.game.WINX * 0.02, self.img_keybinds.rect.centery, 250, 75, btn_ref='midright')
        self.btn_modify = Btn(self.game, 64, self.game.WINX * 0.02, self.img_keybinds.rect.centery, 250, 75, 'Modify', btn_ref='midleft')

        self.keys = [['--General--', ''], ['ESC', 'Go back/Pause the game'], ['END', 'Force quit game'], ['Z', 'Shoot the bullet'],
                     ['--Game--', ''], ['W / UP ARROW', 'Move up'], ['A / LEFT ARROW', 'Move left'], ['S / DOWN ARROW', 'Move down'],
                                       ['D / RIGHT ARROW', 'Move right'], ['SHIFT', 'Slows down the player and displays hitbox']]

        # append all objects to one list for iterating through
        self.objects = ([self.img_keybinds, self.txt_keys, self.txt_description, self.btn_back, self.btn_modify] +
                        [Txt(self.game.font_dir, 32, self.game.WINX * 0.02, self.img_keybinds.rect.bottom * 1.4 + (i * 40),
                             self.keys[i][0])  # generates Txt surface objects for each keybind in self.keys
                         for i in range(len(self.keys))] +
                        [Txt(self.game.font_dir, 32, self.game.WINX - self.game.WINX * 0.02, self.img_keybinds.rect.bottom * 1.4 + (i * 40),
                             self.keys[i][1], ref='topright')  # generates Txt surface objects for each keybind description in self.keys
                         for i in range(len(self.keys))])

    def on_enter(self) -> None:
        for i in [self.btn_back, self.btn_modify]:
            generalEventManager.register(pygame.MOUSEBUTTONDOWN, i.on_click)
            generalEventManager.register(pygame.MOUSEBUTTONUP, i.on_release)

    def on_exit(self) -> None:
        for i in [self.btn_modify, self.btn_back]:
            generalEventManager.deregister(pygame.MOUSEBUTTONDOWN, i.on_click)
            generalEventManager.deregister(pygame.MOUSEBUTTONUP, i.on_release)
    
    def render_state(self, surface: pygame.Surface) -> None:
        if self.game.playing:
            self.prev_state.prev_state.prev_state.render_state(surface)  # prev state of prev state of prev state is Stage1
        super().render_state(surface)