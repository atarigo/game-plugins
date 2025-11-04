from dataclasses import dataclass, field
from enum import Enum

import pygame


class AnimationState(Enum):
    """角色動畫狀態"""

    IDLE = "idle"
    WALK = "walk"
    ATTACK = "attack"


@dataclass
class AnimationFrame:
    """單一動畫影格"""

    image: pygame.Surface
    duration: float  # 秒


@dataclass
class Animation:
    """動畫組件 - 管理角色的多個動畫狀態"""

    # 所有動畫狀態的 frames
    # 格式: {AnimationState.IDLE: [frame1, frame2, ...], ...}
    animations: dict[AnimationState, list[AnimationFrame]] = field(default_factory=dict)

    # 當前狀態
    current_state: AnimationState = AnimationState.IDLE
    # 當前 frame index
    current_frame: int = 0
    # 當前 frame 已播放時間
    elapsed_time: float = 0.0

    # 是否循環播放
    loop: bool = True
    # 動畫是否播放完成 (對於非循環動畫)
    finished: bool = False

    def get_current_image(self) -> pygame.Surface | None:
        """取得當前應顯示的圖片"""
        if self.current_state not in self.animations:
            return None

        frames = self.animations[self.current_state]
        if not frames or self.current_frame >= len(frames):
            return None

        return frames[self.current_frame].image

    def set_state(self, state: AnimationState, reset: bool = True):
        """切換動畫狀態"""
        if self.current_state == state and not reset:
            return

        self.current_state = state
        if reset:
            self.current_frame = 0
            self.elapsed_time = 0.0
            self.finished = False

    def add_animation(self, state: AnimationState, frames: list[AnimationFrame]):
        """新增一組動畫"""
        self.animations[state] = frames


@dataclass
class Direction:
    """角色朝向 (用於翻轉 sprite)"""

    facing_right: bool = True  # True = 右, False = 左
