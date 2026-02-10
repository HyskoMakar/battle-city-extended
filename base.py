import pygame as pg
from sprite import Sprite

class Base(Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.destroyed = False
        self.is_solid = True
