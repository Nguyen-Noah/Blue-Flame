import pygame, random
from .config import config

class Window:
    def __init__(self, game):
        self.game = game

        pygame.init()

        self.screen_resolution = config['window']['window_resolution']
        self.game_resolution = config['window']['game_resolution']
        self.fps = config['window']['framerate']
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(self.screen_resolution)
        self.display = pygame.Surface(self.game_resolution)
        self.screen_shake = 0
        self.num_font = pygame.font.Font('data/fonts/Minecraft.ttf', 36)

        pygame.display.set_caption('Blue Flame')

        self.dt = 1 / self.fps

    def add_screen_shake(self, amt):
        self.screen_shake = amt

    def render_frame(self):
        offset = [0, 0]
        if self.screen_shake:
            offset[0] += random.randint(0, 12) - 6
            offset[1] += random.randint(0, 12) - 6
            self.screen_shake -= 1

        if self.game.world.title.done:
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0 + offset[0], 0 + offset[1]))
            score_surf = self.num_font.render(str(int(self.game.world.score)), True, 'white')
            self.screen.blit(score_surf, ((self.screen_resolution[0] // 2) - (score_surf.get_width() // 2), 20))
        pygame.display.update()
        self.clock.tick(self.fps)
        self.display.fill((0, 0, 0))