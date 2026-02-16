import pygame as pg
from widgets.widget import Widget

class Button(Widget):
    def __init__(self, name, x, y, width, height, bg_color, text, text_color, on_click, hover_bg_color=None, hover_text_color=None):
        super().__init__(name, x, y, width, height, bg_color, text, text_color)
        self.on_click = on_click
        self.hover_bg_color = hover_bg_color if hover_bg_color is not None else bg_color
        self.hover_text_color = hover_text_color if hover_text_color is not None else text_color
        self.hovered = False
        self._mouse_was_down = False

    def redraw(self):
        bg = self.hover_bg_color if self.hovered else self.bg_color
        text_col = self.hover_text_color if self.hovered else self.text_color
        self.image.fill(bg)
        font = pg.font.SysFont(None, 24)
        text_surface = font.render(self.text, True, text_col)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)

    def update(self, dt=0):
        mouse_pos = pg.mouse.get_pos()
        mouse_down = pg.mouse.get_pressed()[0]

        hovered = self.rect.collidepoint(mouse_pos)
        if hovered != self.hovered:
            self.hovered = hovered
            self.redraw()

        if self.hovered and not mouse_down and self._mouse_was_down:
            self._mouse_was_down = False
            return self.on_click
        
        if mouse_down:
            self._mouse_was_down = True

        return ""
