from pathlib import Path

import pygame
from pydantic import BaseModel
from collections import deque

from src.core.data import FileModel


class UiKeybinds(BaseModel):
    back: list[tuple[str, int]] = [("", pygame.K_ESCAPE)]
    exit: list[tuple[str, int]] = [("keydown", pygame.K_END)]
    fullscreen: list[tuple[str, int]] = [pygame.K_F11]
    fullscreen_borderless: list[tuple[str, int]] = []


class GameKeybinds(BaseModel):
    move_up: list[int] = [pygame.K_w, pygame.K_UP]
    move_down: list[int] = [pygame.K_s, pygame.K_DOWN]
    move_left: list[int] = [pygame.K_a, pygame.K_LEFT]
    move_right: list[int] = [pygame.K_d, pygame.K_RIGHT]
    focus: list[int] = [pygame.K_LSHIFT, pygame.K_RSHIFT]
    main_attack: list[int] = [pygame.K_z]


class Keybinds(FileModel):
    ui = UiKeybinds()
    game = GameKeybinds()


keybinds_dir = Path("keybinds.json")
keybinds, _ = Keybinds.load()
