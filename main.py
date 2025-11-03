import pygame
import structlog

from example.scene import CityScene, CityStoreScene, MenuScene
from plugins.client import GameClient
from plugins.core import EventManager
from plugins.core.logger_config import configure
from plugins.scene import SceneEvent, SceneManager
from plugins.ui import UiManager
from plugins.world import WorldManager

logger = structlog.getLogger(__name__)


def prepare():
    pygame.init()
    pygame.display.set_caption("Game")
    pygame.display.set_mode((800, 600))


def main():
    configure()

    prepare()

    event_manager = EventManager()

    scene_manager = SceneManager(event_manager=event_manager)
    scene_manager.register("Menu", MenuScene)
    scene_manager.register("City", CityScene)
    scene_manager.register("CityStore", CityStoreScene)

    ui_manager = UiManager(event_manager=event_manager)
    world_manager = WorldManager(event_manager=event_manager)

    try:
        event_manager.emit(SceneEvent.SwitchTo, "Menu")

        screen = pygame.display.get_surface()
        client = GameClient(
            screen, event_manager, scene_manager, ui_manager, world_manager
        )
        client.run()
    finally:
        event_manager.clear()
        pygame.quit()


if __name__ == "__main__":
    main()
