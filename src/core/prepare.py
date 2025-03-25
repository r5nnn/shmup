"""Module for preparing the game to run by initialising the game's components."""

from __future__ import annotations

import logging
from pathlib import Path

from src.components import Audio, events
from src.components.managers import statemanager
from src.components.managers.statemanager import back
from src.core import keybinds, main, settings, system_data
from src.core.constants import ROOT, DISPLAY_FLAG_NAMES_MAP
from src.core.utils import toggle_flag, toggle_fullscreen, update_scale_factor

import pygame

from src.core.load import Load
from src.states import game, options, title

logger = logging.getLogger("src.core")

pygame.init()
pygame.display.set_caption(
    f"shmup {system_data.version}-{system_data.version_type}"
)
system_data.screen_rect = pygame.Rect(
    0, 0, pygame.display.Info().current_w, pygame.display.Info().current_h
)

for flag_name, enabled in settings.flags.items():
    if enabled:
        system_data.flags |= DISPLAY_FLAG_NAMES_MAP.inverse[flag_name][0]
        logger.info("Added flag %s to system_data.", flag_name.upper())

system_data.window = pygame.display.set_mode(
    settings.resolution, system_data.flags
)
logger.info("Created window with resolution %s.", settings.resolution)

system_data.window_rect = system_data.window.get_rect()
system_data.abs_window = pygame.Surface((1920, 1080))
system_data.abs_window_rect = system_data.abs_window.get_rect()
update_scale_factor()

if (
    system_data.window_rect.size == system_data.abs_window_rect.size
    and system_data.default_config
):
    settings.keep_mouse_pos = False
    logger.info(
        "Screen size %s matches native window resolution %s, disabled "
        "keep_mouse_pos in system_data.",
        system_data.abs_window_rect.size,
        system_data.window_rect.size,
    )

Load("image", Path(ROOT) / "assets" / "graphics", ".png")
Load("audio", Path(ROOT) / "assets" / "audio", ".wav")
Load("font", Path(ROOT) / "assets" / "fonts", ".ttf")
pygame.display.set_icon(pygame.image.load(Load("image").path["icon"]))

Audio("bgm").set_volume(0.2)
Audio("bgm").add_audio(Load("audio").path["menuloop rmx"])

Audio("sfx").set_volume(0.2)
Audio("sfx").add_audio(Load("audio").path["click"])

states = {"title": title.Title, "options": options.Options, "game": game.Game}
start_state = "title"

for keybind in keybinds.ui.fullscreen:
    events.eventbinder.register(*keybind, action=toggle_fullscreen)
for keybind in keybinds.ui.quit:
    events.eventbinder.register(*keybind, action=statemanager.quit_game)
for keybind in keybinds.ui.noframe:
    events.eventbinder.register(
        *keybind, action=lambda: toggle_flag(pygame.NOFRAME)
    )
for key_combo in keybinds.ui.back:
    events.eventbinder.register(*key_combo, action=back)


main.init(states, start_state)
logger.info(
    "main.py initialised with dict %s and starting state %s",
    states,
    start_state,
)
