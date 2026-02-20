import pygame as pg
from sprites.tanks.tank import Tank
from sprites.bullet import Bullet

class Player(Tank):
    def __init__(self, lives, **kwargs):
        super().__init__(**kwargs)
        self.lives = lives
        self.reload_timer = 0
        self.moving = False
        self.engine_channel = None

        try:
            self.engine_sound = pg.mixer.Sound("assets/sounds/engine.wav")
        except Exception:
            self.engine_sound = None
        try:
            self.shoot_sound = pg.mixer.Sound("assets/sounds/shoot.wav")
        except Exception:
            self.shoot_sound = None

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
        moving_now = any(keys[k] for k in (pg.K_w, pg.K_s, pg.K_a, pg.K_d))

        if moving_now and not self.moving:
            if self.engine_sound:
                try:
                    self.engine_channel = self.engine_sound.play(-1)
                except Exception:
                    self.engine_channel = None
            self.moving = True
        elif not moving_now and self.moving:
            if self.engine_channel:
                try:
                    self.engine_channel.stop()
                except Exception:
                    pass
            self.moving = False

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
            try:
                if self.shoot_sound:
                    self.shoot_sound.play()
            except Exception:
                pass
            return self.shoot()
        return None

    def shoot(self):
        bullet_x = self.rect.centerx - 8
        bullet_y = self.rect.centery - 8
        return Bullet(speed=375, dir=self.dir, owner=self, x=bullet_x, y=bullet_y,
                     image_path="assets/images/bullet.png", scale=2)