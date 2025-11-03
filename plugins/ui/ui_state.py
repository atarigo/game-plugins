from enum import Enum
from typing import Optional, TypedDict

import structlog

from plugins.core import EventManager
from plugins.scene import SceneEvent

from .ui import UI

logger = structlog.get_logger()


class UiEvent(Enum):
    Register = "Register"
    Unregister = "Unregister"

    Toggle = "Toggle"
    Pop = "Pop"


class UiEventData(TypedDict):
    name: str
    cls: Optional[type[UI]]


class UiStateManager:
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.event_manager.subscribe(UiEvent.Register, self.register)
        self.event_manager.subscribe(UiEvent.Unregister, self.unregister)
        self.event_manager.subscribe(UiEvent.Toggle, self.toggle)
        self.event_manager.subscribe(UiEvent.Pop, self.pop)

        self.registry: dict[str, type[UI]] = {}

        self.children: list[UI] = []

    def register(self, data: UiEventData):
        name = data.get("name")
        cls = data.get("cls")
        if name and cls:
            self.registry[name] = cls

        logger.debug("[UI]", action="register", name=name, cls=cls)

    def unregister(self, data: UiEventData):
        name = data.get("name")
        if name:
            del self.registry[name]

        logger.debug("[UI]", action="unregister", name=name)

    def toggle(self, data: UiEventData):
        ui_name = data.get("name")
        ui_class = self.registry.get(ui_name)
        if ui_class:
            ui = ui_class(self.event_manager)
            if ui in self.children:
                self.children.remove(ui)
            else:
                self.children.append(ui)

        logger.debug("[UI]", action="toggle", name=ui_name)

    def pop(self, data: UiEventData):
        if self.children:
            self.children.pop()
        else:
            self.event_manager.emit(SceneEvent.Pop)

        logger.debug("[UI]", action="pop")

    def clear(self):
        logger.debug("[UI]", action="clear")

        self.registry.clear()
