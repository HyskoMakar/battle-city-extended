import pygame as pg
from scene import Scene
from widget import Widget
from button import Button

class GameOverScene(Scene):
    def __init__(self, level_reached, score, screen_width=648, screen_height=448):
        super().__init__("GameOver")
        self.level_reached = level_reached
        self.score = score
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.widgets = []
        self.setup()

    def setup(self):
        title = Widget(name="title", x=0, y=40, width=self.screen_width, height=80, bg_color=(30,30,30), text="Game Over", text_color=(255,255,255))
        title.image.fill((30,30,30))
        font = pg.font.SysFont(None, 48)
        txt = font.render("Game Over", True, (255,255,255))
        txt_rect = txt.get_rect(center=(self.screen_width//2, 40))
        title.image.blit(txt, txt_rect)
        info = Widget(name="info", x=(self.screen_width-300)//2, y=150, width=300, height=60, bg_color=(60,60,60), text=f"Level: {self.level_reached}  Score: {self.score}", text_color=(255,255,255))
        retry = Button(name="menu", x=(self.screen_width-200)//2, y=250, width=200, height=50, bg_color=(70,200,120), text="Main Menu", text_color=(0,0,0), on_click="MainMenu", hover_bg_color=(100,230,150))
        self.widgets = [title, info, retry]
