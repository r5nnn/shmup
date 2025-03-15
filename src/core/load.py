"""Module for loading assets from files."""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import ClassVar

import pygame


logger = logging.getLogger("src.core")


def parse_spritesheet(spritesheet_file: Path) -> tuple[pygame.Surface, ...]:
    """Gets the subsurfaces from a spritesheet image.

    Splits a spritesheet (image) file into into subsurfaces based on the
    metadata of the spritesheet stored in a json file of the same name. Json
    file should be formatted according to aseprite's spritesheet json output
    format. Order of list returned depends on the order of the sprites
    referenced in the json file.

    :param spritesheet_file: Path to the spritesheet image.
    :returns: A tuple of surfaces based on the metadata in the json file.
    """
    spritesheet = pygame.image.load(spritesheet_file).convert_alpha()
    metadata = spritesheet_file.with_suffix(".json")
    try:
        file = Path.open(metadata, encoding="UTF-8")
    except FileNotFoundError as err:
        msg = (
            f"Spritesheet ({spritesheet_file}) has no accompanying json file."
        )
        raise FileNotFoundError(msg) from err
    else:
        with file:
            data = json.load(file)
    sprite_list = []
    for sprite in (frames := data["frames"]):
        res = frames[sprite]["frame"]
        sprite_list.append(
            spritesheet.subsurface(res["x"], res["y"], res["w"], res["h"])
        )
    logger.info("Parsed spritesheet %s into sprites %s.", spritesheet_file,
             tuple(sprite_list))
    return tuple(sprite_list)


def get_sprites(directory: Path) -> tuple[pygame.Surface, ...]:
    """Gets the sprite surfaces from a given spritesheet directory.

    Uses lazy-loading. Sprites are cached upon being loaded, so they only need
    to be loaded once per game instance.

    :param directory: The path to the spritesheet to get sprite surfaces from.
    :return: A tuple of surfaces based on the spritesheet's metadata json file.
    """
    if directory not in _cached_sprites:
        _cached_sprites[directory] = parse_spritesheet(directory)
    return _cached_sprites[directory]


class _LoadMeta(type):
    """Metaclass to ensure unique Load instances per name."""

    _instances: ClassVar[dict[str, Load]] = {}

    def __call__(cls, name: str,
                 directory: Path | None = None,
                 *accept: str,
                 exclude_dirs: list[str] | None = None,
                 ) -> Load:
        """Ensure each channel_id has a unique instance."""
        if name in cls._instances:
            return cls._instances[name]  # Return existing instance

        # Create and store new instance
        instance = super().__call__(directory, *accept, exclude_dirs=exclude_dirs)
        cls._instances[name] = instance
        return instance


class Load(metaclass=_LoadMeta):
    def __init__(
        self,
        directory: Path,
        *accept: str,
        exclude_dirs: list[str] | None = None,
    ):
        """Class for loading the filepaths of files in a directory.

        Recursively searches directories unless explicitly mentioned to skip in
        `exclude_dirs`.

        :param directory: Directory folder to search recursively through.
        :param accept: File types to accept.
        :param exclude_dirs: Subdirectories inside the directory to ignore.
        """
        self.path = {}
        self.exclude_dirs = exclude_dirs if exclude_dirs else []
        for path, _, files in os.walk(directory):
            if any(
                excluded in os.path.relpath(path, directory)
                for excluded in self.exclude_dirs
            ):
                continue
            for file in files:
                name, ext = Path(file).stem, Path(file).suffix
                if ext.lower() in accept:
                    self.path[name] = Path(path) / file


_cached_sprites = {}
