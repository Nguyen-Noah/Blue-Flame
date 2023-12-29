import pygame, math
from .core_funcs import get_magnitude, clamp

class Flare:
    def __init__(self, game, pos, recharge=True):
        self.game = game
        self.img = self.game.assets.game_assets['temp_flare']
        self.radius = self.img.get_width() // 2
        self.pos = list(pos)
        self.recharge = recharge
        self.on_screen_pos = self.pos.copy()
        self.alive = True
        self.hooked = False
        self.hook_direction = None
        self.hook_pos_difference = 0

    @property
    def rect(self):
        img_rect = self.img.get_rect()
        padding = 2
        return pygame.Rect(img_rect[0] + self.pos[0] - padding, img_rect[1] + self.pos[1] - padding, img_rect[2] + (padding * 2), img_rect[3] + (padding * 2))
    
    def outline(self, surf, scroll=0):
        mask = pygame.mask.from_surface(self.img)
        mask_outline = mask.outline()
        mask_surf = pygame.Surface(self.img.get_size())
        for pixel in mask_outline:
            mask_surf.set_at(pixel, (255, 255, 255))
        mask_surf.set_colorkey((0, 0, 0))
        surf.blit(mask_surf, (self.pos[0] - 1, self.pos[1] - scroll))
        surf.blit(mask_surf, (self.pos[0] + 1, self.pos[1] - scroll))
        surf.blit(mask_surf, (self.pos[0], self.pos[1] - 1 - scroll))
        surf.blit(mask_surf, (self.pos[0], self.pos[1] + 1 - scroll))

    def absorb(self):
        if not self.game.world.player.hook.state == 3:
            return
        
        dist = [(self.pos[0] + self.radius) - self.game.world.player.pos[0], (self.pos[1] + self.radius) - self.game.world.player.pos[1]]
        push = dist
        curr_magnitude = get_magnitude(push[0], push[1])

        if curr_magnitude == 0:
            push = (0, -1)
        push[0] *= 0.2
        push[1] = -10

        push[0] = clamp(push[0], -5, 5)

        self.game.world.player.velocity = push
        self.game.world.player.hook.reset()
        self.alive = False
        self.game.audio.play('explosion')
        self.game.world.score += 10 * self.game.world.difficulty_level

        self.game.window.add_screen_shake(4)
        if self.recharge:
            self.game.world.player.add_health(math.ceil(self.game.world.difficulty_level))

        # args: type, position, radius, width, decay_rate, speed
        self.game.world.vfx.spawn_vfx('circle', self, (self.pos[0] + self.radius, self.pos[1] + self.radius), 20, 15, 40, 100)
        self.game.world.vfx.spawn_vfx('circle', self, (self.pos[0] + self.radius, self.pos[1] + self.radius), 20, 20, 90, 300)

    def update(self, dt):
        # if the flare passed the screen, just delete it
        if self.pos[1] - self.game.world.scroll > self.game.window.game_resolution[1] and not self.hooked:
            self.alive = False

        self.on_screen_pos[1] = self.pos[1] - self.game.world.scroll

        # get the current distance from the player
        dist_from_player = ((self.pos[0] + self.radius) - self.game.world.player.pos[0], (self.pos[1] - self.radius) - self.game.world.player.pos[1])

        # if i am hooked, do a small offset
        if self.hooked:
            if self.hook_direction == None:
                self.hook_direction = self.game.world.player.pos[1] > self.pos[1]
                self.hook_pos_difference = self.game.world.player.pos[1] - self.pos[1]

            self.pos[0] -= dist_from_player[0] * dt * 0.6
            self.pos[1] -= dist_from_player[1] * dt * 0.6

            self.game.world.player.hook.pos[0] -= dist_from_player[0] * dt * 0.6
            self.game.world.player.hook.pos[1] -= dist_from_player[1] * dt * 0.6

            # if the distance from the player is less than 10
            if self.game.world.player.hook.length < self.radius + self.game.world.player.radius:
                self.absorb()

            # corner case bug that made the player slingshot if the hook is too long
            if self.hook_direction and self.game.world.player.pos[1] < self.pos[1] and self.hook_pos_difference > 100:
                # player below
                self.absorb()
            elif not self.hook_direction and self.game.world.player.pos[1] > self.pos[1] and self.hook_pos_difference < -100:
                # player above
                self.absorb()
                
        if not self.game.world.player.hook.state in [2, 3]:
            self.hooked = False

        return self.alive

    def render(self, surf, scroll=0):
        surf.blit(self.img, (self.pos[0], self.pos[1] - scroll))

class FlareManager:
    def __init__(self, game):
        self.game = game
        self.flares = []
        self.blink_timer = 0

    def add_flare(self, pos):
        self.flares.append(Flare(self.game, pos))

    def sort(self):
        self.flares.sort(key=lambda x: x.on_screen_pos[1])

    def get_first_ind(self):
        return self.flares[0]
    
    def reset(self):
        self.flares = []

    def update(self, dt):
        self.blink_timer -= dt

        for i, flare in enumerate(self.flares):
            alive = flare.update(dt)
            if not alive:
                self.flares.pop(i)

    def render(self, surf, scroll=0):
        for flare in self.flares:
            if self.blink_timer <= 0:
                flare.outline(surf, scroll)
                if self.blink_timer <= -1:
                    self.blink_timer = 0.5
            flare.render(surf, scroll)

    def output_stats(self):
        print('- flare debug -')
        print('length:', len(self.flares))