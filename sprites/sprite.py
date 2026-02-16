import pygame as pg

class Sprite(pg.sprite.Sprite):
    def __init__(self, x, y, image_path, scale=1):
        super().__init__()
        self.image = pg.image.load(image_path)
        
        if scale != 1:
            width = int(self.image.get_width() * scale)
            height = int(self.image.get_height() * scale)
            self.image = pg.transform.scale(self.image, (width, height))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        return ""