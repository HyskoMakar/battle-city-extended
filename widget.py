import pygame as pg

class Widget(pg.sprite.Sprite):
    def __init__(self, name, x, y, width, height, bg_color, text, text_color):
        super().__init__()
        self.name = name
        self.image = pg.Surface((width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.text = text
        self.text_color = text_color

        self.setup()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt=0):
        return ""

    def setup(self):
        self.image.fill(self.bg_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        font = pg.font.SysFont(None, 24)
        text_surface = font.render(self.text, True, self.text_color)

        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)