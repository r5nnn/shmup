import os

import pygame

from .modules.btn import BtnBack, BtnTxt
from .modules.eventmanager import generalEventManager
from .modules.img import Img
from .state import State
from .popup import Popup


class EditorHome(State):
    def __init__(self, game):
        super().__init__(game)
        self.img_editor = Img(self.game.WINX / 2, self.game.WINY * 0.1, pygame.image.load(os.path.join(self.game.title_dir, 'editor.png')), scale=4)
        self.btn_new_stage = BtnTxt(self.game, 32, self.game.WINX / 2, self.img_editor.img_rect.bottom + 20, 205, 50, 'New Stage',
                                    lambda: self.switch_state(LevelEditor), btn_ref='midtop')
        self.btn_load_stage = BtnTxt(self.game, 32, self.game.WINX / 2, self.btn_new_stage.rect.bottom + 10, 205, 50, 'Load Stage',
                                     lambda: self.switch_state(LevelEditor), btn_ref='midtop')
        self.btn_back = BtnBack(self.game, 32, self.game.WINX / 2, self.btn_load_stage.rect.bottom + 10, 205, 50, btn_ref='midtop')
        self.objects = [[self.img_editor], [self.btn_new_stage, self.btn_load_stage, self.btn_back]]

    def render_state(self, surface: pygame.Surface) -> None:
        self.backdrop = self.prev_state.backdrop
        super().render_state(surface)


class LevelEditor(State):
    def __init__(self, game):
        super().__init__(game)

        self.backdrop = pygame.image.load(os.path.join(self.game.background_dir, 'editor.png')).convert()

        self.btn_exit = BtnTxt(self.game, 36, self.game.WINX - 10, 10, 205, 50, 'Exit',
                               func=lambda: self.switch_state(Popup,
                                                              'Warning, you have unsaved changes!',
                                                              'Confirm Exit',
                                                              'Back',
                                                              self.editor,
                                                              func1_exit=True),
                               btn_ref='topright')

        self.objects = [[], [self.btn_exit]]

    def editor(self):
        self.back()