"""Package containing components that help run the game."""

import logging

from src.components.audio import Audio
from src.components.colors import shift_rgb, ColorGradient
from src.components.managers import statemanager, overlaymanager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
