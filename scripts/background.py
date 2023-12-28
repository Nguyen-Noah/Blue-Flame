import pygame, math, random
from .core_funcs import itr

class Square:
    def __init__(self, base_location, location, size, speed):
        self.rotation = random.random() * math.pi * 2
        self.rot_speed = (random.random() - 0.5) * 4
        self.width = random.randint(1, 2)

        self.location = list(location)
        self.base_location = list(base_location)
        self.size = size
        self.speed = speed

        self.parallax_rate = random.random() * 0.45

        self.location[0] *= self.parallax_rate
        self.location[1] *= self.parallax_rate
        
    def update(self, dt):
        self.location[1] += self.speed * dt
        self.size -= dt
        self.rotation += self.rot_speed * dt
        if self.size < 0:
            return False
        else:
            return True

    def render(self, surf, scroll=0):
        points = []
        for i in range(4):
            angle = i / 4 * math.pi * 2 + self.rotation
            points.append([self.location[0] + math.cos(angle) * self.size * self.parallax_rate + self.base_location[0], 
                           self.location[1] + math.sin(angle) * self.size - scroll * self.parallax_rate + self.base_location[1]])

        pygame.draw.polygon(surf, (218, 82, 16), points, width=self.width)

class Background:
    def __init__(self, game):
        self.game = game
        self.squares = []
        
    def update(self):
        if random.randint(1, 20) == 1:
            self.squares.append(Square([random.random() * (self.game.window.game_resolution[0] - self.game.world.border_width * 2) + self.game.world.border_width, -20], 
                                        (0, self.game.world.scroll - 20), 
                                        random.randint(10, 25), random.randint(15, 60)))

        for i, square in itr(self.squares):
            alive = square.update(self.game.window.dt)
            if not alive:
                self.squares.pop(i)

    def render(self, surf, scroll=0):
        surf.blit(self.game.assets.background['gradient_n'], (0, 0))

        for square in self.squares:
            square.render(surf, scroll)