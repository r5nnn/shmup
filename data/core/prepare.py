"""Prepares pygame by initializing all its modules and creating the display.

Additionally searches directories and identifies the paths to all the assets
to be used in the game. Loads in fonts and spritesheets."""
import json
import os

import pygame

pygame.init()
pygame.display.set_caption("shmup")
pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)

sources_root = os.path.abspath('.')

def parse_spritesheet(sprite_sheet: str) -> dict[str, pygame.Surface]:
    """Parses a spritesheet using its associated json file.

    :param sprite_sheet: The sprite sheet file to get sprites from.
    :returns: A dictionary containing the name of the sprite pointing to
        a subsurface of the spritesheet with the specific sprite on it."""
    spritesheet = pygame.image.load(sprite_sheet).convert_alpha()
    sprite_name = os.path.splitext(sprite_sheet)[0]
    metadata = sprite_name + '.json'
    try:
        metadata_json = open(metadata, encoding='UTF-8')
    except OSError:
        print(f'Could not open/read file: {metadata}')
        raise OSError
    with metadata_json:
        data = json.load(metadata_json)
    metadata_json.close()
    sprite_dict = {}
    for sprite in (frames := data["frames"]):
        res = frames[sprite]["frame"]
        sprite_dict[sprite] = spritesheet.subsurface(res['x'], res['y'],
                                                     res['w'], res['h'])
    return sprite_dict


class Load:
    """Loads in files from specified directories.

    :param directory: The parent directory to start searching from.
        Subdirectories are also searched.
    :param accept: The file endings to search for.
    :param exclude_dirs: Subdirectories to skip when searching for files."""

    def __init__(self, directory: str, *accept: str, exclude_dirs: list[str] = None):
        self.files = {}
        self.exclude_dirs = exclude_dirs if exclude_dirs else []
        for path, dirs, files in os.walk(directory):
            if any(excluded in os.path.relpath(path, directory) for excluded in
                   self.exclude_dirs):
                continue
            for file in files:
                name, ext = os.path.splitext(file)
                if ext.lower() in accept:
                    self.files[name] = os.path.join(path, file)

    def __call__(self, name: str) -> str:
        """Returns a dictionary of file names pointing to their directories."""
        return self.files[name]


class LoadSprites:
    """Loads in spritesheets from specified directories.

    :param directory: The directory to start searching from. Subdirectories are
        also searched."""

    def __init__(self, directory: str):
        self.files = {}
        for path, dirs, files in os.walk(directory):
            for file in files:
                name, ext = os.path.splitext(file)
                if ext.lower() == '.png' and os.path.isfile(
                        os.path.join(path, name + ".json")):
                    path1 = os.path.join(path, file)
                    image = parse_spritesheet(path1)
                    self.files[name] = image

    def __call__(self, name: str) -> dict:
        """Returns a dictionary of file names pointing to their directories."""
        return self.files[name]

image_paths = Load(os.path.join(sources_root, 'resources', 'graphics'), '.png')
audio_paths = Load(os.path.join(sources_root, 'resources', 'audio'), '.wav')
font_paths = Load(os.path.join(sources_root, 'resources', 'fonts'), '.ttf')
sprites = LoadSprites(os.path.join(sources_root, 'resources', 'graphics'))
