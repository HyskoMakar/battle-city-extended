import pygame as pg
import random
from scene import Scene
from block import Block
from tank import Tank
from player_tank import Player
from widget import Widget
from bullet import Bullet
from enemy_tank import EnemyTank
from tank_spawner import TankSpawner
from base import Base
from generator import seed_to_level


class Level(Scene):
    CELL_SIZE = 48
    PLAYER_SPEED = 120
    ENEMY_SPEED = 90
    PLAYER_RELOAD = 0.5
    ENEMY_RELOAD = 1.5
    SPAWNER_FIRST_DELAY = 3
    SPAWNER_RELOAD = 8
    KILL_POINTS = 100
    
    def __init__(self, name, seed, current_level):
        super().__init__(name)
        self.current_level = current_level
        self.seed = seed
        self.sprites = []
        self.spawners = []
        self.player = None
        self.player_start = None
        self.base = None
        self.kills = 0
        self.points = 0
        self._init_widgets()
        self.regenerate(3, 0, 0)
    
    def _init_widgets(self):
        self.widgets = [
            Widget(name="kills", x=672, y=50, width=280, height=50, 
                  bg_color=(50, 50, 50), text="", text_color=(255, 255, 255)),
            Widget(name="points", x=672, y=110, width=280, height=50, 
                  bg_color=(50, 50, 50), text="", text_color=(255, 255, 255))
        ]
    
    def regenerate(self, lives, points, kills):
        self.kills = kills
        self.points = points
        self.sprites = []
        self.spawners = []
        
        level_data = seed_to_level(self.seed)
        self._build_level(level_data, lives)
        self._spawn_player_if_needed(lives)
    
    def _build_level(self, level_data, lives):
        for y, row in enumerate(level_data):
            for x, cell in enumerate(row):
                self._create_cell_object(x, y, cell, lives)
    
    def _create_cell_object(self, x, y, cell, lives):
        pos_x, pos_y = x * self.CELL_SIZE, y * self.CELL_SIZE
        
        if cell == "bd":
            self._add_block(pos_x, pos_y, False, "images/bedrock.png", 3)
        elif cell == "st":
            self._add_steel_blocks(pos_x, pos_y)
        elif cell == "br":
            self._add_brick_blocks(pos_x, pos_y)
        elif cell == "ts":
            self._add_spawner(pos_x, pos_y)
        elif cell == "bs":
            self._add_base(pos_x, pos_y)
    
    def _add_block(self, x, y, breakable, image_path, scale):
        self.sprites.append(Block(breakable=breakable, x=x, y=y, 
                                 image_path=image_path, scale=scale))
    
    def _add_steel_blocks(self, x, y):
        for dx, dy in [(0, 0), (24, 0), (0, 24), (24, 24)]:
            self._add_block(x + dx, y + dy, False, "images/steel.png", 3)
    
    def _add_brick_blocks(self, x, y):
        for dx, dy in [(0, 0), (24, 0), (0, 24), (24, 24)]:
            self._add_block(x + dx, y + dy, True, "images/bricks.png", 3)
    
    def _add_spawner(self, x, y):
        spawner = TankSpawner(
            first_tank_spawn_time=self.SPAWNER_FIRST_DELAY,
            reload_time=self.SPAWNER_RELOAD,
            tank_options=(self.ENEMY_SPEED, 1, self.ENEMY_RELOAD),
            x=x, y=y, image_path="images/tank_spawner.png", scale=1.5
        )
        self.spawners.append(spawner)
        self.sprites.append(spawner)
    
    def _add_base(self, x, y):
        self.base = Base(x=x, y=y, image_path="images/base.png", scale=1.5)
        self.sprites.append(self.base)
    
    def _spawn_player_if_needed(self, lives):
        if self.player is None and self.base:
            self.player = Player(
                speed=self.PLAYER_SPEED, dir="top", hp=1, 
                reload_time=self.PLAYER_RELOAD, lives=lives,
                x=self.base.rect.x, y=self.base.rect.y,
                image_path="images/player_tank.png", scale=3
            )
            self.player_start = (self.base.rect.x, self.base.rect.y)
            self.sprites.append(self.player)
    
    def update(self, dt):
        super().update(dt)
        self._update_sprites(dt)
        self._cleanup_dead_enemies()
        self._respawn_player_if_dead()
        self._update_widgets()
        return self._check_game_over()
    
    def _update_sprites(self, dt):
        for sprite in list(self.sprites):
            if isinstance(sprite, Tank):
                self._update_tank(sprite, dt)
            elif isinstance(sprite, Bullet):
                self._update_bullet(sprite, dt)
            elif isinstance(sprite, TankSpawner):
                self._update_spawner(sprite, dt)
    
    def _update_tank(self, tank, dt):
        result = tank.update(self.sprites, dt)
        if result:
            self.sprites.append(result)
    
    def _update_bullet(self, bullet, dt):
        hit = bullet.update(self.sprites, dt)
        if hit:
            self._handle_bullet_hit(bullet, hit)
    
    def _handle_bullet_hit(self, bullet, hit):
        if isinstance(hit, list):
            for block in hit:
                if block in self.sprites:
                    self.sprites.remove(block)
        elif isinstance(hit, Block) and hit in self.sprites:
            self.sprites.remove(hit)
        
        if bullet in self.sprites:
            self.sprites.remove(bullet)
    
    def _update_spawner(self, spawner, dt):
        result = spawner.update(self.sprites, dt)
        if result and self._can_spawn_enemy(spawner):
            self.sprites.append(result)
    
    def _can_spawn_enemy(self, spawner):
        enemy_count = sum(1 for s in self.sprites if isinstance(s, EnemyTank))
        return enemy_count == 0 and spawner == random.choice(self.spawners)
    
    def _cleanup_dead_enemies(self):
        for sprite in list(self.sprites):
            if isinstance(sprite, EnemyTank) and sprite.hp <= 0:
                self.sprites.remove(sprite)
                self.kills += 1
                self.points += self.KILL_POINTS
    
    def _respawn_player_if_dead(self):
        if self.player and self.player.hp <= 0:
            if self.player in self.sprites:
                self.sprites.remove(self.player)
            
            self.player = Player(
                speed=self.PLAYER_SPEED, dir="top", hp=1,
                reload_time=self.PLAYER_RELOAD, lives=3,
                x=self.player_start[0], y=self.player_start[1],
                image_path="images/player_tank.png", scale=3
            )
            self.sprites.append(self.player)
    
    def _update_widgets(self):
        for widget in self.widgets:
            if widget.name == "kills":
                widget.text = f"Kills: {self.kills}"
            elif widget.name == "points":
                widget.text = f"Points: {self.points}"
            widget.setup()
    
    def _check_game_over(self):
        if self.base and self.base.destroyed:
            return f"GAME_OVER:{self.current_level}:{self.points}"
        return ""
    
    def draw(self, screen):
        for sprite in self.sprites:
            sprite.draw(screen)
        super().draw(screen)