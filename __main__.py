#!/usr/bin/env python3
"""Script that opens the game."""
import sys
import pygame
import src

if __name__ == "__main__":
    src.main.gameloop()
    pygame.quit()
    sys.exit()
