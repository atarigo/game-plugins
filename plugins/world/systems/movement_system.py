from plugins.core import EventManager, GameNode

from ..components import Position, Velocity
from ..world_component_manager import WorldComponentManager

SPEED = 100


class MovementSystem(GameNode):
    def __init__(
        self, event_manager: EventManager, world_manager: WorldComponentManager
    ):
        super().__init__()

        self.event = event_manager
        self.world = world_manager

    def update(self, dt: float) -> None:
        for entity_id in self.world.get_entities_with(Position, Velocity):
            position = self.world.get_component(entity_id, Position)
            velocity = self.world.get_component(entity_id, Velocity)

            position.x += velocity.dx * dt * SPEED
            position.y += velocity.dy * dt * SPEED
