from pathlib import Path

import pygame
from pydantic import BaseModel

from src.core.data import FileModel


Keybinds_ = list[list[tuple[str, int]]]


class UiKeybinds(BaseModel):
    back: Keybinds_ = [[("keydown", pygame.K_ESCAPE)]]
    quit: Keybinds_ = [[("keydown", pygame.K_END)]]
    fullscreen: Keybinds_ = [[("keydown", pygame.K_F11)]]
    noframe: Keybinds_ = [
        [("key", pygame.K_LSHIFT), ("keydown", pygame.K_F11)],
        [("key", pygame.K_RSHIFT), ("keydown", pygame.K_F11)],
    ]


class GameKeybinds(BaseModel):
    move_up: list[int] = [pygame.K_w, pygame.K_UP]
    move_down: list[int] = [pygame.K_s, pygame.K_DOWN]
    move_left: list[int] = [pygame.K_a, pygame.K_LEFT]
    move_right: list[int] = [pygame.K_d, pygame.K_RIGHT]
    focus: list[int] = [pygame.K_LSHIFT, pygame.K_RSHIFT]
    main_attack: list[int] = [pygame.K_z]


class Keybinds(FileModel):
    ui: UiKeybinds = UiKeybinds()
    game: GameKeybinds = GameKeybinds()


keybinds_dir = Path("keybinds.json")
keybinds, _ = Keybinds.load(keybinds_dir)
