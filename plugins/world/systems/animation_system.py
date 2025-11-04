import pygame

from plugins.core import EventManager, GameNode

from ..components import Animation, Direction, Sprite, Velocity
from ..world_component_manager import WorldComponentManager


class AnimationSystem(GameNode):
    """處理動畫播放和 frame 更新"""

    def __init__(
        self, event_manager: EventManager, world_manager: WorldComponentManager
    ):
        super().__init__()

        self.event = event_manager
        self.world = world_manager

    def update(self, dt: float) -> None:
        """更新所有 entity 的動畫 frame"""
        for entity_id in self.world.get_entities_with(Animation):
            animation = self.world.get_component(entity_id, Animation)

            # 取得當前狀態的 frames
            if animation.current_state not in animation.animations:
                continue

            frames = animation.animations[animation.current_state]
            if not frames:
                continue

            # 更新時間
            animation.elapsed_time += dt

            # 取得當前 frame 的持續時間
            current_frame_duration = frames[animation.current_frame].duration

            # 檢查是否該切換到下一個 frame
            if animation.elapsed_time >= current_frame_duration:
                animation.elapsed_time = 0.0
                animation.current_frame += 1

                # 檢查是否播放完成
                if animation.current_frame >= len(frames):
                    if animation.loop:
                        animation.current_frame = 0
                    else:
                        animation.current_frame = len(frames) - 1
                        animation.finished = True

            # 更新 Sprite component 的圖片
            sprite = self.world.get_component(entity_id, Sprite)
            if sprite:
                current_image = animation.get_current_image()
                if current_image:
                    # 檢查是否需要翻轉圖片
                    direction = self.world.get_component(entity_id, Direction)
                    if direction and not direction.facing_right:
                        sprite.image = pygame.transform.flip(current_image, True, False)
                    else:
                        sprite.image = current_image

                    sprite.width = sprite.image.get_width()
                    sprite.height = sprite.image.get_height()

        # 自動根據 Velocity 更新動畫狀態和朝向
        self._update_movement_animation()

    def _update_movement_animation(self):
        """根據移動速度自動切換 idle/walk 動畫"""
        from ..components import AnimationState, Attack

        for entity_id in self.world.get_entities_with(Animation, Velocity):
            animation = self.world.get_component(entity_id, Animation)
            velocity = self.world.get_component(entity_id, Velocity)

            # 如果正在攻擊,不要切換動畫
            attack = self.world.get_component(entity_id, Attack)
            if attack and attack.is_attacking:
                continue

            # 根據速度切換動畫
            is_moving = abs(velocity.dx) > 0.01 or abs(velocity.dy) > 0.01

            if is_moving:
                if animation.current_state != AnimationState.WALK:
                    animation.set_state(AnimationState.WALK)
            else:
                if animation.current_state != AnimationState.IDLE:
                    animation.set_state(AnimationState.IDLE)

            # 更新朝向
            direction = self.world.get_component(entity_id, Direction)
            if direction and abs(velocity.dx) > 0.01:
                direction.facing_right = velocity.dx > 0
