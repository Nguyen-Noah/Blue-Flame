import math, random
from .hook import Hook

class Player:
    def __init__(self, game, pos):
        self.game = game
        self.pos = list(pos)
        self.velocity = [0, 0]
        self.gravity = 0
        self.img = self.game.assets.game_assets['player']
        self.radius = (self.img.get_width() // 2)
        self.colors = [(0, 152, 219), (12, 230, 242), (0, 0, 0)]
        self.hook = Hook(self.game, self)
        self.health = 100
        self.alive = True

        self.game.audio.add('bump.wav', 0.5)
        self.game.audio.add('death.wav', 0.5)

    def die(self):
        self.alive = False
        self.game.audio.play('death')
        self.game.world.vfx.spawn_vfx('circle', self, (self.pos[0] + self.radius, self.pos[1] + self.radius), 20, 15, 40, 100)
        self.game.world.vfx.spawn_vfx('circle', self, (self.pos[0] + self.radius, self.pos[1] + self.radius), 20, 20, 90, 300)

    def add_health(self, amt):
        self.health = min(100, self.health + amt)

    def update(self, dt):
        if self.alive and self.game.world.title.done:
            if self.health <= 0 and self.hook.state == Hook.IDLE:
                self.die()
            else:
                if self.game.world.has_started:
                    self.health -= dt * self.game.world.difficulty_level

            # update the hook
            self.hook.update(dt)

            # if click AND the hook is not deploying, use the hook
            if self.game.input.mouse_state['left_click']:
                # start the game loop
                if not self.game.world.has_started:
                    self.game.world.start_game_loop()
                
                # deploying the hook
                if not self.hook.state == Hook.DEPLOYING:
                    self.hook.use()
            
            acceleration = [0, 0]
            if self.hook.state == Hook.STUCK:
                # if the hook is stuck, pause for a second
                self.velocity[0] = 0
                self.velocity[1] = 0
            elif self.hook.state == Hook.STUCK_REELING:
                acceleration = [self.hook.pos[0] - self.pos[0], self.hook.pos[1] - self.pos[1]]
            else:
                acceleration = [0, self.gravity]

            self.velocity[0] += acceleration[0] * dt
            self.velocity[1] += acceleration[1] * dt

            if self.hook.state == Hook.DEPLOYING:
                self.pos[0] += self.velocity[0] * dt
                self.pos[1] += self.velocity[1] * dt
            else:
                self.pos[0] += self.velocity[0]
                self.pos[1] += self.velocity[1]

    def render(self, surf, scroll=0):
        if self.alive:
            if self.game.world.has_started:
                for i in range(math.ceil(self.health / 30)):
                    self.game.world.particles.add_particle('player', self.pos, 'circle', [(random.randint(0, 10) / 10 - 0.5) * 10, (random.randint(0, 20) / 10 - 2) * 10], 20, 0 + random.randint(0, 20) / 10, custom_color=self.colors[random.randint(0, 1)], glow=(6, 6, 18), glow_radius=2)
                self.game.world.particles.add_particle('player', self.pos, 'circle', [(random.randint(0, 10) / 10 - 0.5) * 10, (random.randint(0, 20) / 10 - 2) * 10], 10, 0 + random.randint(0, 20) / 10, custom_color=self.colors[2])
            else:
                self.game.world.particles.add_particle('player', self.pos, 'circle', [(random.randint(0, 10) / 10 - 0.5) * 10, (random.randint(0, 20) / 10 - 2) * 10], 4, 0 + random.randint(0, 20) / 10, custom_color=self.colors[random.randint(0, 2)], glow=(6, 6, 18), glow_radius=3)
                self.game.world.particles.add_particle('player', self.pos, 'circle', [(random.randint(0, 10) / 10 - 0.5) * 10, (random.randint(0, 20) / 10 - 2) * 10], 15, 0 + random.randint(0, 20) / 10, custom_color=self.colors[2], glow=(6, 6, 18), glow_radius=2)
            self.game.world.particles.render('player', surf, scroll)
            surf.blit(self.img, (self.pos[0] - self.img.get_width() // 2, self.pos[1] - self.img.get_height() // 2 - scroll))