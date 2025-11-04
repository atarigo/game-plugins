from dataclasses import dataclass
from enum import Enum

import pygame

from plugins.core.resource_loader import load_sound


class AttackType(Enum):
    Ranged = "Ranged"


@dataclass
class Attack:
    # 可在 JSON 中設定的參數,給預設值
    type: str = "Ranged"  # AttackType enum 值
    sound_path: str = ""
    cooldown: float = 0.5  # 攻擊冷卻時間(秒)
    duration: float = 0.3  # 攻擊動作時長(秒),沒有動畫時使用此值
    projectile_speed: float = 150.0  # 投射物速度(像素/秒)

    # 內部使用的參數
    sound: pygame.Sound = None
    cooldown_timer: float = 0.0

    # 攻擊狀態
    is_attacking: bool = False  # 是否正在攻擊中
    attack_duration: float = 0.0  # 當前攻擊剩餘時間(動態計算)

    def __post_init__(self):
        # 將字串轉換為 AttackType enum
        if isinstance(self.type, str):
            self.type = AttackType(self.type)

        # 只在有音效路徑時才載入
        if self.sound is None and self.sound_path:
            try:
                self.sound = load_sound(self.sound_path)
            except Exception as e:
                # 如果載入失敗,印出錯誤但繼續執行
                print(f"警告: 無法載入音效 {self.sound_path}: {e}")
                self.sound = None


@dataclass
class AttackSprite:
    image: pygame.Surface = None
    width: int = 0
    height: int = 0

    def __post_init__(self):
        if self.image is None:
            self.image = pygame.Surface((3, 3))
            self.image.fill((255, 255, 255))

        if self.width == 0:
            self.width = self.image.get_width()
        if self.height == 0:
            self.height = self.image.get_height()
