class Renderer:
    def __init__(self, game):
        self.game = game

    def render(self):
        surf = self.game.window.display
        self.game.world.render(surf)