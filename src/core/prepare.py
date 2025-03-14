"""Module for preparing the game to run by initialising the game's components."""

from __future__ import annotations

import logging
from pathlib import Path

from src.components import Audio
from src.core import main, settings, system_data
from src.core.constants import ROOT, DISPLAY_FLAG_NAMES_MAP

import pygame

from src.core.load import Load
from src.states import game, options, title

logger = logging.getLogger("src.core")

pygame.init()
pygame.display.set_caption(
    f"shmup {system_data.version}-{system_data.version_type}"
)

for flag_name, enabled in settings.flags.items():
    if enabled:
        system_data.flags |= DISPLAY_FLAG_NAMES_MAP.inverse[flag_name][0]
        logger.info("Added flag %s to system_data.", flag_name.upper())

system_data.screen_rect = pygame.Rect(
    0, 0, pygame.display.Info().current_w, pygame.display.Info().current_h
)

pygame.display.set_mode((1920, 1080), system_data.flags)

system_data.window = pygame.display.get_surface()
system_data.window_rect = system_data.window.get_rect()

if (
    system_data.window_rect.size == system_data.screen_rect.size
    and system_data.default_config
):
    settings.keep_mouse_pos = False
    logger.info(
        "Screen size %s matches native window resolution %s, disabled "
        "keep_mouse_pos in system_data.",
        system_data.screen_rect.size,
        system_data.window_rect.size,
    )

system_data.image_paths = Load(Path(ROOT) / "assets" / "graphics", ".png")
system_data.audio_paths = Load(Path(ROOT) / "assets" / "audio", ".wav")
system_data.font_paths = Load(Path(ROOT) / "assets" / "fonts", ".ttf")
pygame.display.set_icon(pygame.image.load(system_data.image_paths("icon")))

system_data.background_audio = Audio()
system_data.background_audio.set_volume(0.2)

system_data.button_audio = Audio()
system_data.button_audio.set_volume(0.2)
system_data.button_audio.add_audio(system_data.audio_paths("click"))

states = {"title": title.Title, "options": options.Options, "game": game.Game}
start_state = "title"

main.init(states, start_state)
logger.info(
    "main.py initialised with dict %s and starting state %s",
    states,
    start_state,
)
