import pygame as pg
from scenes.scene import Scene
from widgets.widget import Widget
from widgets.button import Button

class WinScene(Scene):
    TOTAL_LEVELS = 5
    
    def __init__(self, level_reached, score, screen_width=800, screen_height=480):
        super().__init__("Win")
        self.level_reached = level_reached
        self.score = score
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.widgets = []
        self.setup()

    def setup(self):
        title = Widget(name="title", x=0, y=50, width=self.screen_width, height=100, bg_color=(20,120,20), text="You Win!", text_color=(255,255,255))
        title.image.fill((20,120,20))
        font = pg.font.SysFont(None, 60)
        txt = font.render("You Win!", True, (255,255,255))
        txt_rect = txt.get_rect(center=(self.screen_width//2, 50))
        title.image.blit(txt, txt_rect)
        info = Widget(name="info", x=(self.screen_width-400)//2, y=180, width=400, height=70, bg_color=(60,60,60), text=f"Level: {self.level_reached}  Score: {self.score}", text_color=(255,255,255))
        
        if self.level_reached < self.TOTAL_LEVELS:
            next_level = Button(name="next", x=(self.screen_width-250)//2, y=300, width=250, height=60, bg_color=(70,200,120), text="Next Level", text_color=(0,0,0), on_click=f"Level{self.level_reached + 1}", hover_bg_color=(100,230,150))
            self.widgets = [title, info, next_level]
        else:
            menu = Button(name="menu", x=(self.screen_width-250)//2, y=300, width=250, height=60, bg_color=(70,200,120), text="Main Menu", text_color=(0,0,0), on_click="MainMenu", hover_bg_color=(100,230,150))
            self.widgets = [title, info, menu]