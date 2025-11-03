import time
from enum import Enum

from plugins.core import EventManager


class GameEvent(Enum):
    Pause = "Pause"
    Resume = "Resume"
    Quit = "Quit"


class GameState(Enum):
    Running = "Running"
    Paused = "Paused"
    Saving = "Saving"
    Quitting = "Quitting"


class GameStateManager:
    def __init__(self, event_manager: EventManager):
        self.current = GameState.Running

        self.event_manager = event_manager
        self.event_manager.subscribe(GameEvent.Pause, self.pause)
        self.event_manager.subscribe(GameEvent.Resume, self.resume)
        self.event_manager.subscribe(GameEvent.Quit, self.quit)

    def pause(self):
        if self.current == GameState.Running:
            self.current = GameState.Paused

    def resume(self):
        if self.current == GameState.Paused:
            self.current = GameState.Running

    def quit(self):
        if self.current == GameState.Saving:
            time.sleep(0.5)
            self.event_manager.emit(GameEvent.Quit)
        else:
            self.current = GameState.Quitting
