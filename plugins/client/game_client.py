import pygame

from plugins.core import EventManager
from plugins.scene import SceneManager
from plugins.ui import UiManager
from plugins.world import WorldManager

from .game_debug_panel import DebugPanel
from .game_state import GameEvent, GameState, GameStateManager


class GameClient:
    def __init__(
        self,
        screen: pygame.Surface,
        event_manager: EventManager,
        scene_manager: SceneManager,
        ui_manager: UiManager,
        world_manager: WorldManager,
    ):
        self.screen = screen
        self.event_manager = event_manager
        self.scene_manager = scene_manager
        self.ui_manager = ui_manager
        self.world_manager = world_manager

        self.state = GameStateManager(event_manager)
        self.clock = pygame.time.Clock()

        self.debug = False
        self.debug_panel = DebugPanel()

    def run(self):
        while self.state.current == GameState.Running:
            dt = self.clock.tick(60) / 1000.0

            self.handle_events()
            self.event_manager.process_events()
            self.update(dt)
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.event_manager.emit(GameEvent.Quit)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.debug = not self.debug

            self.scene_manager.handle_event(event)
            self.world_manager.handle_event(event)
            self.ui_manager.handle_event(event)

    def update(self, dt):
        self.scene_manager.update(dt)
        self.world_manager.update(dt)
        self.ui_manager.update(dt)

        if self.debug:
            self.debug_panel.update(dt)

    def render(self):
        self.screen.fill((0, 0, 0))

        self.scene_manager.render(self.screen)
        self.world_manager.render(self.screen)
        self.ui_manager.render(self.screen)

        if self.debug:
            self.debug_panel.render(
                self.screen, self.scene_manager, self.ui_manager, self.world_manager
            )

        pygame.display.flip()
