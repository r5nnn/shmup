"""Package containing global utilities and modules for running the game."""

import logging

from src.core.utils import toggle_flag, toggle_fullscreen
from src.core.data import settings, system_data
from src.core.structs import Validator, Bidict
from src.core.keybinds import keybinds, keybinds_dir

logger = logging.getLogger("src")
logger.setLevel(logging.INFO)
