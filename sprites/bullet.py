import pygame as pg
from sprites.sprite import Sprite
from sprites.tanks.tank import Tank
from sprites.blocks.base import Base
from sprites.blocks.block import Block

class Bullet(Sprite):
    MAX_BLOCKS_DESTROYED = 2
    
    def __init__(self, speed, dir, owner, **kwargs):
        super().__init__(**kwargs)
        self._image = self.image
        self.speed = speed
        self.dir = dir
        self.owner = owner
        self.blocks_destroyed = 0

    def update(self, sprites, dt):
        self._move(dt)
        return self._check_collisions(sprites)

    def _move(self, dt):
        movement = {"left": (-self.speed * dt, 0), "right": (self.speed * dt, 0),
                    "top": (0, -self.speed * dt), "bottom": (0, self.speed * dt)}
        dx, dy = movement.get(self.dir, (0, 0))
        self.rect.x += dx
        self.rect.y += dy

    def _check_collisions(self, sprites):
        blocks_to_remove = []
        for sprite in sprites:
            if sprite is self or sprite is self.owner:
                continue
            
            if not self.rect.colliderect(sprite.rect):
                continue
                
            if isinstance(sprite, Tank):
                sprite.hp = 0
                return True
            elif isinstance(sprite, Base):
                if self.owner.__class__.__name__ != "Player":
                    sprite.destroyed = True
                    return True
            elif isinstance(sprite, Block):
                result = self._handle_block_collision(sprite, blocks_to_remove)
                if result:
                    return result
        
        return blocks_to_remove if blocks_to_remove else False

    def _handle_block_collision(self, block, blocks_to_remove):
        if block.breakable:
            blocks_to_remove.append(block)
            self.blocks_destroyed += 1
            if self.blocks_destroyed >= self.MAX_BLOCKS_DESTROYED:
                return blocks_to_remove
        else:
            return True
        return None

    def draw(self, screen):
        rotation = {"left": 90, "right": -90, "top": 0, "bottom": 180}
        self.image = pg.transform.rotate(self._image, rotation.get(self.dir, 0))
        return super().draw(screen)