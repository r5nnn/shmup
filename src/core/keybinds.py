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
    move_up: Keybinds_ = [[("key", pygame.K_w)], [("key", pygame.K_UP)]]
    move_down: Keybinds_ = [[("key", pygame.K_s)], [("key", pygame.K_DOWN)]]
    move_left: Keybinds_ = [[("key", pygame.K_a)], [("key",pygame.K_LEFT)]]
    move_right: Keybinds_ = [[("key", pygame.K_d)], [("key", pygame.K_RIGHT)]]
    focus: Keybinds_ = [[("key", pygame.K_LSHIFT)], [("key", pygame.K_RSHIFT)]]
    main_attack: Keybinds_ = [[("key",pygame.K_z)]]


class Keybinds(FileModel):
    ui: UiKeybinds = UiKeybinds()
    game: GameKeybinds = GameKeybinds()


keybinds_dir = Path("keybinds.json")
keybinds, _ = Keybinds.load(keybinds_dir)
