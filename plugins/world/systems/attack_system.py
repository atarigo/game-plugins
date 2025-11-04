from enum import Enum

import pygame
import structlog

from plugins.core import EventManager, GameNode

from ..components import (
    Animation,
    AnimationState,
    Attack,
    AttackSprite,
    AttackType,
    Direction,
    Position,
    Velocity,
)
from ..world_component_manager import WorldComponentManager

logger = structlog.get_logger()


def spawn_projectile(
    world: "WorldComponentManager",
    attacker_id: int,
    projectile_speed: float,
) -> int | None:
    """
    生成投射物(子彈)

    Args:
        world: WorldComponentManager 實例
        attacker_id: 攻擊者的 entity ID
        projectile_speed: 子彈速度(像素/秒)

    Returns:
        子彈的 entity ID,如果生成失敗則返回 None
    """
    # 取得攻擊者的位置和朝向
    attacker_pos = world.get_component(attacker_id, Position)
    if not attacker_pos:
        return None

    # 取得朝向,如果沒有就預設向右
    direction = world.get_component(attacker_id, Direction)
    facing_right = direction.facing_right if direction else True

    # 建立子彈 entity
    projectile_id = world.create_entity()

    # 設定子彈位置(從攻擊者位置發射)
    world.add_component(projectile_id, Position(x=attacker_pos.x, y=attacker_pos.y))

    # 設定子彈速度(根據朝向)
    speed = projectile_speed if facing_right else -projectile_speed
    world.add_component(projectile_id, Velocity(dx=speed, dy=0))

    # 設定子彈外觀
    world.add_component(projectile_id, AttackSprite())

    logger.debug(
        "生成子彈",
        projectile_id=projectile_id,
        position=(attacker_pos.x, attacker_pos.y),
        speed=speed,
    )

    return projectile_id


class AttackEvent(Enum):
    Trigger = "Trigger"


class AttackSystem(GameNode):
    def __init__(
        self, event_manager: EventManager, world_manager: WorldComponentManager
    ):
        super().__init__()

        self.event = event_manager
        self.world = world_manager

        self.event.subscribe(AttackEvent.Trigger, self.trigger)

    def trigger(self, data: dict):
        """觸發攻擊"""
        trigger_id = data["trigger_id"]
        attack = self.world.get_component(trigger_id, Attack)

        # 檢查 entity 是否有 Attack component
        if not attack:
            logger.debug("攻擊失敗: entity 沒有 Attack component", entity_id=trigger_id)
            return

        # 檢查冷卻時間和是否已在攻擊中
        if attack.cooldown_timer > 0 or attack.is_attacking:
            logger.debug(
                "攻擊失敗: 冷卻中或攻擊中",
                entity_id=trigger_id,
                cooldown_timer=attack.cooldown_timer,
                is_attacking=attack.is_attacking,
            )
            return

        logger.info("🗡️ 攻擊觸發!", entity_id=trigger_id, attack_type=attack.type.value)

        # 播放攻擊音效
        if attack.sound:
            attack.sound.play()

        # 切換到攻擊動畫
        animation = self.world.get_component(trigger_id, Animation)
        if animation and AnimationState.ATTACK in animation.animations:
            animation.set_state(AnimationState.ATTACK, reset=True)
            animation.loop = False  # 攻擊動畫不循環

            # 計算攻擊動畫總時長
            attack_frames = animation.animations[AnimationState.ATTACK]
            attack.attack_duration = sum(frame.duration for frame in attack_frames)
            logger.debug("切換到攻擊動畫", duration=attack.attack_duration)
        else:
            # 沒有動畫時,使用 component 的 duration 設定
            attack.attack_duration = attack.duration
            logger.debug("沒有攻擊動畫,使用設定時長", duration=attack.attack_duration)

        # 標記為攻擊中
        attack.is_attacking = True
        attack.cooldown_timer = attack.cooldown

        # 生成攻擊物件(子彈/投射物)
        if attack.type == AttackType.Ranged:
            spawn_projectile(self.world, trigger_id, attack.projectile_speed)

    def update(self, dt: float) -> None:
        """更新攻擊狀態和冷卻時間"""
        for entity_id in self.world.get_entities_with(Attack):
            attack = self.world.get_component(entity_id, Attack)

            # 更新冷卻計時器
            if attack.cooldown_timer > 0:
                attack.cooldown_timer -= dt
                if attack.cooldown_timer < 0:
                    attack.cooldown_timer = 0

            # 檢查攻擊動畫是否播放完成
            if attack.is_attacking:
                animation = self.world.get_component(entity_id, Animation)

                # 有動畫:等待動畫播放完成
                if animation and AnimationState.ATTACK in animation.animations:
                    if animation.finished:
                        # 攻擊動畫結束,回到 idle 狀態
                        attack.is_attacking = False
                        animation.set_state(AnimationState.IDLE)
                        animation.loop = True
                        logger.debug("攻擊動畫完成", entity_id=entity_id)
                else:
                    # 沒有動畫:根據 attack_duration 計時
                    attack.attack_duration -= dt
                    if attack.attack_duration <= 0:
                        attack.is_attacking = False
                        logger.debug("攻擊完成(無動畫)", entity_id=entity_id)

    def render(self, screen: pygame.Surface) -> None:
        for entity_id in self.world.get_entities_with(AttackSprite, Position):
            attack_sprite = self.world.get_component(entity_id, AttackSprite)
            position = self.world.get_component(entity_id, Position)
            screen.blit(attack_sprite.image, (position.x, position.y))
