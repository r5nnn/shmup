#!/usr/bin/env python3
"""Script that opens the game."""
import sys
import pygame
from src import main, title, options, game

if __name__ == "__main__":
    states = {"title": title.Title,
              "options": options.Options,
              "game": game.Game}
    main.init(states, "title")
    main.gameloop()
    pygame.quit()
    sys.exit()
