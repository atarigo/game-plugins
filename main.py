import structlog

from plugins.client.game_state import GameStateManager
from plugins.core import EventManager
from plugins.core.logger_config import configure

logger = structlog.getLogger(__name__)


def main():
    configure()

    event_manager = EventManager()

    game_state = GameStateManager(event_manager)

    logger.debug("Hello from game-plugins!")


if __name__ == "__main__":
    main()
