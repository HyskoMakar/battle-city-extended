import pygame as pg
from sprite import Sprite
from enemy_tank import EnemyTank
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
            return EnemyTank(speed=speed, hp=hp, reload_speed=reload_time, dir="bottom", x=self.rect.x, y=self.rect.y, image_path="images/enemy_tank.png", scale=3)
        return None
