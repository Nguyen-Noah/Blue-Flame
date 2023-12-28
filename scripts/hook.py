import pygame, math, random
from .core_funcs import advance, get_dis

class Hook:
    # states
    IDLE = 0
    DEPLOYING = 1
    STUCK = 2
    STUCK_REELING = 3
    REELING = 4

    def __init__(self, game, owner):
        self.game = game
        self.owner = owner
        self.pos = self.owner.pos.copy()
        self.limit = 2
        self.since_stuck = 0
        self.state = Hook.IDLE
        self.velocity = (0, 0)
        self.target = None

        self.game.audio.add('hit.wav', 0.3)

    @property
    def length(self):
        if not self.state == Hook.IDLE:
            return get_dis(self.owner.pos, self.pos)
        else:
            return 0

    def use(self):
        self.pos = self.owner.pos.copy()
        self.state = Hook.DEPLOYING
        target_pos = self.game.input.mouse_pos
        self.target = math.atan2(target_pos[1] - self.game.world.player.pos[1] + self.game.world.scroll, target_pos[0] - self.game.world.player.pos[0])
        self.velocity = (self.game.input.mouse_pos[0] - self.owner.pos[0], self.game.input.mouse_pos[1] - self.owner.pos[1] + self.game.world.scroll)
        for i in range(10):
            if i % 2 == 0:
                self.game.world.vfx.spawn_vfx('spark', self.owner.pos, self.target + random.random(), random.random() * 3 + 2, random.random() * 0.3 + 0.15)
            else:
                self.game.world.vfx.spawn_vfx('spark', self.owner.pos, self.target - random.random(), random.random() * 3 + 2, random.random() * 0.3 + 0.15)

    def retract(self):
        if not self.state == Hook.DEPLOYING:
            return
        self.state = Hook.REELING

    def hit(self, hit_entity):
        if not self.state == Hook.DEPLOYING:
            return
        self.game.audio.play('hit')
        self.state = Hook.STUCK
        self.since_stuck = 0
        hit_entity.hooked = True

    def reset(self):
        self.state = Hook.IDLE

    def update(self, dt):
        # getting the time that the hook is stuck
        if self.state == Hook.STUCK:
            if self.since_stuck > 0.1:
                self.state = Hook.STUCK_REELING
            self.since_stuck += dt
        elif self.state == Hook.STUCK_REELING:
            self.since_stuck += dt
        else:
            self.since_stuck = 0

        # reeling
        if self.state == Hook.REELING:
            self.velocity = (self.owner.pos[0] - self.pos[0], self.owner.pos[1], self.pos[1])

        # deploying the hook and adding a small offset
        if self.state == Hook.DEPLOYING:
            # actually moving the hook
            self.pos = advance(self.pos, self.target, amt=20)

            # owner offset
            self.owner.pos[0] -= self.velocity[0] * dt
            self.owner.pos[1] -= self.velocity[1] * dt

        # checking for collissions with the hook
        if self.state == Hook.DEPLOYING:
            for flare in self.game.world.flares.flares:
                if flare.rect.collidepoint(self.pos[0], self.pos[1]):
                    self.hit(flare)
            
    def render(self, surf, scroll=0):
        if not self.state == Hook.IDLE:
            pygame.draw.circle(surf, (200, 0, 0), (self.pos[0], self.pos[1] - scroll), 5)
            self.game.world.particles.add_particle('hook', self.pos, 'circle', [(random.randint(0, 10) / 10 - 0.5) * 10, (random.randint(0, 20) / 10 - 2) * 10], 20, random.randint(0, 20) / 10, custom_color=(255, 255, 255))
            self.game.world.particles.add_particle('hook', self.pos, 'circle', [(random.randint(0, 10) / 10 - 0.5) * 10, (random.randint(0, 20) / 10 - 2) * 10], 20, random.randint(30, 50) / 10, custom_color=(255, 255, 255), glow=(10, 10, 10), glow_radius=3)
            self.game.world.particles.render('hook', surf, scroll)