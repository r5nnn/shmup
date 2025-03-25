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
    model_config = ConfigDict(extra="ignore")

    def save(self, directory: Path) -> None:
        directory.touch()
        with directory.open("w") as file:
            file.write(self.model_dump_json())
        logger.info(
            "Saved current settings into %s file: %s.", directory, self
        )

    @classmethod
    def load(cls, directory: Path) -> tuple[FileModel, bool]:
        """Load a dict from a json file."""
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
                        "File: %s empty. Saving with defaults.", directory
                    )
                default_settings.save(directory)
                return default_settings, True


class Settings(FileModel):
    flags: dict[str, bool] = {"fullscreen": True, "noframe": True}
    resolution: tuple[int, int] = (1920, 1080)
    non_int_scaling: bool = True
    non_native_ratio: bool = False
    keep_mouse_pos: bool = True
    fps: int = 165


@dataclass(kw_only=True)
class SystemData:
    flags: int = pygame.SCALED
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
    scale_factor: list[float] | float = ...


system_data = SystemData()
config_dir = Path("config.json")
settings, system_data.default_config = Settings.load(config_dir)
