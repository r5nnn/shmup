"""Module for saving and loading game config file."""
import json
from pathlib import Path

import pygame


def save(data: dict, directory: Path) -> None:
    directory.touch()
    with directory.open("w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4)


def load(directory: Path, default_config: dict) -> dict:
    directory.touch()
    with directory.open(encoding="UTF-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            save(default_config, directory)
            return default_config


def validate_config(data: dict, default_config: dict) -> dict:
    if default_config.keys() == data.keys():
        pass
    elif len(default_config) > len(data):
        missing_keys = default_config.keys() - data.keys()
        for key in missing_keys:
            data[key] = default_config[key]
    else:
        invalid_keys = data.keys() - default_config.keys()
        for key in invalid_keys:
            del data[key]
    return data


_default_config = {
    "flags": {
        "fullscreen": True,
        "noframe": True,
    },
}
_config_dir = Path("config.json")
config = validate_config(load(_config_dir, _default_config), _default_config)
# volatile global data
system_data = {
    "flags": pygame.SCALED,
    "dt": 1.0,
}
