import os
import json
from typing import override

import pygame

from .modules.btn import BtnBack, BtnTxt
from .modules.img import Img
from .modules.eventmanager import generalEventManager
from .modules.txtinput import TextInputVisualizer, TextInputManager
from .state import State
from .popup import Popup


class EditorHome(State):
    def __init__(self, game):
        super().__init__(game)
        self.img_editor = Img(
            (self.game.WINX / 2, self.game.WINY * 0.1),
            pygame.image.load(os.path.join(self.game.title_dir, 'editor.png')),
            scale=4
        )
        self.btn_new_stage = BtnTxt(
            self.game,
            (self.game.WINX / 2, self.img_editor.img_rect.bottom + 20),
            205, 50,
            'New Stage',
            lambda: self.switch_state(LevelEditor),
            font_size=32,
            btn_allign='midtop'
        )
        self.btn_load_stage = BtnTxt(
            self.game,
            (self.game.WINX / 2, self.btn_new_stage.rect.bottom + 10),
            205, 50,
            'Load Stage',
            self.name_state,
            font_size=32,
            btn_allign='midtop'
        )
        self.text_input = None
        self.btn_back = BtnBack(
            self.game,
            (self.game.WINX / 2, self.btn_load_stage.rect.bottom + 10),
            205, 50,
            font_size=32,
            btn_allign='midtop'
        )
        self.objects = [
            [self.img_editor],
            [self.btn_new_stage, self.btn_load_stage, self.btn_back]
        ]

    def render_state(self, surface: pygame.Surface) -> None:
        self.backdrop = self.prev_state.backdrop
        super().render_state(surface)
        surface.blit(self.text_input.surface,
                     self.text_input.surface.get_rect(
                         center=(self.game.WINX/2, self.game.WINY/2))
                     ) if self.text_input is not None else None

    def name_state(self):
        ...


class LevelEditor(State):
    def __init__(self, game, file=None, save_dir=None):
        super().__init__(game)

        self.backdrop = pygame.image.load(os.path.join(self.game.background_dir,
                                                       'editor.png')).convert()

        self.btn_exit = BtnTxt(
            self.game,
            (self.game.WINX - 10, 10),
            195, 50,
            'Exit',
            func=lambda: self.switch_state(Popup,
                                           'Warning, you have unsaved changes!',
                                           'Confirm Exit',
                                           'Back',
                                           self.editor,
                                           func1_exit=True),
            font_size=36,
            btn_allign='topright'
        )

        self.btn_save = BtnTxt(
            self.game,
            (self.game.WINX - 10, self.btn_exit.rect.bottom + 10),
            195, 50,
            'Save',
            func=self.save,
            font_size=36,
            btn_allign='topright'
        )
        self.btn_save_exit = BtnTxt(
            self.game,
            (self.game.WINX - 10, self.btn_save.rect.bottom + 10),
            195, 50,
            'Save & Exit',
            func=self.save_exit,
            font_size=36,
            btn_allign='topright')

        self.data = {

        }

        # with open(os.path.join(save_dir, 'unnamed.json'), 'w') as f:
        #     json.dump(self.data, f)

        self.objects = [[], [self.btn_exit, self.btn_save, self.btn_save_exit]]

    def editor(self):
        super().back()

    @override
    def back(self, play_sfx: bool = True):
        self.game.btn_sfx.force_play_audio('click') if play_sfx else None
        self.switch_state(Popup,
                          'Warning, you have unsaved changes!',
                          'Confirm Exit',
                          'Back',
                          self.editor,
                          func1_exit=True)

    def save(self):
        print('save placeholder')

    def save_exit(self):
        self.save()
        super().back()