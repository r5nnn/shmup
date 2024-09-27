from . import control
from .states import title, options


def main():
    states = {
        "title": title.Title,
        "options": options.Options
    }
    game = control.Control(states, "title")
    game.main()
