import pygame as pg
import random
from sprites.tanks.tank import Tank
from sprites.bullet import Bullet

_ENEMY_SHOOT_SOUND = None

def _get_enemy_shoot_sound():
    s = globals().get('_ENEMY_SHOOT_SOUND')
    if s is None:
        try:
            s = pg.mixer.Sound("assets/sounds/shoot.wav")
        except Exception:
            s = None
        globals()['_ENEMY_SHOOT_SOUND'] = s
    return s

class EnemyTank(Tank):
    MIN_MOVE_TIME = 1.0
    MAX_MOVE_TIME = 3.0
    DIRECTIONS = ["top", "bottom", "left", "right"]
    BASE_TARGET_PROBABILITY = 0.7
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reload_timer = 0
        self.move_timer = random.uniform(self.MIN_MOVE_TIME, self.MAX_MOVE_TIME)
        self.current_move_time = 0
        self.target_base = None

    def update(self, sprites, dt):
        self._find_base(sprites)
        self._update_movement(dt)
        self._move(dt)
        super().update(sprites, dt)
        return self._try_shoot(sprites, dt)

    def _find_base(self, sprites):
        if self.target_base is None:
            for sprite in sprites:
                if sprite.__class__.__name__ == "Base":
                    self.target_base = sprite
                    break

    def _update_movement(self, dt):
        self.current_move_time += dt
        if self.current_move_time >= self.move_timer:
            self.current_move_time = 0
            self.move_timer = random.uniform(self.MIN_MOVE_TIME, self.MAX_MOVE_TIME)
            self._choose_direction()

    def _choose_direction(self):
        if self.target_base and random.random() < self.BASE_TARGET_PROBABILITY:
            self._move_towards_base()
        else:
            self.dir = random.choice(self.DIRECTIONS)

    def _move_towards_base(self):
        dx = self.target_base.rect.centerx - self.rect.centerx
        dy = self.target_base.rect.centery - self.rect.centery
        if abs(dx) > abs(dy):
            self.dir = "right" if dx > 0 else "left"
        else:
            self.dir = "bottom" if dy > 0 else "top"

    def _move(self, dt):
        movement = {"left": (-self.speed * dt, 0), "right": (self.speed * dt, 0),
                    "top": (0, -self.speed * dt), "bottom": (0, self.speed * dt)}
        dx, dy = movement.get(self.dir, (0, 0))
        self.rect.x += dx
        self.rect.y += dy

    def _try_shoot(self, sprites, dt):
        self.reload_timer -= dt
        if self.reload_timer <= 0:
            first_block = None
            for sprite in sprites:
                if sprite is self:
                    continue
                if hasattr(sprite, 'rect') and self.rect.colliderect(sprite.rect):
                    continue

            scan_rect = self.rect.copy()
            max_scan = 160
            step = 8
            for _ in range(0, max_scan, step):
                if self.dir == 'left':
                    scan_rect.x -= step
                elif self.dir == 'right':
                    scan_rect.x += step
                elif self.dir == 'top':
                    scan_rect.y -= step
                elif self.dir == 'bottom':
                    scan_rect.y += step

                for s in sprites:
                    if s is self:
                        continue
                    if not hasattr(s, 'rect'):
                        continue
                    if not scan_rect.colliderect(s.rect):
                        continue
                    from sprites.blocks.block import Block
                    if isinstance(s, Block):
                        first_block = s
                        break
                    from sprites.tanks.tank import Tank as _Tank
                    from sprites.blocks.base import Base as _Base
                    if isinstance(s, _Tank) or isinstance(s, _Base):
                        first_block = None
                        break
                if first_block is not None:
                    break

            if first_block is not None and not getattr(first_block, 'breakable', False):
                self.reload_timer = max(0.2, self.reload_speed / 2)
                return None

            self.reload_timer = self.reload_speed
            return self.shoot()
        return None

    def shoot(self):
        bullet_x = self.rect.centerx - 8
        bullet_y = self.rect.centery - 8
        try:
            s = _get_enemy_shoot_sound()
            if s:
                s.play()
        except Exception:
            pass

        return Bullet(speed=375, dir=self.dir, owner=self, x=bullet_x, y=bullet_y, 
                     image_path="assets/images/bullet.png", scale=2)
