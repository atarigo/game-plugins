from plugins.core import EventManager, GameNode


class UI(GameNode):
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager

    def __hash__(self):
        return hash(self.__class__.__name__)

    def __eq__(self, other):
        return isinstance(other, UI) and self.__hash__() == other.__hash__()
