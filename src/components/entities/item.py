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
    def __init__(self, speed: int, *args, acceleration: float = 500,
                 max_speed: int | None = 100, **kwargs):
        self.speed = speed
        super().__init__(*args, **kwargs)
        self.acceleration = acceleration
        self.max_speed = max_speed
        self.current_speed = self.speed

    def update(self) -> None:
        super().update()
        self.current_speed += self.acceleration * system_data.dt
        if self.max_speed is not None:
            self.current_speed = min(self.current_speed, self.max_speed)
        self.abs_rect.move_ip(0, self.current_speed * system_data.dt)
