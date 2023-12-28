import pygame, math, random

class Healthbar:
    def __init__(self, game, owner, pos):
        self.game = game
        self.owner = owner
        self.pos = pos
        self.height = self.game.window.game_resolution[1] - ((self.game.window.game_resolution[1] / 5) * 2)
        self.surf = pygame.Surface((9, self.height))
        self.colors = [
            (0, 152, 219),
            (30, 87, 156)
        ]

    def update(self, dt):
        if random.randint(1, 2) == 1:
            self.game.world.particles.add_particle('healthbar', (random.randint(0, self.surf.get_width()), self.surf.get_height()), 'circle', [0, random.randint(0, 6) * -10], 1, random.randint(0, 2), custom_color=self.colors[random.randint(0, 1)])

    def render(self, surf):
        self.surf.fill((32, 52, 98))
        self.game.world.particles.render('healthbar', self.surf)

        ratio = self.owner.health / 100
        pygame.draw.rect(self.surf, (10, 10, 10), (0, 0, 9, self.height - (self.height * ratio)))
        pygame.draw.rect(self.surf, (255, 255, 255), (0, self.height - (self.height * ratio), 9, self.height * ratio + 1), 1)
        surf.blit(self.surf, self.pos)