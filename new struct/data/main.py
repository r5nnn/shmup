import pygame

from . import tools
from .states import title


def main():
    state_dict = {
        "Title": title.Title()
    }
    game = tools.Control(state_dict, "Title")
    game.main()
