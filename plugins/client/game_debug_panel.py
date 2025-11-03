import pygame

from plugins.core import GameNode
from plugins.scene import SceneManager
from plugins.ui import UiManager


class DebugPanel(GameNode):
    def __init__(self):
        super().__init__()

        self.font_small = pygame.font.Font(None, 18)
        self.font_normal = pygame.font.Font(None, 20)
        self.fps = 0.0

    def update(self, dt: float):
        if dt > 0:
            self.fps = 1.0 / dt

    def render(
        self, screen: pygame.Surface, scene_manager: SceneManager, ui_manager: UiManager
    ):
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Create semi-transparent light red background
        panel_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (255, 230, 230, 40), panel_surface.get_rect())
        screen.blit(panel_surface, (0, 0))

        # Display "debug mode" text in top-left corner
        debug_text = self.font_small.render("debug mode", True, (200, 100, 100))
        screen.blit(debug_text, (10, 10))

        # Info box on the right side
        info_box_width = 250
        info_box_height = screen_height - 40
        info_box_x = screen_width - info_box_width - 20
        info_box_y = 20

        # Draw info box with light background and transparency
        info_box_surface = pygame.Surface(
            (info_box_width, info_box_height), pygame.SRCALPHA
        )
        pygame.draw.rect(
            info_box_surface,
            (255, 240, 240, 40),
            info_box_surface.get_rect(),
            border_radius=5,
        )
        pygame.draw.rect(
            info_box_surface,
            (255, 200, 200, 80),
            info_box_surface.get_rect(),
            2,
            border_radius=5,
        )
        screen.blit(info_box_surface, (info_box_x, info_box_y))

        # Reserved space for debug information (to be added from top to bottom)
        y_offset = info_box_y + 15

        # Display FPS
        fps_text = self.font_normal.render(
            f"FPS: {self.fps:.1f}", True, (250, 250, 250)
        )
        screen.blit(fps_text, (info_box_x + 15, y_offset))
        y_offset += 30
