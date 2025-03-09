"""Module for preparing the game to run by initialising the game's components."""
from __future__ import annotations

import json
import logging
import os
from operator import attrgetter
from pathlib import Path
from src.core.data import config, system_data
from src.core.constants import ROOT

import pygame

pygame.init()
pygame.display.set_caption("shmup " + system_data["version"])
for flag_name, enabled in config["flags"].items():
    if enabled:
        system_data["flags"] |= attrgetter(flag_name.upper())(pygame)
pygame.display.set_mode((1920, 1080), system_data["flags"])

screen = pygame.display.get_surface()
screen_size = screen.get_size()
screen_center = tuple(round(coordinate / 2) for coordinate in screen_size)
screen_rect = screen.get_rect()

logging.basicConfig(level=logging.WARNING,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%d/%m/%Y %H:%M:%S")


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
        msg = f"Spritesheet ({spritesheet_file}) has no accompanying json file."
        raise FileNotFoundError(msg) from err
    else:
        with file:
            data = json.load(file)
    sprite_list = []
    for sprite in (frames := data["frames"]):
        res = frames[sprite]["frame"]
        sprite_list.append(
            spritesheet.subsurface(res["x"], res["y"], res["w"], res["h"]))
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


class Load:
    def __init__(self, directory: Path, *accept: str,
                 exclude_dirs: list[str] | None = None):
        """Class for loading the filepaths of files in a directory.

        Recursively searches directories unless explicitly mentioned to skip in
        `exclude_dirs`.

        :param directory: Directory folder to search recursively through.
        :param accept: File types to accept.
        :param exclude_dirs: Subdirectories inside the directory to ignore.
        """
        self.files = {}
        self.exclude_dirs = exclude_dirs if exclude_dirs else []
        for path, _, files in os.walk(directory):
            if any(excluded in os.path.relpath(path, directory) for excluded in
                   self.exclude_dirs):
                continue
            for file in files:
                name, ext = Path(file).stem, Path(file).suffix
                if ext.lower() in accept:
                    self.files[name] = Path(path) / file

    def __call__(self, name: str) -> Path:
        """Returns the path to the filename specified.

        :param name: Name of the file.
        :return: The path to that file.
        """
        return self.files[name]


_cached_sprites = {}

image_paths = Load(Path(ROOT) / "assets" / "graphics", ".png")
audio_paths = Load(Path(ROOT) / "assets" / "audio", ".wav")
font_paths = Load(Path(ROOT) / "assets" / "fonts", ".ttf")
spritesheet_paths = Load(Path(ROOT) / "assets" / "graphics", ".png")

pygame.display.set_icon(pygame.image.load(image_paths("icon")))