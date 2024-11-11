"""Package that contains core modules for initialising and running the game.

Also contains utilities used globally across the game."""
from data.core.prepare import (audio_paths, font_paths, image_paths, screen,
                               screen_rect, screen_size, sprites)
from data.core.utils import (Colors, Mouse, Observer, Popups, Singleton,
                             SingletonABCMeta, Validator)
from data.core.control import quit_game

__all__ = ["screen", "screen_size", "screen_rect", "image_paths", "audio_paths",
           "font_paths", "sprites", "Mouse", "Popups", "Colors", "Singleton",
           "Observer", "SingletonABCMeta", "Validator", "quit_game"]
