"""Module for saving and loading game config file."""

import json
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pygame
from pydantic import BaseModel, ConfigDict, ValidationError

from src.components import Audio
from src.core.load import Load


class Settings(BaseModel):
    flags: dict[Literal["fullscreen", "noframe"], bool] = {"fullscreen": True,
                                                           "noframe": True}
    keep_mouse_pos: bool = True

    model_config = ConfigDict(extra="ignore")


    def save(self) -> None:
        config_dir.touch()
        with config_dir.open("w") as file:
            file.write(self.model_dump_json())


    @classmethod
    def load(cls) -> "Settings":
        """Load a dict from a json file.

        :param directory: The path to the json file.
        """
        config_dir.touch()
        with config_dir.open() as file:
            try:
                file_data = json.load(file)
                return cls.model_validate(file_data)
            except (json.decoder.JSONDecodeError, ValidationError) as e:
                warnings.warn(f"Config file corrupted. Using defualts. Error {e}",
                              stacklevel=2)
                backup_path = config_dir.with_suffix(".backup.json")
                config_dir.rename(backup_path)  # Backup the corrupted file
                default_settings = cls()
                default_settings.save()
                return default_settings


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


config_dir = Path("config.json")
settings = Settings.load()
system_data = SystemData()
