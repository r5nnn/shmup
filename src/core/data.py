"""Module for saving and loading game config file."""

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import pygame
from pydantic import BaseModel, ConfigDict, ValidationError

from src.core.load import Load


logger = logging.getLogger("src.core")


class Settings(BaseModel):
    flags: dict[str, bool] = {"fullscreen": True, "noframe": True}
    resolution: tuple[int, int] = (1920, 1080)
    non_int_scaling: bool = True
    keep_mouse_pos: bool = True

    model_config = ConfigDict(extra="ignore")

    def save(self) -> None:
        config_dir.touch()
        with config_dir.open("w") as file:
            file.write(self.model_dump_json())
        logger.info("Saved current settings into config.json file: %s.", self)

    @classmethod
    def load(cls) -> tuple["Settings", bool]:
        """Load a dict from a json file."""
        config_dir.touch()
        with config_dir.open() as file:
            try:
                file_data = json.load(file)
                logger.info(
                    "Attempting to load existing config.json file with data: "
                    "%s.",
                    file_data,
                )
                return cls.model_validate(file_data), False
            except (json.decoder.JSONDecodeError, ValidationError) as e:
                backup_path = config_dir.with_suffix(".backup.json")
                config_dir.rename(backup_path)  # Backup the corrupted file
                default_settings = cls()
                if e == ValidationError:
                    logger.exception(
                        "Config file corrupted. Overwriting config with"
                        "defaults."
                    )
                else:
                    logger.info("Config file empty. Saving with default config.")
                default_settings.save()
                return default_settings, True


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
    scale_factor: float = ...


system_data = SystemData()
config_dir = Path("config.json")
settings, system_data.default_config = Settings.load()
