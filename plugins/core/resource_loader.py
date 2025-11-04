from functools import lru_cache

import pygame
import structlog

logger = structlog.getLogger(__name__)


@lru_cache(maxsize=50)
def load_image(path: str) -> pygame.Surface:
    logger.debug("[Loader]", action="image", path=path)

    return pygame.image.load(path).convert_alpha()


@lru_cache(maxsize=50)
def load_sound(path: str) -> pygame.Sound:
    logger.debug("[Loader]", action="sound", path=path)

    return pygame.mixer.Sound(path)


@lru_cache(maxsize=50)
def load_font(size: int) -> pygame.Font:
    logger.debug("[Loader]", action="font", size=size)

    return pygame.font.Font(None, size)
