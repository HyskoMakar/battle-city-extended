import pygame as pg
from sprites.sprite import Sprite
from sprites.tanks.enemy_tank import EnemyTank
import random

class TankSpawner(Sprite):
    def __init__(self, first_tank_spawn_time, reload_time, tank_options, **kwargs):
        super().__init__(**kwargs)
        self.first_tank_spawn_time = first_tank_spawn_time
        self.reload_time = reload_time
        self.tank_options = tank_options
        self.timer = first_tank_spawn_time
        self.first_spawn = True
        self.is_solid = True

    def update(self, sprites, dt):
        self.timer -= dt
        if self.timer <= 0:
            if self.first_spawn:
                self.timer = self.reload_time
                self.first_spawn = False
            else:
                self.timer = self.reload_time
            
            speed, hp, reload_time = self.tank_options
            tank_size = 32
            spawner_size = 32
            center_x = self.rect.x + (spawner_size - tank_size) // 2
            center_y = self.rect.y + (spawner_size - tank_size) // 2
            return EnemyTank(speed=speed, hp=hp, reload_speed=reload_time, dir="bottom", x=center_x, y=center_y, image_path="assets/images/enemy_tank.png", scale=2)
        return None
