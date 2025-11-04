import pygame

from plugins.core import EventManager, GameNode

from ..components import PlayerTag, Velocity
from ..world_component_manager import WorldComponentManager


class PlayerControlSystem(GameNode):
    def __init__(
        self, event_manager: EventManager, world_manager: WorldComponentManager
    ):
        super().__init__()

        self.event = event_manager
        self.world = world_manager

    def handle_event(self, event: pygame.event.Event) -> None:
        """處理按鍵事件 (攻擊觸發)"""
        from .attack_system import AttackEvent

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # 空白鍵觸發攻擊
                for entity_id in self.world.get_entities_with(PlayerTag):
                    self.event.emit(AttackEvent.Trigger, {"trigger_id": entity_id})

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        for entity_id in self.world.get_entities_with(PlayerTag, Velocity):
            dx = dy = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = 1
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = 1

            magnitude = (dx**2 + dy**2) ** 0.5
            if magnitude > 0:
                dx = dx / magnitude
                dy = dy / magnitude

            velocity = self.world.get_component(entity_id, Velocity)
            velocity.dx = dx
            velocity.dy = dy
