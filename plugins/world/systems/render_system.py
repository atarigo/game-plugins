import pygame

from plugins.core import EventManager, GameNode
from plugins.world.components import Position, Sprite

from ..world_component_manager import WorldComponentManager


class RenderSystem(GameNode):
    def __init__(
        self, event_manager: EventManager, world_manager: WorldComponentManager
    ):
        super().__init__()

        self.event = event_manager
        self.world = world_manager

        self.lable_font = pygame.font.Font(None, 24)

    def render(self, screen: pygame.Surface) -> None:
        for entity_id in self.world.get_entities_with(Position, Sprite):
            pos = self.world.get_component(entity_id, Position)
            sprite = self.world.get_component(entity_id, Sprite)

            # center align
            x = pos.x - sprite.width // 2
            y = pos.y - sprite.height // 2
            screen.blit(sprite.image, (x, y))

            # label
            """
            name_label = world.get_component(entity_id, NameLabel)
            if name_label:
                text = self.lable_font.render(name_label.value, True, (255, 255, 255))

                text_rect = text.get_rect(
                    midtop=(pos.x, pos.y + sprite.height // 2 + 8)
                )
                screen.blit(text, text_rect)
            """
