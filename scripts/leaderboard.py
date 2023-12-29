import pygame, json
from .config import config

class Leaderboard:
    def __init__(self, game):
        self.game = game
        self.data = config['leaderboard']
        self.surf = pygame.Surface((200, self.game.window.screen_resolution[1] // 2))
        self.surf.set_colorkey((0, 0, 0))
        self.font = pygame.font.Font('data/fonts/Minecraft.ttf', 28)
        self.since_start = 0

    def add_score(self, score):
        self.data.append(score)
        self.data.sort(reverse=True)
        self.data = self.data[:5]

        with open('data/config/leaderboard.json', 'w') as file:
            json.dump(self.data, file)

    def render(self, surf):
        padding = 50
        self.surf.fill((0, 0, 0))
        for i, score in enumerate(self.data):
            i += 1
            score_surf = self.font.render(str(score), True, 'white')
            num_surf = self.font.render(str(i), True, 'white')
            self.surf.blit(score_surf, (self.surf.get_width() - score_surf.get_width(), i * padding))
            self.surf.blit(num_surf, (0, i * padding))
        pygame.draw.line(self.surf, 'white', (0, 32), (self.surf.get_width(), 32))
        pygame.draw.line(self.surf, 'white', (0, 286), (self.surf.get_width(), 286))
        self.since_start += self.game.window.dt
        self.surf.set_alpha(min(255, self.since_start * 400))
        surf.blit(self.surf, ((self.game.window.screen_resolution[0] // 2) - (self.surf.get_width() // 2), self.game.window.screen_resolution[1] // 10))