"""Module containing constants used in the game."""
from typing import Literal

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

# literal type constants

input_types = Literal[
    "key", "keydown", "keyup",
    "mouse", "mousedown", "mouseup",
    "quit",
]
# both display_flag constants are missing pygame.FULLSCREEN since there is a
# dedicated toggle_fullscreen function meaning it is always expected when
# passed.
display_flags = Literal[1073741824, 1, 2, 16, 32, 64, 128, 512]
display_flag_names = Literal[
    "doublebuf", "hwsurface", "opengl", "noframe",
    "resizable", "scaled", "shown", "hidden",
]
