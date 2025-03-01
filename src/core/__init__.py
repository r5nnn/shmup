"""Package containing global utilities and modules for running the game."""
from src.core.prepare import (audio_paths, font_paths, image_paths, screen,
                              screen_rect, screen_size, sprites)
from src.core.utils import (toggle_fullscreen, Singleton, SingletonABCMeta,
                            Validator)
from src.core.data import config, system_data
