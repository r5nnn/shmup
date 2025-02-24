import json
from pathlib import Path

data = {
    "fullscreen": True,
    "borderless": True,
}
data_dir = Path("data.json")


def save():
    try:
        file = Path.open(data_dir, encoding="UTF-8")
    except FileNotFoundError:
        data_dir.touch()
    json.dumps(data)
