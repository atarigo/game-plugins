from dataclasses import dataclass
from random import randint

import pygame


@dataclass
class Sprite:
    image: pygame.Surface = None
    width: int = 0
    height: int = 0

    def __post_init__(self):
        if self.image is None:
            self.image = pygame.Surface((10, 10))
            self.image.fill((randint(0, 255), randint(0, 255), randint(0, 255)))

        if self.width == 0:
            self.width = self.image.get_width()
        if self.height == 0:
            self.height = self.image.get_height()
