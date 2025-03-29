"""Module for saving and loading game config file."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import pygame
from pydantic import BaseModel, ConfigDict, ValidationError

logger = logging.getLogger("src.core")


class FileModel(BaseModel):
    """Base class for pydantic models saving and loading from json files."""

    model_config = ConfigDict(extra="ignore")
    def save(self, directory: Path) -> None:
        """Saves the current config into the json file of directory specified.

        The json file is created if it does not already exist, and the
        default config is saved to that file.
        """
        directory.touch()
        with directory.open("w") as file:
            file.write(self.model_dump_json())
        logger.info(
            "Saved current settings into %s file: %s.", directory, self
        )

    @classmethod
    def load(cls, directory: Path) -> tuple[FileModel, bool]:
        """Load a config dictionary from a json file into a pydantic object.

        The json file is created if it does not already exist. If the file is
        empty, loads the default config. If the file fails pydantic validation
        checks, the invalid config is saved as a .backup file, and the default
        config is loaded in its place.
        """
        directory.touch()
        with directory.open() as file:
            try:
                file_data = json.load(file)
                logger.info(
                    "Attempting to load existing file %s with data: %s.",
                    directory,
                    file_data,
                )
                return cls.model_validate(file_data), False
            except (json.decoder.JSONDecodeError, ValidationError) as e:
                default_settings = cls()
                if e == ValidationError:
                    backup_path = directory.with_suffix(".backup.json")
                    directory.rename(backup_path)  # Backup the corrupted file
                    logger.exception(
                        "Config file corrupted. Overwriting config with"
                        "defaults."
                    )
                else:
                    logger.info(
                        "File: %s empty. Saving and loading with defaults.", directory
                    )
                default_settings.save(directory)
                return default_settings, True


class Settings(FileModel):
    """Class containing settings that should be saved between sessions."""

    flags: dict[str, bool] = {"fullscreen": True, "noframe": True}
    resolution: tuple[int, int] = (1920, 1080)
    non_int_scaling: bool = True
    non_native_ratio: bool = False
    keep_mouse_pos: bool = True


@dataclass(kw_only=True)
class SystemData:
    """Dataclass containing globals that don't need to be saved."""

    flags: int = pygame.SCALED
    fps: int = 165
    dt: float = 1.0
    quit: bool = False
    version: str = "0.0.3"
    version_type: str = "prototype"
    # Defined when settings loaded.
    default_config: bool = ...
    # Defined when prepare.py is ran.
    window: pygame.Surface = ...
    window_rect: pygame.Rect = ...
    abs_window: pygame.Surface = ...
    abs_window_rect: pygame.Rect = ...
    screen_rect: pygame.Rect = ...
    scale_factor: tuple[float, float] = ...


system_data = SystemData()
config_dir = Path("config.json")
settings, system_data.default_config = Settings.load(config_dir)
