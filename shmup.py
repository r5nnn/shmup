"""This script boots the game by loading all the game's modules."""
import sys
import pygame
from data.core.main import main


if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
