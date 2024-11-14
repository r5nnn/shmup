"""Package containing all the entities for the game."""
from data.components.entities.player import Player, Remi
from data.components.entities.entityutils import EntityGroup
from data.components.entities.collisionmanager import update_collisions

__all__ = ["Player", "Remi", "EntityGroup", "update_collisions"]
