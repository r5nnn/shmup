"""Module containing utilities with some dependencies on other game modules."""

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
    logger.debug(
        "Attempting to toggle flag, and setmode with %s and flags %s %s",
        settings.resolution,
        system_data.flags,
        settings.flags,
    )
    pygame.display.set_mode(settings.resolution, system_data.flags)
    system_data.window = pygame.display.get_surface()
    logger.info(
        "Window flag %s toggled %s", flag_name, "on" if toggled else "off"
    )


def set_resolution(size: tuple[int, int]) -> None:
    if size == settings.resolution:
        logging.info(
            "Window resolution: %s equal to new resolution. Ignoring call.",
            settings.resolution,
        )
        return
    logger.debug(
        "Attempting to set the mode of the screen with resolution %s and flags"
        " %s %s",
        size,
        system_data.flags,
        settings.flags,
    )
    pygame.display.set_mode(size, system_data.flags)
    logger.info(
        "Window resolution changed from %s to %s.", settings.resolution, size
    )
    settings.resolution = size
    system_data.window = pygame.display.get_surface()
    system_data.window_rect = system_data.window.get_rect()
    update_scale_factor()


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
        # causes the noframe flag and potentially other flags to disappear.
        # Toggling the flag and manually setting the mode of the screen makes
        # sure all flags are preserved.
        toggle_flag(pygame.FULLSCREEN)
    else:
        system_data.flags ^= pygame.FULLSCREEN
        settings.flags["fullscreen"] = True
        pygame.display.toggle_fullscreen()
        system_data.window = pygame.display.get_surface()
        logger.info(
            "Fullscreen safely toggled on using"
            " pygame.display.toggle_fullscreen()."
        )
    if settings.keep_mouse_pos:
        logger.debug(
            "keep_mouse_pos is True, so setting coords to absolute position: "
            "%s",
            coords,
        )
        events.set_abs_mouse_pos(coords)
        pygame.mouse.set_visible(True)


def update_scale_factor(*, non_native_ratio: bool | None = None) -> None:
    if non_native_ratio is not None:
        settings.non_native_ratio = non_native_ratio
    else:
        non_native_ratio = settings.non_native_ratio
    if settings.non_int_scaling:
        scalex = (
            system_data.window_rect.width / system_data.abs_window_rect.width
        )
        scaley = (
            system_data.window_rect.height / system_data.abs_window_rect.height
        )
        if non_native_ratio:
            system_data.scale_factor = (scalex, scaley)
        else:
            minimum_ratio = min(scalex, scaley)
            system_data.scale_factor = (minimum_ratio, minimum_ratio)
    else:
        int_scalex = (
            system_data.window_rect.width // system_data.abs_window_rect.width
        )
        int_scaley = (
            system_data.window_rect.height
            // system_data.abs_window_rect.height
        )
        if non_native_ratio:
            system_data.scale_factor = (int_scalex, int_scaley)
        else:
            minimum_int_ratio = min(int_scalex, int_scaley)
            system_data.scale_factor = minimum_int_ratio
    logger.info(
        "Scale factor calculated as %s filtering based on non_int_scaling as "
        "%s, non_native_resolution as %s, window size: %s and internal "
        "surface size: %s.",
        system_data.scale_factor,
        settings.non_int_scaling,
        settings.non_native_ratio,
        system_data.window_rect.size,
        system_data.abs_window_rect.size,
    )
