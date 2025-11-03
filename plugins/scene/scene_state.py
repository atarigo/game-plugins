from enum import Enum

from plugins.core import EventManager

from .scene import Scene


class SceneEvent(Enum):
    SwitchTo = "SwitchTo"


class SceneStateManager:
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.event_manager.subscribe(SceneEvent.SwitchTo, self.switch_to)

        self.registry: dict[str, type[Scene]] = {}

        self.children: list[Scene] = []

    def register(self, scene_name: str, scene: type[Scene]):
        self.registry[scene_name] = scene

    def switch_to(self, scene_name: str):
        scene_class = self.registry.get(scene_name)
        if scene_class:
            self.children.clear()
            self.children.append(scene_class(self.event_manager))
