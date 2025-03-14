"""Contains all the game's source code."""
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s:%(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.debug("Started logging.")

from src.core import prepare, main
