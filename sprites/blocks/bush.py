import pygame as pg
from sprites.sprite import Sprite


class Bush(Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image.set_alpha(128)
