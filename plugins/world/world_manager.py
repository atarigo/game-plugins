from enum import Enum
from typing import Optional, TypedDict

import pygame
import structlog

from plugins.core import EventManager, GameNode

from .components import Position, Sprite, Velocity
from .systems import RenderSystem
from .world_component_manager import WorldComponentManager

logger = structlog.get_logger()


class WorldEvent(Enum):
    AddSystems = "AddSystems"
    AddEntities = "AddEntities"


SYSTEM = {
    "RenderSystem": RenderSystem,
}

COMPONENT = {
    "Position": Position,
    "Velocity": Velocity,
    "Sprite": Sprite,
}


class WorldEventData(TypedDict):
    systems: Optional[list[str]]
    entities: Optional[list[dict]]


class WorldManagerEventHandlers:
    component_manager: WorldComponentManager

    def add_systems(self, data: WorldEventData):
        logger.debug("[world]", action="add_systems", data=data)

        for system in data["systems"]:
            if cls := SYSTEM.get(system, None):
                self.systems.add(cls(self.event_manager, self.component_manager))

    def add_entities(self, data: WorldEventData):
        logger.debug("[world]", action="add_entities", data=data)

        """
        data["entities"] = [
            {
                "components": {
                    "Sprite": {
                    },
                    "Position": {
                        "x": 0,
                        "y": 0,
                    },
                    "Velocity": {
                        "dx": 0,
                        "dy": 0,
                    },
                },
            },
            ...,
        ]
        """
        for entity in data["entities"]:
            entity_id = self.component_manager.create_entity()
            for comp_name, comp_data in entity["components"].items():
                comp_cls = COMPONENT.get(comp_name, None)
                if comp_cls:
                    self.component_manager.add_component(
                        entity_id, comp_cls(**comp_data)
                    )


class WorldManager(GameNode, WorldManagerEventHandlers):
    def __init__(self, event_manager: EventManager):
        super().__init__()

        self.event_manager = event_manager
        self.event_manager.subscribe(WorldEvent.AddSystems, self.add_systems)
        self.event_manager.subscribe(WorldEvent.AddEntities, self.add_entities)

        self.component_manager = WorldComponentManager()
        self.systems = set()

    def handle_event(self, event: pygame.event.Event):
        for system in self.systems:
            system.handle_event(event)

    def update(self, dt: float):
        for system in self.systems:
            system.update(dt)

    def render(self, screen: pygame.Surface):
        for system in self.systems:
            system.render(screen)
