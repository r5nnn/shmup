"""Module containing functions and design patterns used globally across the game."""

from __future__ import annotations

import logging

import pygame

from src.core.constants import DISPLAY_FLAG_NAMES_MAP
from src.core.data import settings, system_data
from src.components import events

logger = logging.getLogger(__name__)


def toggle_flag(flag: int) -> None:
    """Toggles the given flag and resets the screen mode with the new flags.

    :param flag: The integer value of the flag to toggle.
    """
    system_data.flags ^= flag
    settings.flags[flag_name := DISPLAY_FLAG_NAMES_MAP[flag]] = (
        toggled := not settings.flags[DISPLAY_FLAG_NAMES_MAP[flag]]
    )
    pygame.display.set_mode((1920, 1080), system_data.flags)
    logger.info(
        "Window flag %s toggled %s", flag_name, "on" if toggled else "off"
    )


def toggle_fullscreen() -> None:
    """Toggles the fullscreen flag of the screen.

    While this could be done using exclusively the toggle_flag procedure,
    pygame has an inbuilt toggle_fullscreen procedure that is more efficient,
    however doesn't work if already in fullscreen. This procedure abstracts the
    logic for choosing the correct method.

    Also sets the absolute position of the mouse cursor to the same location it
    was before toggling using pynput, since pygame cannot get or set
    coordinates beyond the main window.
    """
    if settings.keep_mouse_pos:
        pygame.mouse.set_visible(False)
        coords = events.get_abs_mouse_pos()
    if system_data.flags & pygame.FULLSCREEN:
        # Using the pygame inbuilt display.toggle_fullscreen to exit fullscreen
        # causes the noframe  flag and potentially other flags to disappear.
        # Toggling the flag and manually setting the mode of the screen makes
        # sure all flags are preserved.
        toggle_flag(pygame.FULLSCREEN)
    else:
        system_data.flags ^= pygame.FULLSCREEN
        settings.flags["fullscreen"] = True
        pygame.display.toggle_fullscreen()
        logger.info(
            "Fullscreen safely toggled on using"
            " pygame.display.toggle_fullscreen()."
        )
    if settings.keep_mouse_pos:
        logger.debug(
            "keep_mouse_pos is True, so setting coords to absolute position: %s",
            coords,
        )
        events.set_abs_mouse_pos(coords)
        pygame.mouse.set_visible(True)
