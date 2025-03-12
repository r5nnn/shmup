"""Contains all the game's source code."""
import logging

from src.core import prepare, main

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s:%(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
