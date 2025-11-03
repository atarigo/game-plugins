import pygame

from plugins.core import EventManager, GameNode

from .ui import UI
from .ui_state import UiStateManager


class UiManager(GameNode):
    def __init__(self, event_manager: EventManager):
        super().__init__()

        self.event_manager = event_manager

        self.state = UiStateManager(event_manager)

    @property
    def children(self) -> list[UI]:
        return self.state.children

    def register(self, ui_name: str, ui: type[UI]):
        self.state.register(ui_name, ui)

    def handle_event(self, event: pygame.event.Event):
        for child in self.children:
            child.handle_event(event)

    def update(self, dt: float):
        for child in self.children:
            child.update(dt)

    def render(self, screen: pygame.Surface):
        for child in self.children:
            child.render(screen)
