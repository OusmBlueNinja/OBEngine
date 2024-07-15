class Entity:
    def __init__(self, x, y):
        print("Entity Init")
        self.x = x
        self.y = y
        self.image = None  # This should be set to a Pygame surface

    def update(self):
        pass

    def draw(self):
        pass
