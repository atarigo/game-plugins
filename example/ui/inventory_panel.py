import pygame

from plugins.core import EventManager
from plugins.ui import UI


class InventoryPanel(UI):
    def __init__(self, event_manager: EventManager):
        super().__init__(event_manager)

        self.font = pygame.font.Font(None, 24)

    def render(self, screen: pygame.Surface):
        rect = pygame.Rect(100, 100, 200, 200)
        pygame.draw.rect(screen, (0, 255, 255), rect)

        text = self.font.render("Inventory Panel", True, (255, 255, 255))
        screen.blit(text, (150, 150))
