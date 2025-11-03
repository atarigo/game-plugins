import pygame

from plugins.core import EventManager, GameNode

from .scene import Scene
from .scene_state import SceneStateManager


class SceneManager(GameNode):
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager

        self.state = SceneStateManager(event_manager)

    @property
    def children(self) -> list[Scene]:
        return self.state.children

    def register(self, scene_name: str, scene: Scene):
        self.state.register(scene_name, scene)

    def handle_event(self, event: pygame.event.Event):
        for child in self.children:
            child.handle_event(event)

    def update(self, dt: float):
        for child in self.children:
            child.update(dt)

    def render(self, screen: pygame.Surface):
        for child in self.children:
            child.render(screen)
