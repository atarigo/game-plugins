import pygame

from plugins.core import EventManager
from plugins.ui import UI


class CharacterPanel(UI):
    def __init__(self, event_manager: EventManager):
        super().__init__(event_manager)

        self.font = pygame.font.Font(None, 24)

    def render(self, screen: pygame.Surface):
        rect = pygame.Rect(400, 100, 200, 200)
        pygame.draw.rect(screen, (255, 0, 255), rect)

        text = self.font.render("Character Panel", True, (255, 255, 255))
        screen.blit(text, (450, 150))
