"""Module containing constants used in the game."""
from pathlib import Path
from typing import Literal

import pygame

# mouse buttons

LEFTCLICK = 1
MIDDLECLICK = 2
RIGHTCLICK = 3
SCROLLUP = 4
SCROLLDOWN = 5

# colors

PRIMARY = (30, 30, 30)
SECONDARY = (35, 35, 35)
ACCENT = (85, 85, 85)

DEFAULT_FONT_NAME = "editundo"
DEFAULT_FONT_SIZE = 32

# convert from constant to name

DISPLAY_FLAG_NAMES = {
    pygame.FULLSCREEN: "fullscreen",
    pygame.DOUBLEBUF: "doublebuf",
    pygame.HWSURFACE: "hwsurface",
    pygame.OPENGL: "opengl",
    pygame.NOFRAME: "noframe",
    pygame.RESIZABLE: "resizable",
    pygame.SCALED: "scaled",
    pygame.SHOWN: "shown",
    pygame.HIDDEN: "hidden",
}

# sources root

ROOT = Path.resolve(Path())

EventTypes = Literal[
    "key", "keydown", "keyup",
    "mouse", "mousedown", "mouseup",
    "quit",
]
RectAlignments = Literal[
    "topleft", "midtop", "topright",
    "midleft", "center", "midright",
    "bottomleft", "midbottom", "bottomright"]
TextRectAlignments = Literal["right", "left", "center", "justified"]
