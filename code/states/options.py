"""Used for anything related to the options state"""
import os
from typing import TYPE_CHECKING

import pygame

from .modules.eventmanager import generalEventManager
from .state import State
from .modules.btn import Btn, BtnBack
from .modules.img import Img
from .keybinds import Keybinds

# avoids relative import error while making pycharm happy (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class Options(State):
    def __init__(self, game: 'Game', prev_state: State):
        """Initialises Options with parent class State

        Assigns backdrop to whatever was used in the previous state and creates all the surfaces to display.

        Args:
            prev_state: Previous State in the state stack, used for inheriting properties e.g. backgrounds

        For additional info on args, view help on parent class State.
        """
        super().__init__(game)
        self.backdrop = prev_state.backdrop  # copy backdrop of previous screen

        # surface
        self.img_options = Img(self.game.WINX / 2, self.game.WINY / 2 * 0.4,
                               pygame.image.load(os.path.join(self.game.title_dir, 'options.png')).convert_alpha(),
                               scale=4)

        # buttons
        self.btn_keybinds = Btn(self.game, 36, self.game.WINX/2, self.img_options.rect.bottom * 1.03, 205, 50,
                                'Keybinds', self.keybinds, btn_ref='midtop')
        self.btn_back = BtnBack(self.game, 32, self.game.WINX/2, self.btn_keybinds.rect.bottom * 1.03, 205, 50,
                                btn_ref='midtop')

        # append objects to list for iteration
        self.objects = [self.img_options, self.btn_keybinds, self.btn_back]

    def on_enter(self) -> None:
        for i in [self.btn_keybinds, self.btn_back]:
            generalEventManager.register(pygame.MOUSEBUTTONDOWN, i.on_click)
            generalEventManager.register(pygame.MOUSEBUTTONUP, i.on_release)

    def on_exit(self) -> None:
        for i in [self.btn_keybinds, self.btn_back]:
            generalEventManager.deregister(pygame.MOUSEBUTTONDOWN, i.on_click)
            generalEventManager.deregister(pygame.MOUSEBUTTONUP, i.on_release)

    def keybinds(self) -> None:
        """Creates and appends Keybinds state to the top of the state stack."""
        self.on_exit()
        new_state = Keybinds(self.game, self.game.state_stack[-1])
        new_state.enter_state()
        new_state.on_enter()

    def render_state(self, surface: pygame.Surface) -> None:
        if self.game.playing:
            self.prev_state.prev_state.render_state(surface)  # prev state of prev state is Stage1
        super().render_state(surface)
