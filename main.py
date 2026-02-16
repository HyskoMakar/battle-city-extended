import pygame as pg
from scenes.level import Level
from scenes.menu import MainMenu
from scenes.gameover import GameOverScene
from scenes.win import WinScene

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 480))
        self.running = True
        self.menu = MainMenu()
        self.level1 = Level(name="Level1", seed="eJytlFEKwCAMQ-_itzcSEWQnmN6fDRlU00w36U9AGt9iWxaCy4fzJhL9A6vllpS2pN3tYZscEQXLp5ZSB2GWFQyOwKHmBYylZQUOk9d8aBKYeTKpsyaxKofhgMZ2we3JNMXUJZ_CwMeT_XrmZM9Ml5Z-sYUqul2rZLDtr3tGff0ALP4a8QJqYB-R", current_level=1)
        self.level2 = Level(name="Level2", seed="eJyLjlZKSlHSoQoRqwM1rKQYSMTHwwg0LhqBTTGyYTg1EktgGFZcAiMg8kU4CKyKiTEMIQYmiDcM3eVww5JKMQ3D4000PxBrGJL_iYkAsDkIgvgIwB_OOGMGj2FoviFajBiXES1G00SLO6kW40u-tHUZVUqNWADdtB7v", current_level=2)
        self.level3 = Level(name="Level3", seed="eJy9VEEOgCAM-wtnfkQIifEFAv9Xh6RkbGDUeGmgjK5lRufMshr7CXh7iaV4QAgnm-uKbdUDutuKERtThVK-VZC2vLgRoz6SGKwwDsV0t3P2BjoxBIHR0jYLHHsEHpPlQmCVQ-dBTLjAvCDG5vqDM-nNJJi92WRUQq5ZzBsSKic7a7IConIw-M4eOutjfvHX8DvyAR9H", current_level=3)
        self.level4 = Level(name="Level4", seed="eJyLjlZKSlHSoQoRqwM1rKQYJFAKI9C48fH4ZCFcJMPAosUlMAJhBDYCm2Jkw8CKIFJFKARCN4SFKgvWAZFANwxiRREKC91RRZjqsBuGUI6mEck3RZjqMAzDGUiIcCagBLvL4HrQghjBRVNHN5dRHma0jE1i0xkel-E0MakYnzlERQBJYiiGUaPUiAUAdLogWA==", current_level=4)
        self.level5 = Level(name="Level5", seed="eJytVEEOwCAI-4tnf7QYE7MXoP5_mc6IBc0OXBoErKXOXZdLt_MmEPxHVvKbqAPmMsYFoMqWjKxlc1lgkkGk9elkiUbUd9MCLQd9gmzfRDJSD0VlYBIMMpdgoa4M5mLyqhQ1pxbK2DkkKeD6oE8ns1J29gzgl2emt2n6nWm7O-RN4eAZeAHPcluVz8nirxEeOsMk2Q==", current_level=5)
        self.scenes = [self.menu, self.level1, self.level2, self.level3, self.level4, self.level5]
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
                    self.scene = go
                elif res.startswith("WIN:"):
                    parts = res.split(":")
                    level_num = int(parts[1])
                    score = int(parts[2])
                    ws = WinScene(level_num, score)
                    self.scene = ws
                elif res == "MainMenu":
                    self.scene = self.menu
                    for scene in self.scenes:
                        if hasattr(scene, 'regenerate'):
                            scene.regenerate(3, 0, 0)
                else:
                    scene = self.find_scene_by_name(res)
                    if scene is not None:
                        self.scene = scene

            self.screen.fill((50, 50, 50))
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