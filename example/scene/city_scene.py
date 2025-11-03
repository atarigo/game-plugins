from datetime import datetime

import pygame

from plugins.core import EventManager
from plugins.scene import Scene, SceneEvent


class CityScene(Scene):
    def __init__(self, event_manager: EventManager):
        super().__init__(event_manager)

        self.font = pygame.font.Font(None, 64)

        self.now = datetime.now()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.event_manager.emit(SceneEvent.SwitchTo, "Menu")
            elif event.key == pygame.K_s:
                self.event_manager.emit(SceneEvent.Append, "CityStore")

    def update(self, dt: float):
        self.now = datetime.now()

    def render(self, screen: pygame.Surface):
        title = self.font.render(f"City {self.now.isoformat()}", True, (255, 255, 255))
        screen.blit(title, (300, 100))
