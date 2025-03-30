from __future__ import annotations

from typing import override

from src.components.entities.entity import Entity
from src.core import system_data


class Item(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "item"

    @override
    def update(self) -> None:
        super().update()
        if not system_data.abs_window_rect.contains(self.rect):
            self.kill()

    @override
    def on_collide(self, collided_entity: Entity) -> None:
        if collided_entity.type == "player":
            self.kill()

class FallingItem(Item):
    def __init__(self, speed: int, *args, **kwargs):
        self.speed = speed
        super().__init__(*args, **kwargs)

    def update(self) -> None:
        super().update()
        self.abs_rect.move_ip(0, self.speed * system_data.dt)
