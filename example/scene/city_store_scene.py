import pygame

from plugins.core import EventManager
from plugins.scene import Scene
from plugins.ui import UiEvent


class CityStoreScene(Scene):
    def __init__(self, event_manager: EventManager):
        super().__init__(event_manager)

        self.font = pygame.font.Font(None, 72)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.event_manager.emit(UiEvent.Toggle, {"name": "Inventory"})
            elif event.key == pygame.K_ESCAPE:
                self.event_manager.emit(UiEvent.Pop)

    def render(self, screen: pygame.Surface):
        title = self.font.render("Store", True, (255, 255, 255))
        screen.blit(title, (300, 300))
