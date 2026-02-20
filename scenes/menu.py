import pygame as pg
from scenes.scene import Scene
from widgets.button import Button
from widgets.widget import Widget

class MainMenu(Scene):
    def __init__(self, screen_width=800, screen_height=480):
        super().__init__("MainMenu")
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.widgets = []
        self.setup()

    def setup(self):
        btn_w, btn_h = 250, 60
        x = (self.screen_width - btn_w) // 2
        y = (self.screen_height // 2) - btn_h - 15
        start = Button(name="start", x = x, y = y + 30, width=btn_w, height=btn_h, bg_color=(70,200,120), text="Start", text_color=(0,0,0), on_click="Level1", hover_bg_color=(100,230,150))
        quit_btn = Button(name="quit", x = x, y = y + btn_h + 100, width=btn_w, height=btn_h, bg_color=(200,70,70), text="Quit", text_color=(0,0,0), on_click="QUIT", hover_bg_color=(230,100,100))
        title = Widget(name="title", x=0, y=50, width=self.screen_width, height=100, bg_color=(40,40,40), text="Battle City Extended", text_color=(240,240,240))
        title.image.fill((40,40,40))
        font = pg.font.SysFont(None, 48)
        txt = font.render("Battle City Extended", True, (240,240,240))
        txt_rect = txt.get_rect(center=(self.screen_width//2, 50))
        title.image.blit(txt, txt_rect)
        self.widgets = [title, start, quit_btn]