import os
from abc import ABC, abstractmethod
from typing import Literal, override

import pygame

# initialisation
pygame.init()
pygame.display.set_caption("shmup")
screen = pygame.display.set_mode(
    MONITOR_SIZE := (pygame.display.Info().current_w,
                     pygame.display.Info().current_h),
    pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF
)
SCREEN_SIZE = MONITOR_SIZE
display = pygame.Surface(SCREEN_SIZE)

# type hints shorthands
rect_alignments = Literal['midtop', 'topright', 'midleft', 'center',
                          'midright', 'bottomleft', 'midbottom', 'bottomright']

# colors
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
button_colors = {'inactive': pygame.Color(30, 30, 30),
                 'hovered': pygame.Color(35, 35, 35),
                 'clicked': pygame.Color(85, 85, 85)
                 }


class _Load:
    def __init__(self, directory: str, *accept: str):
        """
        Loads in files from specified directories.
        Allows for filering accepted files by file extension.


        Args:
            directory: Directory storing all the files to load.
            accept: Tuple of file endings to look for.
        """
        self.files = {}
        for file in os.listdir(directory):
            name, ext = os.path.splitext(file)
            if ext.lower() in accept:
                self.process_file(file, name, directory)

    def process_file(self, file: str, name: str, directory: str):
        """
        Adds the given file to the dictionary.

        Args:
            file: The file to be added to the dictionary.
            name: The name of the file to be used in the dictionary.
            directory: The path where the file is stored.
        """
        self.files[name] = os.path.join(directory, file)

    def __call__(self) -> dict[str, str]:
        """Returns: A dictionary of file names pointing to their directories."""
        return self.files


class _LoadImages(_Load):
    def __init__(self,
                 directory: str,
                 accept: tuple[str] = (".png", ".jpeg", ".jpg")):
        super().__init__(directory, *accept)

    @override
    def process_file(self, file: str, name: str, directory: str):
        image = pygame.image.load(os.path.join(directory, file))
        if image.get_alpha():
            image = image.convert_alpha()
        else:
            image = image.convert()
        self.files[name] = image


class Validator(ABC):

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


FONTS = _Load(os.path.join("resources", "fonts"), ".ttf")
BACKGROUNDS = _LoadImages(os.path.join("resources", "graphics", "backgrounds"))
ICONS = _LoadImages(os.path.join("resources", "graphics", "icons"))
