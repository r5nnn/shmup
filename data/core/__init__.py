"""Package containing global utilities and modules fo running the game."""
from data.core.prepare import (audio_paths, font_paths, image_paths, screen,
                               screen_rect, screen_size, sprites)
from data.core.utils import (Colors, Mouse, Observer, Singleton, SingletonABCMeta,
                             Validator)
from data.core.control import quit_game
