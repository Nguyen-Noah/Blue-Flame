import pygame, math, sys
from pygame.locals import *
from .core_funcs import get_dis

class Input:
    def __init__(self, game):
        self.game = game
        self.mouse_pos = (0, 0)
        self.retry = False

        self.reset()

    def reset(self):
        self.mouse_state = {
            'left_click': False,
            'right_click': False,
            'left_hold': False,
            'right_hold': False,
            'left_release': False,
            'right_release': False,
            'scroll_down': False,
            'scroll_up': False
        }

    def soft_reset(self):
        self.retry = False

        for binding in self.mouse_state:
            self.mouse_state[binding] = False
            
    def update(self):
        # get mouse pos
        mx, my = pygame.mouse.get_pos()
        self.mouse_pos = (int(mx / self.game.window.screen_resolution[0] * self.game.window.game_resolution[0]), int(my / self.game.window.screen_resolution[1] * self.game.window.game_resolution[1]))

        self.soft_reset()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == 27):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == 114:
                    self.retry = True

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_state['left_click'] = True
                    self.mouse_state['left_hold'] = True
                if event.button == 3:
                    self.mouse_state['right_click'] = True
                    self.mouse_state['right_hold'] = True
                if event.button == 4:
                    self.mouse_state['scroll_up'] = True
                if event.button == 5:
                    self.mouse_state['scroll_down'] = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_state['left_release'] = True
                    self.mouse_state['left_hold'] = False
                if event.button == 3:
                    self.mouse_state['right_release'] = True
                    self.mouse_state['right_hold'] = False