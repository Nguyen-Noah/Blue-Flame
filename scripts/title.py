import pygame

class Title:
    def __init__(self, game):
        self.game = game
        self.done = False
        self.load()

    def load(self):
        self.age = 0
        self.pre_age = 0
        self.ending = False

        # title screen
        res = self.game.window.screen.get_size()
        self.surf = pygame.Surface(res)
        self.surf.fill((0, 0, 0))
        self.surf.blit(self.game.assets.background['vignette'], (0, 0))
        big_font = pygame.font.Font('data/fonts/Horison.ttf', 50)
        title = big_font.render('Blue Flame', True, 'white')
        title_shadow = big_font.render('Blue Flame', True, 'black')
        self.surf.blit(title_shadow, (((res[0] // 2) - title.get_width() // 2) + 4, ((res[1] // 2) - title.get_height() // 2) + 4))
        self.surf.blit(title, ((res[0] // 2) - title.get_width() // 2, (res[1] // 2) - title.get_height() // 2))
        small_font = pygame.font.Font('data/fonts/Horison.ttf', 18)
        self.click_text = small_font.render('Click to Play', True, 'white')

    def update(self, dt):
        self.pre_age += dt
        if self.pre_age > 0.5:
            if not self.ending:
                self.age += dt
            else:
                self.age -= dt

            if self.age > 3 and not self.ending and self.game.input.mouse_state['left_click']:
                self.ending = True
                self.age = 0.3

        if self.ending and self.age < 0:
            self.done = True

    def render(self, surf):
        self.surf.set_alpha(min(255, self.age * 100))
        surf.blit(self.surf, (0, 0))
        if self.age > 2.8:
            if self.age % 1 < 0.86:
                self.surf.blit(self.click_text, ((self.game.window.screen.get_width() // 2) - self.click_text.get_width() // 2, self.game.window.screen.get_height() - 20))