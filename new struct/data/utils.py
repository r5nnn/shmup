import json
import os
import sys
from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, Literal, override

import pygame
from pygame import freetype


@dataclass(frozen=True)
class CustomTypes:
    rect_alignments = Literal['topleft', 'midtop', 'topright',
                              'midleft', 'center', 'midright',
                              'bottomleft', 'midbottom', 'bottomright']
    alignments = Literal['left', 'right', 'center', 'block']


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


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class _SingletonABCMeta(Singleton, ABCMeta):
    pass


class _Load(ABC, metaclass=_SingletonABCMeta):
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
        return os.path.join(directory, file)

    def __call__(self, name: str = None,
                 mode: Literal["object", "path"] = "object") -> dict | Any:
        """
        :returns: A dictionary of file names pointing to their directories."""
        return self.files[name][mode] if name is not None else self.files


class _LoadImages(_Load):
    def __init__(self, directory: str, exclude_dirs: list[str] = None):
        super().__init__(directory, *(".png", ".jpeg", ".jpg"),
                         exclude_dirs=exclude_dirs)

    @override
    def process_file(self, file: str, name: str, directory: str):
        path = super().process_file(file, name, directory)  # returns path
        if os.path.isfile(os.path.join(directory, name+".json")):
            image = parse_spritesheet(path)
        else:
            image = pygame.image.load(path)
            if image.get_alpha():
                image = image.convert_alpha()
            else:
                image = image.convert()
        self.files[name] = {"object": image, "path": path}


class _LoadFonts(_Load):
    def __init__(self, directory: str, exclude_dirs: list[str] = None):
        super().__init__(directory, ".ttf", exclude_dirs=exclude_dirs)

    @override
    def process_file(self, file: str, name: str, directory: str):
        path = super().process_file(file, name, directory)  # returns path
        self.files[name] = {
            "object": pygame.freetype.Font(path),
            "path": path}


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


fonts = _LoadFonts(os.path.join("resources", "fonts"))
graphics = _LoadImages(os.path.join("resources", "graphics"))