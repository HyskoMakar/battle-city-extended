class Scene:
    def __init__(self, name):
        self.name = name
        self.widgets = []

    def find_widget_by_name(self, name):
        for widget in self.widgets:
            if widget.name == name:
                return widget
        return None

    def draw(self, screen):
        for widget in self.widgets:
            widget.draw(screen)

    def update(self, dt=0):
        for widget in self.widgets:
            try:
                res = widget.update(dt)
            except TypeError:
                res = widget.update()
            if res != "":
                return res
        return ""