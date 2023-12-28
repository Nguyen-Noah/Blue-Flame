import pygame, math
from .core_funcs import itr, advance

GLOW_CACHE = {}
GLOW_SURFS = []

def glow(loc, radius, color):
    glow_id = (int(radius), color)
    
    if glow_id in GLOW_CACHE:
        GLOW_SURFS.append([GLOW_CACHE[glow_id], (loc[0] - radius, loc[1] - radius)])
        return None
    
    render_surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(render_surf, color, (radius, radius), radius)

    rotated_surf = render_surf

    GLOW_SURFS.append([rotated_surf, (loc[0] - rotated_surf.get_width() // 2, loc[1] - rotated_surf.get_height() // 2)])
    GLOW_CACHE[glow_id] = render_surf

def render_glow(surf):
    global GLOW_SURFS
    for glow in GLOW_SURFS:
        surf.blit(glow[0], glow[1], special_flags=pygame.BLEND_RGBA_ADD)
    GLOW_SURFS = []

class Circle:
    def __init__(self, game, owner, pos, radius, width, decay_rate, speed, color=(255, 255, 255), glow=True):
        self.game = game
        self.owner = owner
        self.pos = pos
        self.radius = radius
        self.width = width
        self.decay_rate = decay_rate
        self.speed = speed
        self.color = color
        self.glow = glow

    def update(self, dt=0):
        self.radius += self.speed * dt
        self.width -= self.decay_rate * dt
        self.pos = (self.owner.pos[0] + self.owner.radius, self.owner.pos[1] + self.owner.radius)
        if self.width <= 0:
            return False
        return True
    
    def render(self, surf, scroll=0):
        pygame.draw.circle(surf, self.color, [self.pos[0], self.pos[1] - scroll], int(self.radius), max(1, int(self.width)))

class Spark:
    def __init__(self, game, pos, angle, speed, decay):
        self.game = game
        self.pos = pos.copy()
        self.angle = angle
        self.speed = speed
        self.decay = decay
        self.points  = []

    def update(self, dt):
        self.points = []
        advance(self.pos, self.angle, self.speed)
        self.speed -= self.decay
        if self.speed <= 0:
            return False
        return True

    def render(self, surf, scroll=0):
        self.points = [
            (self.pos[0] + math.cos(self.angle) * (self.speed + 5), (self.pos[1] - scroll) + math.sin(self.angle) * (self.speed + 5)),
            (self.pos[0] + math.cos(self.angle + math.pi / 2) * (self.speed * 0.4), (self.pos[1] - scroll) + math.sin(self.angle + math.pi / 2) * (self.speed * 0.4)),
            (self.pos[0] + math.cos(self.angle + math.pi) * (self.speed + 5), (self.pos[1] - scroll) + math.sin(self.angle + math.pi) * (self.speed + 5)),
            (self.pos[0] + math.cos(self.angle - math.pi / 2) * (self.speed * 0.4), (self.pos[1] - scroll) + math.sin(self.angle - math.pi / 2) * (self.speed * 0.4))
        ]
        pygame.draw.polygon(surf, (255, 255, 255), self.points)

VFX_TYPES = {
    'circle': Circle,
    'spark': Spark
}

class VFX:
    def __init__(self, game):
        self.game = game
        self.effects = []

    def output_stats(self):
        print('- vfx -')
        print('len:', len(self.effects))

    def spawn_vfx(self, effect_type, *args, **kwargs):
        self.effects.append(VFX_TYPES[effect_type](self.game, *args, **kwargs))

    def update(self, dt):
        for i, effect in itr(self.effects):
            alive = effect.update(dt)
            if not alive:
                self.effects.pop(i)

    def render(self, surf, scroll=0):
        for effect in self.effects:
            effect.render(surf, scroll)