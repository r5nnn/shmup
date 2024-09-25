from . import control
from .states import title


def main():
    state_dict = {
        "Title": title.Title
    }
    game = control.Control(state_dict, "Title")
    game.main()
