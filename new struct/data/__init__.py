import json
import os
import sys

import pygame

from data.utils import SingletonABCMeta, Singleton

pygame.init()
pygame.display.set_caption("shmup")
pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)

def parse_spritesheet(sprite_sheet: str):
    """Parses a spritesheet using its associated json file.

    :param sprite_sheet: Directory to the spritesheet.

    :return: A dictionary of the sprites name along with its tag and a
        subsurface with the specific sprite on it.
    """
    spritesheet = pygame.image.load(sprite_sheet).convert_alpha()
    sprite_name = os.path.splitext(sprite_sheet)[0]
    metadata = sprite_name + '.json'
    try:
        metadata_json = open(metadata, encoding='UTF-8')
    except OSError:
        print(f'Could not open/read file: {metadata}')
        sys.exit()
    with metadata_json:
        data = json.load(metadata_json)
    metadata_json.close()
    sprites = {}
    for sprite in (frames := data["frames"]):
        res = frames[sprite]["frame"]
        sprites[sprite] = (
            spritesheet.subsurface(res['x'], res['y'], res['w'], res['h']))
    return sprites


class Load:
    def __init__(self, directory: str, *accept: str,
                 exclude_dirs: list[str] = None):
        """Loads in files from specified directories. Allows for filtering
        accepted files by file extension and excluding certain directories.

        :param directory: Directory storing all the files to load.
        :param accept: Tuple of file endings to look for.
        :param exclude_dirs: List of directory names to exclude from the
            search.
        """
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
        """
        :returns: A dictionary of file names pointing to their directories."""
        return self.files[name]


class LoadSprites:
    def __init__(self, directory: str):
        self.files = {}
        for path, dirs, files in os.walk(directory):
            for file in files:
                name, ext = os.path.splitext(file)
                if ext.lower() == '.png' and os.path.isfile(
                        os.path.join(path, name+".json")):
                    path1 = os.path.join(path, file)
                    image = parse_spritesheet(path1)
                    self.files[name] = image

    def __call__(self, name: str) -> dict:
        """
        :returns: A dictionary of file names pointing to their directories."""
        return self.files[name]


image_paths = Load(os.path.join('resources', 'graphics'), '.png')
audio_paths = Load(os.path.join('resources', 'audio'), '.wav')
font_paths = Load(os.path.join('resources', 'fonts'), '.ttf')
sprites = LoadSprites(os.path.join('resources', 'graphics'))
