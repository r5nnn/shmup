"""Package containing global utilities and modules for running the game."""

from src.core.prepare import (
    audio_paths,
    font_paths,
    image_paths,
    spritesheet_paths,
    get_sprites,
)
from src.core.utils import toggle_flag, toggle_fullscreen, Validator
from src.core.data import config, system_data
