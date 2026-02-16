import pygame as pg
from sprites.tanks.tank import Tank
from sprites.bullet import Bullet

class Player(Tank):
    def __init__(self, lives, **kwargs):
        super().__init__(**kwargs)
        self.lives = lives
        self.reload_timer = 0

    def update(self, sprites, dt):
        self._handle_input(dt)
        super().update(sprites, dt)
        return self._try_shoot(dt)

    def _handle_input(self, dt):
        keys = pg.key.get_pressed()
        movement = {
            pg.K_w: (0, -self.speed * dt, "top"),
            pg.K_s: (0, self.speed * dt, "bottom"),
            pg.K_a: (-self.speed * dt, 0, "left"),
            pg.K_d: (self.speed * dt, 0, "right")
        }
        
        for key, (dx, dy, direction) in movement.items():
            if keys[key]:
                self.rect.x += dx
                self.rect.y += dy
                self.dir = direction
                break

    def _try_shoot(self, dt):
        self.reload_timer -= dt
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.reload_timer <= 0:
            self.reload_timer = self.reload_speed
            return self.shoot()
        return None

    def shoot(self):
        bullet_x = self.rect.centerx - 8
        bullet_y = self.rect.centery - 8
        return Bullet(speed=375, dir=self.dir, owner=self, x=bullet_x, y=bullet_y,
                     image_path="assets/images/bullet.png", scale=2)