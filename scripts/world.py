import pygame, random
from .background import Background
from .player import Player
from .config import config
from .flare import FlareManager
from .particles import ParticleManager
from .healthbar import Healthbar
from .vfx import VFX, render_glow
from .title import Title

class World:
    def __init__(self, game):
        self.game = game
        self.border_width = config['world']['world_borders']
        self.game_time = 0
        self.scroll = 0
        self.since_enemy = 0
        self.score = 0
        self.difficulty_level = 1
        self.load()

    def load(self):
        self.title = Title(self.game)
        self.background = Background(self.game)
        self.particles = ParticleManager(self.game)
        self.flares = FlareManager(self.game)
        self.player = Player(self.game, (self.game.window.game_resolution[0] // 2, ((self.game.window.game_resolution[1] // 3) * 2) + 50))
        self.healthbar = Healthbar(self.game, self.player, ((self.border_width // 2) - 4, (self.game.window.game_resolution[1] / 5)))
        self.vfx = VFX(self.game)
        self.particles.add_group('healthbar')    

        self.game.audio.add('bg_music.ogg', 1)
        self.game.audio.add('explosion.wav', 0.7)

        # tutorial and opening
        self.flares.add_flare((self.game.window.game_resolution[0] // 2 - 10, (self.game.window.game_resolution[1] // 2)))
        self.tutorial_timer = 0
        self.has_started = False
        self.title_screen = True
        self.music_loaded = False

        self.black_cover = pygame.Surface((self.game.window.game_resolution))
        self.black_cover.fill((0, 0, 0))

        self.tutorial_shade = self.black_cover.copy()
        self.tutorial_shade_alpha = 0
        self.tutorial_shade_alpha_target = 0

    def start_game_loop(self):
        self.has_started = True
        self.player.gravity = 5

    def spawn_flare(self, top_flare):
        width = (self.game.window.game_resolution[0] - (self.border_width * 2))

        enemy_chance = 1
        height = -self.scroll/10
        self.difficulty_level = min(5, int(height / 500) + 1)
        if height < 500:
            enemy_chance = 1
        elif height < 1000:
            enemy_chance = 0.3
        elif height < 1500:
            enemy_chance = 0.2
        else:
            enemy_chance = 0.175

        if self.since_enemy != 0:
            if 1 / self.since_enemy < enemy_chance:
                enemy_chance = 1

        height_min = 100
        height_var = 300 + 200 * (-self.scroll) / 1000 / 50

        y = top_flare.pos[1] - (random.random() * height_var + height_min)

        if random.random() < enemy_chance:
            self.flares.add_flare((random.random() * width * 0.75 + self.border_width + width * 0.125, y))
            self.since_enemy = 0
        else:
            self.since_enemy += 1

    def update(self):
        dt = self.game.window.dt
        # updating the title screen
        if self.title.done and not self.music_loaded:
            self.game.audio.change_volume('title', 0)
            self.game.audio.play('bg_music', loop=-1)
            self.music_loaded = True
        else:
            self.title.update(dt)

        # tutorial shade and updating
        if not self.has_started and self.title.done:
            self.tutorial_timer -= dt

            self.tutorial_shade_alpha_target = 75
            self.tutorial_shade_alpha += dt * 200
            if self.tutorial_shade_alpha > self.tutorial_shade_alpha_target:
                self.tutorial_shade_alpha = self.tutorial_shade_alpha_target
        else:
            self.tutorial_shade_alpha -= dt * 200
            if self.tutorial_shade_alpha < 0:
                self.tutorial_shade_alpha = 0

        # MAIN GAMEPLAY
        if self.player.alive:
            self.game_time += dt
            self.score = -self.scroll / 10
            self.player.update(dt)

            # appending particles to the cursor
            for i in range(2):
                self.game.world.particles.add_particle('cursor', self.game.input.mouse_pos, 'circle', [(random.randint(0, 10) / 10 - 0.5) * 10, (random.randint(0, 20) / 10 - 2) * 10], 50, 0 + random.randint(0, 20) / 10, custom_color=(255, 0, 0))

            # vertical scroll
            if self.player.pos[1] - 200 < self.scroll:
                self.scroll += (self.player.pos[1] - 200 - self.scroll) / 10

            # wall collision
            if self.player.hook.state == 0:
                if self.player.pos[0] - self.player.radius < self.border_width:
                    self.game.audio.play('bump')
                    self.player.velocity[0] *= -1
                elif self.player.pos[0] + self.player.radius > self.game.window.game_resolution[0] - self.border_width:
                    self.game.audio.play('bump')
                    self.player.velocity[0] *= -1
            if self.player.hook.state == 1:
                if self.player.pos[0] - self.player.radius < self.border_width:
                    self.player.pos[0] = self.border_width + self.player.radius
                elif self.player.pos[0] + self.player.radius > self.game.window.game_resolution[0] - self.border_width:
                    self.player.pos[0] = self.game.window.game_resolution[0] - self.border_width - self.player.radius
                
            # if the player goes off camera, end the game
            if self.player.pos[1] - self.scroll > self.game.window.game_resolution[1] and self.player.hook.state == 0:
                self.player.die()

            if self.player.hook.state == 1:
                # crazy long if statement that basically checks if the hook hits any of the window borders
                if self.player.hook.pos[0] < self.border_width or self.player.hook.pos[0] > self.game.window.game_resolution[0] - self.border_width or self.player.hook.pos[1] - self.scroll > self.game.window.game_resolution[1] or self.player.hook.pos[1] - self.scroll < 0:
                    self.player.hook.reset()

            # spawning algo
            self.flares.sort()
            if self.flares.flares:
                top_flare = self.flares.get_first_ind()
            else:
                self.flares.add_flare((0, 0))
                top_flare = self.flares.get_first_ind()

            while top_flare.on_screen_pos[1] >= 0:
                self.spawn_flare(top_flare)
                self.flares.sort()
                top_flare = self.flares.get_first_ind()
        else:
            pass
        
        # updating everything else
        self.background.update()
        self.particles.update(dt)
        self.flares.update(dt)
        self.vfx.update(dt)
        self.healthbar.update(dt)

    def render(self, surf):
        if self.title.done:
            self.background.render(surf, self.scroll)
            self.player.hook.render(surf, self.scroll)          # render the hook behind the flares
            self.flares.render(surf, self.scroll)
            self.particles.render('cursor', surf)
            self.player.render(surf, self.scroll)
            self.vfx.render(surf, self.scroll)
            render_glow(surf)

            #borders
            border = pygame.Rect(0, 0, self.border_width, surf.get_height())
            pygame.draw.rect(surf, (10, 10, 10), border)
            border.x = surf.get_width() - self.border_width
            pygame.draw.rect(surf, (10, 10, 10), border)

            self.healthbar.render(surf)

            # rendering the tutorial
            if not self.has_started:
                # shade
                if self.tutorial_shade_alpha > 0:
                    self.tutorial_shade.set_alpha(self.tutorial_shade_alpha)
                    surf.blit(self.tutorial_shade, (0, 0))

                # blink tutorial click
                if self.tutorial_timer <= 0:
                    surf.blit(self.game.assets.game_assets['click_1'], (126, 195))
                    if self.tutorial_timer <= -1:
                        self.tutorial_timer = 0.5
                else:
                    surf.blit(self.game.assets.game_assets['click_0'], (126, 195))
        else:
            # rendering the title screen
            self.title.render(self.game.window.screen)