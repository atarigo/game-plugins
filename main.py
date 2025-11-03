import structlog

from plugins.core.logger_config import configure

logger = structlog.getLogger(__name__)


def main():
    configure()

    logger.debug("Hello from game-plugins!")


if __name__ == "__main__":
    main()
