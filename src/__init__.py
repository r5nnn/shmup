"""Contains all the game's source code."""
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s:%(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)
logger.debug("Started logging.")

from src.core import prepare, main
