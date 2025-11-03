import pygame

from plugins.core import EventManager

from .game_state import GameEvent, GameState, GameStateManager


class GameClient:
    def __init__(self, screen: pygame.Surface, event_manager: EventManager):
        self.screen = screen
        self.event_manager = event_manager

        self.state = GameStateManager(event_manager)
        self.clock = pygame.time.Clock()

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

    def update(self, dt):
        pass

    def render(self):
        self.screen.fill((0, 0, 0))

        pygame.display.flip()
