from plugins.core import EventManager, GameNode


class Scene(GameNode):
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.paused = False
