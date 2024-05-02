import os

import pygame

from .modules.btn import BtnBack, BtnTxt
from .modules.img import Img
from .state import State
from .modules.eventmanager import generalEventManager
from .modules.entity import Enemy


class EditorHome(State):
    def __init__(self, game):
        super().__init__(game)
        self.img_editor = Img(self.game.WINX / 2, self.game.WINY * 0.1, pygame.image.load(os.path.join(self.game.textures_dir, 'null.png')), scale=4)
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
        self.enemies = pygame.sprite.Group()
        # create window background rect
        self.rect = pygame.Rect(0, 0, self.game.WINX * 0.3, self.game.WINY * 0.5)
        # create surface compatible with modifying alpha (pygame.SRCALPHA)
        self.rect_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.rect_surf.set_alpha(128)  # half opacity
        # draw rectangle onto surface
        pygame.draw.rect(self.rect_surf, (0, 0, 0), self.rect_surf.get_rect())

    def on_enter(self) -> None:
        generalEventManager.register(pygame.MOUSEBUTTONDOWN, self.on_click)
        super().on_enter()

    def render_state(self, surface: pygame.Surface) -> None:
        surface.blit(self.prev_state.backdrop, (0, 0))
        surface.blit(self.rect_surf, self.rect_surf.get_rect(midright=(self.game.WINX, self.game.WINY / 2)))
        super().render_state(surface)
        self.enemies.draw(surface)

    def on_click(self) -> None:
        self.enemy = Enemy(self, self.game.pos[0], self.game.pos[1], {'hp': 4,'df': 0, 'atk': 1}, os.path.join(self.game.sfx_dir, 'shoot.wav'), ref='center')
        self.enemies.add(self.enemy)
