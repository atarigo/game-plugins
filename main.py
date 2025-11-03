import pygame
import structlog

from plugins.client import GameClient
from plugins.core import EventManager
from plugins.core.logger_config import configure

logger = structlog.getLogger(__name__)


def prepare():
    pygame.init()
    pygame.display.set_caption("Game")
    pygame.display.set_mode((800, 600))


def main():
    configure()

    prepare()

    event_manager = EventManager()

    try:
        screen = pygame.display.get_surface()
        client = GameClient(screen, event_manager)
        client.run()
    finally:
        event_manager.clear()
        pygame.quit()


if __name__ == "__main__":
    main()
