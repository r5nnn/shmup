"""Contains utilities for handling and binding events."""

import logging

from src.components.events import eventbinder
from src.components.events.utils import (
    process,
    is_key_up,
    is_key_down,
    is_key_pressed,
    is_mouse_pressed,
    is_mouse_up,
    is_mouse_down,
    get_mouse_pos,
    get_abs_mouse_pos,
    set_abs_mouse_pos,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
