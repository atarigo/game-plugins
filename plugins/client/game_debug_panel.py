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

        # Section: Scene Manager
        section_title = self.font_normal.render(
            "Scene Manager", True, (255, 200, 200)
        )
        screen.blit(section_title, (info_box_x + 15, y_offset))
        y_offset += 25

        # Registered scenes
        registered_scenes = list(scene_manager.state.registry.keys())
        reg_text = self.font_small.render(
            f"Registered: {len(registered_scenes)}", True, (250, 250, 250)
        )
        screen.blit(reg_text, (info_box_x + 20, y_offset))
        y_offset += 20

        # List registered scenes
        for scene_name in registered_scenes:
            scene_text = self.font_small.render(
                f"  - {scene_name}", True, (220, 220, 220)
            )
            screen.blit(scene_text, (info_box_x + 25, y_offset))
            y_offset += 18

        y_offset += 5

        # Active scenes
        active_scenes = scene_manager.children
        active_text = self.font_small.render(
            f"Active: {len(active_scenes)}", True, (250, 250, 250)
        )
        screen.blit(active_text, (info_box_x + 20, y_offset))
        y_offset += 20

        # List active scenes
        for scene in active_scenes:
            scene_class_name = scene.__class__.__name__
            status = " (paused)" if scene.paused else ""
            scene_text = self.font_small.render(
                f"  - {scene_class_name}{status}", True, (220, 220, 220)
            )
            screen.blit(scene_text, (info_box_x + 25, y_offset))
            y_offset += 18

        y_offset += 10

        # Section: UI Manager
        section_title = self.font_normal.render("UI Manager", True, (255, 200, 200))
        screen.blit(section_title, (info_box_x + 15, y_offset))
        y_offset += 25

        # Registered UIs
        registered_uis = list(ui_manager.state.registry.keys())
        reg_ui_text = self.font_small.render(
            f"Registered: {len(registered_uis)}", True, (250, 250, 250)
        )
        screen.blit(reg_ui_text, (info_box_x + 20, y_offset))
        y_offset += 20

        # List registered UIs
        for ui_name in registered_uis:
            ui_text = self.font_small.render(
                f"  - {ui_name}", True, (220, 220, 220)
            )
            screen.blit(ui_text, (info_box_x + 25, y_offset))
            y_offset += 18

        y_offset += 5

        # Active UIs
        active_uis = ui_manager.children
        active_ui_text = self.font_small.render(
            f"Active: {len(active_uis)}", True, (250, 250, 250)
        )
        screen.blit(active_ui_text, (info_box_x + 20, y_offset))
        y_offset += 20

        # List active UIs
        for ui in active_uis:
            ui_class_name = ui.__class__.__name__
            ui_text = self.font_small.render(
                f"  - {ui_class_name}", True, (220, 220, 220)
            )
            screen.blit(ui_text, (info_box_x + 25, y_offset))
            y_offset += 18
