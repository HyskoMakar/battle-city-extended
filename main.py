import pygame as pg
from scenes.level import Level
from scenes.menu import MainMenu
from scenes.gameover import GameOverScene
from scenes.win import WinScene

class Game:
    def __init__(self):
        pg.init()
        try:
            pg.mixer.init()
        except Exception:
            pass
        self.screen = pg.display.set_mode((800, 480))
        pg.display.set_caption("Battle City Extended")
        self.running = True
        self.menu = MainMenu()
        self.level1 = Level(name="Level1", seed="eJytlFEKwCAMQ-_itzcSEWQnmN6fDRlU00w36U9AGt9iWxaCy4fzJhL9A6vllpS2pN3tYZscEQXLp5ZSB2GWFQyOwKHmBYylZQUOk9d8aBKYeTKpsyaxKofhgMZ2we3JNMXUJZ_CwMeT_XrmZM9Ml5Z-sYUqul2rZLDtr3tGff0ALP4a8QJqYB-R", current_level=1)
        self.level2 = Level(name="Level2", seed="eJyLjlZKSlHSoQoRqwM1rKQYSMTHwwg0LhqBTTGyYTg1EktgGFZcAiMg8kU4CKyKiTEMIQYmiDcM3eVww5JKMQ3D4000PxBrGJL_iYkAsDkIgvgIwB_OOGMGj2FoviFajBiXES1G00SLO6kW40u-tHUZVUqNWADdtB7v", current_level=2)
        self.level3 = Level(name="Level3", seed="eJy9VEEOgCAM-wtnfkQIifEFAv9Xh6RkbGDUeGmgjK5lRufMshr7CXh7iaV4QAgnm-uKbdUDutuKERtThVK-VZC2vLgRoz6SGKwwDsV0t3P2BjoxBIHR0jYLHHsEHpPlQmCVQ-dBTLjAvCDG5vqDM-nNJJi92WRUQq5ZzBsSKic7a7IConIw-M4eOutjfvHX8DvyAR9H", current_level=3)
        self.level4 = Level(name="Level4", seed="eJyLjlZKSlHSoQoRqwM1rKQYJFAKI9C48fH4ZCFcJMPAosUlMAJhBDYCm2Jkw8CKIFJFKARCN4SFKgvWAZFANwxiRREKC91RRZjqsBuGUI6mEck3RZjqMAzDGUiIcCagBLvL4HrQghjBRVNHN5dRHma0jE1i0xkel-E0MakYnzlERQBJYiiGUaPUiAUAdLogWA==", current_level=4)
        self.level5 = Level(name="Level5", seed="eJytVEEOwCAI-4tnf7QYE7MXoP5_mc6IBc0OXBoErKXOXZdLt_MmEPxHVvKbqAPmMsYFoMqWjKxlc1lgkkGk9elkiUbUd9MCLQd9gmzfRDJSD0VlYBIMMpdgoa4M5mLyqhQ1pxbK2DkkKeD6oE8ns1J29gzgl2emt2n6nWm7O-RN4eAZeAHPcluVz8nirxEeOsMk2Q==", current_level=5)
        self.scenes_map = {
            "MainMenu": self.menu,
            "Level1": self.level1,
            "Level2": self.level2,
            "Level3": self.level3,
            "Level4": self.level4,
            "Level5": self.level5,
        }
        self.scene = self.menu
        self.clock = pg.time.Clock()
        self.dt = 0

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            self.dt = self.clock.tick(60) / 1000.0

            try:
                res = self.scene.update(self.dt) or ""
            except Exception:
                res = ""
            
            if res:
                if res == "QUIT":
                    self.running = False
                elif res == "MainMenu":
                    self._stop_all_sounds()
                    self._clear_button_states()
                    self.scene = self.menu
                elif res.startswith("GAME_OVER:"):
                    parts = res.split(":")
                    level_num = int(parts[1])
                    score = int(parts[2])
                    self._stop_all_sounds()
                    self._clear_button_states()
                    self.scene = GameOverScene(level_num, score)
                elif res.startswith("WIN:"):
                    parts = res.split(":")
                    level_num = int(parts[1])
                    score = int(parts[2])
                    self._stop_all_sounds()
                    self._clear_button_states()
                    self.scene = WinScene(level_num, score)
                elif res in self.scenes_map:
                    next_scene = self.scenes_map[res]
                    self._clear_button_states()
                    self.scene = next_scene
                    if res.startswith("Level"):
                        try:
                            next_scene.regenerate(3, 0, 0)
                        except Exception:
                            pass

            self.screen.fill((50, 50, 50))
            try:
                self.scene.draw(self.screen)
            except Exception:
                pass
            pg.display.flip()

    def _stop_all_sounds(self):
        try:
            pg.mixer.stop()
        except Exception:
            pass

    def _clear_button_states(self):
        for scene in self.scenes_map.values():
            if hasattr(scene, 'widgets'):
                for widget in scene.widgets:
                    if hasattr(widget, '_mouse_was_down'):
                        widget._mouse_was_down = False
                    if hasattr(widget, 'hovered'):
                        widget.hovered = False


if __name__ == "__main__":
    game = Game()
    game.run()
    pg.quit()