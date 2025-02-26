"""Module for preparing the game to run by initialising the game's components."""
from __future__ import annotations

import json
import logging
import os
from operator import attrgetter
from pathlib import Path
from src.core.data import config, system_data

import pygame

pygame.init()
pygame.display.set_caption("shmup")
for flag_name, enabled in config["flags"].items():
    if enabled:
        system_data["flags"] |= attrgetter(flag_name.upper())(pygame)
pygame.display.set_mode((1920, 1080), system_data["flags"])

sources_root = Path.resolve(Path())

screen = pygame.display.get_surface()
screen_size = screen.get_size()
screen_center = tuple(round(coordinate / 2) for coordinate in screen_size)
screen_rect = screen.get_rect()

logging.basicConfig(level=logging.WARNING,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%d/%m/%Y %H:%M:%S")


def parse_spritesheet(spritesheet_file: Path) -> list[pygame.Surface]:
    """Gets the subsurfaces from a spritesheet image.

    Splits a spritesheet (image) file into into subsurfaces based on the metadata of
    the spritesheet stored in a json file of the same name. Json file should be
    formatted according to aseprite's spritesheet json output format. Result is stored
    in a tuple. Order of list returned depends on the order of the sprites referenced
    in the json file.
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
    return sprite_list


class Load:
    """Class for loading the filepaths of files in a directory.

    Recursively searches directories unless explicitly mentioned to skip in
    `exclude_dirs`.
    """

    def __init__(self, directory: Path, *accept: str,
                 exclude_dirs: list[str] | None = None):
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
        return self.files[name]


class LoadSprites:
    """Class for loading in sprites/spritesheets from a given directory.

    Recursively searches directories unless explicitly mentioned to skip in
    `exclude_dirs`. If file has an accompanying json file, attempts to load spritesheet
    using the `parse_spritesheet` function.
    """

    def __init__(self, directory: Path):
        self.files = {}
        self.default = None
        for path, _, files in os.walk(directory):
            for file in files:
                name, ext = Path(file).stem, Path(file).suffix
                if ext.lower() == ".png" and Path.is_file(
                        Path(path) / (name + ".json")):
                    path1 = Path(path) / file
                    image = parse_spritesheet(path1)
                    self.files[name] = image

    def __call__(self, name: str) -> list[pygame.Surface] | None:
        return self.files.get(name, self.default)


image_paths = Load(Path(sources_root) / "resources" / "graphics", ".png")
audio_paths = Load(Path(sources_root) / "resources" / "audio", ".wav")
font_paths = Load(Path(sources_root) / "resources" / "fonts", ".ttf")
sprites = LoadSprites(Path(sources_root) / "resources" / "graphics")
