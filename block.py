from sprite import Sprite

class Block(Sprite):
    def __init__(self, breakable: bool, **kwargs):
        super().__init__(**kwargs)
        self.breakable = breakable