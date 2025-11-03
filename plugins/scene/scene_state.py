from enum import Enum

import structlog

from plugins.core import EventManager

from .scene import Scene

logger = structlog.get_logger()


class SceneEvent(Enum):
    SwitchTo = "SwitchTo"
    Append = "Append"
    Pop = "Pop"


class SceneStateManager:
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.event_manager.subscribe(SceneEvent.SwitchTo, self.switch_to)
        self.event_manager.subscribe(SceneEvent.Append, self.append)
        self.event_manager.subscribe(SceneEvent.Pop, self.pop)

        self.registry: dict[str, type[Scene]] = {}

        self.children: list[Scene] = []

    def register(self, scene_name: str, scene: type[Scene]):
        self.registry[scene_name] = scene

        logger.debug("[Scene]", action="register", name=scene_name, cls=scene)

    def switch_to(self, scene_name: str):
        logger.debug("[Scene]", action="switch_to", name=scene_name)

        scene_class = self.registry.get(scene_name)
        if scene_class:
            self.children.clear()
            self.children.append(scene_class(self.event_manager))

    def append(self, scene_name: str):
        logger.debug("[Scene]", action="append", name=scene_name)

        scene_class = self.registry.get(scene_name)
        if scene_class:
            for child in self.children:
                child.paused = True
            self.children.append(scene_class(self.event_manager))

    def pop(self, *args, **kwargs):
        logger.debug("[Scene]", action="pop")

        if len(self.children) == 1:
            return

        if self.children:
            self.children.pop()

        if self.children:
            self.children[-1].paused = False
