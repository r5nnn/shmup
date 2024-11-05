import json
import logging
import os

import pygame

pygame.init()
pygame.display.set_caption("shmup")
pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)

sources_root = os.path.abspath('.')

screen = pygame.display.get_surface()
screen_size = screen.get_size()
screen_center = tuple(round(coordinate / 2) for coordinate in screen_size)
screen_rect = screen.get_rect()

logging.basicConfig(level=logging.WARNING,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%d/%m/%Y %H:%M:%S",)

def parse_spritesheet(sprite_sheet: str) -> list[pygame.Surface]:
    spritesheet = pygame.image.load(sprite_sheet).convert_alpha()
    sprite_name = os.path.splitext(sprite_sheet)[0]
    metadata = sprite_name + '.json'
    try:
        metadata_json = open(metadata, encoding='UTF-8')
    except OSError:
        raise OSError(f'Could not open/read file: {metadata}')
    with metadata_json:
        data = json.load(metadata_json)
    metadata_json.close()
    sprite_list = []
    for sprite in (frames := data["frames"]):
        res = frames[sprite]["frame"]
        sprite_list.append(spritesheet.subsurface(res['x'], res['y'],
                                                  res['w'], res['h']))
    return sprite_list


class Load:
    def __init__(self, directory: str, *accept: str,
                 exclude_dirs: list[str] = None):
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
        return self.files[name]


class LoadSprites:
    def __init__(self, directory: str):
        self.files = {}
        for path, dirs, files in os.walk(directory):
            for file in files:
                name, ext = os.path.splitext(file)
                if ext.lower() == '.png' and os.path.isfile(os.path.join(
                        path, name + ".json")):
                    path1 = os.path.join(path, file)
                    image = parse_spritesheet(path1)
                    self.files[name] = image

    def __call__(self, name: str) -> list[pygame.Surface]:
        return self.files[name]


image_paths = Load(os.path.join(sources_root, 'resources', 'graphics'), '.png')
audio_paths = Load(os.path.join(sources_root, 'resources', 'audio'), '.wav')
font_paths = Load(os.path.join(sources_root, 'resources', 'fonts'), '.ttf')
sprites = LoadSprites(os.path.join(sources_root, 'resources', 'graphics'))
