import pygame as pg
from sprites.sprite import Sprite
from sprites.blocks.block import Block
from sprites.blocks.base import Base
from sprites.blocks.bush import Bush

class Tank(Sprite):
    def __init__(self, speed, dir, hp, reload_speed=None, reload_time=None, **kwargs):
        super().__init__(**kwargs)
        self._image = self.image
        self.speed = speed
        self.dir = dir
        self.hp = 1
        self.max_hp = 1
        self.reload_speed = reload_time if reload_speed is None else reload_speed

    def update(self, sprites, dt):
        self._handle_collisions(sprites)

    def _handle_collisions(self, sprites):
        for sprite in sprites:
            if sprite is self:
                continue
            
            if isinstance(sprite, Block) and self.rect.colliderect(sprite.rect):
                self._resolve_collision(sprite)
            elif isinstance(sprite, Bush) and self.rect.colliderect(sprite.rect):
                if self.__class__.__name__ != "Player":
                    self._resolve_collision(sprite)
            elif self._should_collide_with_solid(sprite):
                self._resolve_collision(sprite)

    def _should_collide_with_solid(self, sprite):
        if not hasattr(sprite, 'is_solid') or not sprite.is_solid:
            return False
        if not self.rect.colliderect(sprite.rect):
            return False
        if self.__class__.__name__ == "Player" and sprite.__class__.__name__ == "Base":
            return False
        return self.__class__.__name__ == "Player"

    def _resolve_collision(self, sprite):
        if self.dir == "left":
            self.rect.left = sprite.rect.right
        elif self.dir == "right":
            self.rect.right = sprite.rect.left
        elif self.dir == "top":
            self.rect.top = sprite.rect.bottom
        elif self.dir == "bottom":
            self.rect.bottom = sprite.rect.top

    def draw(self, screen):
        rotation = {"left": 90, "right": -90, "top": 0, "bottom": 180}
        self.image = pg.transform.rotate(self._image, rotation.get(self.dir, 0))
        return super().draw(screen)