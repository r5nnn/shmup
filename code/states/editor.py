import os
import json
from typing import override

import pygame

from .modules.btn import BtnBack, BtnTxt
from .modules.img import Img
from .state import State
from .popup import Popup, PopupTextbox


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
            lambda: self.switch_state(PopupTextbox,
                                      'Enter the name of your stage:',
                                      'Confirm',
                                      'Cancel',
                                      btn1_func=self.create_stage,
                                      font=pygame.font.Font(
                                          self.game.font1_dir, 32),
                                      func1_exit=True),
            font_size=32,
            btn_allign='midtop'
        )
        self.btn_load_stage = BtnTxt(
            self.game,
            (self.game.WINX / 2, self.btn_new_stage.rect.bottom + 10),
            205, 50,
            'Load Stage',
            self.create_stage,
            font_size=32,
            btn_allign='midtop'
        )
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

    def create_stage(self, name: str):
        self.data = {
            name: {
            }
        }
        if not (exists := os.path.isfile(path := os.path.join('stages', f'{name}.json'))):
            try:
                with open(path, 'w') as f:
                    json.dump(self.data, f)
            except OSError:
                exists = "Error, invalid file name, try again:"
        # since strings with any form of characters become True when converted
        # into a boolean, this check can be used to avoid using a goto function
        # or rewriting the popup object twice. Peak coding brother.
        if bool(exists):
            self.switch_state(PopupTextbox,
                              exists if type(exists) is str else 'Error, file already exists, try again:',
                              'Confirm',
                              'Cancel',
                              btn1_func=self.create_stage,
                              font=pygame.font.Font(
                                  self.game.font1_dir, 32),
                              func1_exit=True)


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