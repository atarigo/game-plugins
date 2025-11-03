from datetime import datetime

import pygame

from example.ui import CharacterPanel, InventoryPanel
from plugins.core import EventManager
from plugins.scene import Scene, SceneEvent
from plugins.ui import UiEvent


class CityScene(Scene):
    def __init__(self, event_manager: EventManager):
        super().__init__(event_manager)

        self.event_manager.emit(
            UiEvent.Register, {"name": "Inventory", "cls": InventoryPanel}
        )
        self.event_manager.emit(
            UiEvent.Register, {"name": "Character", "cls": CharacterPanel}
        )

        self.font = pygame.font.Font(None, 64)

        self.now = datetime.now()

    def __del__(self):
        self.event_manager.emit(UiEvent.Unregister, {"name": "Inventory"})
        self.event_manager.emit(UiEvent.Unregister, {"name": "Character"})

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.event_manager.emit(UiEvent.Pop)
            elif event.key == pygame.K_i:
                self.event_manager.emit(UiEvent.Toggle, {"name": "Inventory"})
            elif event.key == pygame.K_c:
                self.event_manager.emit(UiEvent.Toggle, {"name": "Character"})
            elif event.key == pygame.K_s:
                self.event_manager.emit(SceneEvent.Append, "CityStore")
            elif event.key == pygame.K_q:
                self.event_manager.emit(SceneEvent.SwitchTo, "Menu")

    def update(self, dt: float):
        self.now = datetime.now()

    def render(self, screen: pygame.Surface):
        title = self.font.render(f"City {self.now.isoformat()}", True, (255, 255, 255))
        screen.blit(title, (300, 100))
