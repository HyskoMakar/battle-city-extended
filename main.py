import pygame as pg
from level import Level
from menu import MainMenu
from gameover import GameOverScene
from win import WinScene

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((972, 672))
        self.running = True
        self.menu = MainMenu(screen_width=648, screen_height=448)
        self.level1 = Level(name="Level1", seed="eJyLjlZKSlHSoZSI1YGaU1IMJOLjYQQaF6cEmItsDjY9xBIY5iQVwQg0Lk6JIWkO7gAhzZziEhQxMJcoc7BZC9aNMJFQfKG5Ar856C7D6h5szsfmYTzph1rpEKsrinFI4AgfCvNpLABMq_oW", current_level=1)
        self.scenes = [self.menu, self.level1]
        self.scene = self.menu
        self.clock = pg.time.Clock()
        self.dt = 0

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            self.dt = self.clock.tick(60) / 1000.0

            res = self.scene.update(self.dt) or ""
            if res:
                if res == "QUIT":
                    self.running = False
                elif res.startswith("GAME_OVER:"):
                    parts = res.split(":")
                    level_num = int(parts[1])
                    score = int(parts[2])
                    go = GameOverScene(level_num, score)
                    self.scenes.append(go)
                    self.scene = go
                elif res.startswith("WIN:"):
                    parts = res.split(":")
                    level_num = int(parts[1])
                    score = int(parts[2])
                    ws = WinScene(level_num, score)
                    self.scenes.append(ws)
                    self.scene = ws
                else:
                    scene = self.find_scene_by_name(res)
                    if scene is not None:
                        self.scene = scene

            self.screen.fill((80, 80, 80))
            self.scene.draw(self.screen)
            pg.display.flip()

    def find_scene_by_name(self, name):
        for scene in self.scenes:
            if scene.name == name:
                return scene
        return None


if __name__ == "__main__":
    game = Game()
    game.run()
    pg.quit()