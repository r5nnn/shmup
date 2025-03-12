"""Module for saving and loading game config file."""

import json
from dataclasses import dataclass
from pathlib import Path

import pygame
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.components import Audio
from src.core.load import Load


class Flags(BaseModel):
    fullscreen: bool = True
    noframe: bool = True


class Settings(BaseSettings):
    flags: Flags = Flags()
    keep_mouse_pos: bool = True

    model_config = SettingsConfigDict(extra="ignore")


@dataclass(kw_only=True)
class SystemData:
    flags: int = pygame.SCALED
    dt: float = 1.0
    quit: bool = False
    version: str = "0.0.3"
    version_type: str = "prototype"
    # Defined when prepare.py is ran.
    screen_rect: pygame.Rect = ...
    window: pygame.Surface = ...
    window_rect: pygame.Rect = ...
    image_paths: Load = ...
    audio_paths: Load = ...
    font_paths: Load = ...
    background_audio: Audio = ...
    button_audio: Audio = ...


def save(data: Settings, directory: Path) -> None:
    """Save a dictionary to a json file.

    :param data: Dictionary to save.
    :param directory: Directory in which to save file to. If file doesn't
    already exist it is created, otherwise any previous data stored is
    overriden.
    """
    directory.touch()
    with directory.open("w") as file:
        file.write(data.model_dump_json())


def load(directory: Path, data: Settings) -> Settings:
    """Load a dict from a json file.

    :param directory: The path to the json file.
    :param data: The default data of the file. Used if the file
    doesn't exist, is empty or unreadable.
    """
    directory.touch()
    with directory.open() as file:
        try:
            file_data = json.load(file)
            data.model_validate(file_data)
            print(data)
        except json.decoder.JSONDecodeError:
            save(data, directory)
            return data
        return Settings(**file_data)


config_dir = Path("config.json")
settings = load(config_dir, Settings())
system_data = SystemData()
print(settings)