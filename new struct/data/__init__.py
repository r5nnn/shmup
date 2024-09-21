import json
import os
import sys
from abc import ABC, abstractmethod
from typing import Literal

import pygame

pygame.init()
pygame.display.set_caption("shmup")
pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)

# type hints
rect_alignments = Literal['midtop', 'topright', 'midleft', 'center',
                          'midright', 'bottomleft', 'midbottom', 'bottomright']


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
    for sprite in data:
        frame = data[sprite]
        sprites[f"{sprite_name} {frame["tag"]}"] = (
            spritesheet.subsurface(frame["pos"]['x'], frame["pos"]['y'],
                                   frame["pos"]['w'], frame["pos"]['h']))
    return sprites


class _Load(ABC):
    def __init__(self, directory: str, *accept: str,
                 exclude_dirs: list[str] = None):
        """Loads in files from specified directories. Allows for filtering
        accepted files by file extension and excluding certain directories.

        :param directory: Directory storing all the files to load.
        :param accept: Tuple of file endings to look for.
        :param exclude_dirs: List of directory names to exclude from the search.
        """
        self.files = {}
        self.exclude_dirs = exclude_dirs if exclude_dirs else []

        for path, dirs, file in os.walk(directory):
            if any(excluded in os.path.relpath(path, directory) for excluded in
                   self.exclude_dirs):
                continue

            for f in file:
                name, ext = os.path.splitext(f)
                if ext.lower() in accept:
                    self.process_file(f, name, path)

    @abstractmethod
    def process_file(self, file: str, name: str, directory: str):
        """Abstract method to be implemented by subclasses to process files."""
        pass

    def __call__(self) -> dict[str, str]:
        """
        :returns: A dictionary of file names pointing to their directories."""
        return self.files


class _LoadImages(_Load):
    def __init__(self,
                 directory: str,
                 accept: tuple[str] = (".png", ".jpeg", ".jpg"),
                 exclude_dirs: list[str] = None):
        super().__init__(directory, *accept, exclude_dirs=exclude_dirs)

    def process_file(self, file: str, name: str, directory: str):
        if os.path.isfile(os.path.join(directory, file+".json")):
            image = parse_spritesheet(file)
        else:
            image = pygame.image.load(os.path.join(directory, file))
            if image.get_alpha():
                image = image.convert_alpha()
            else:
                image = image.convert()
        self.files[name] = image


fonts = _Load(os.path.join("resources", "fonts"), ".ttf")
graphics = _LoadImages(os.path.join("resources", "graphics"))


class Validator(ABC):
    """Descriptor parent class for validating a property in various ways."""
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        self._validate(instance, value)
        setattr(instance, self.private_name, value)

    @abstractmethod
    def _validate(self, instance, value):
        pass
