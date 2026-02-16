import pygame as pg
import random
from sprites.tanks.tank import Tank
from sprites.bullet import Bullet

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
        return self._try_shoot(dt)

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
        self.dir = "right" if abs(dx) > abs(dy) and dx > 0 else \
                   "left" if abs(dx) > abs(dy) else \
                   "bottom" if dy > 0 else "top"

    def _move(self, dt):
        movement = {"left": (-self.speed * dt, 0), "right": (self.speed * dt, 0),
                    "top": (0, -self.speed * dt), "bottom": (0, self.speed * dt)}
        dx, dy = movement.get(self.dir, (0, 0))
        self.rect.x += dx
        self.rect.y += dy

    def _try_shoot(self, dt):
        self.reload_timer -= dt
        if self.reload_timer <= 0:
            self.reload_timer = self.reload_speed
            return self.shoot()
        return None

    def shoot(self):
        bullet_x = self.rect.centerx - 8
        bullet_y = self.rect.centery - 8
        return Bullet(speed=375, dir=self.dir, owner=self, x=bullet_x, y=bullet_y, 
                     image_path="assets/images/bullet.png", scale=2)
