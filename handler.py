import pygame
from pygame.locals import *
from actions import Forward, Backward, Left, Right, Aim, Fire


class Handler:
    def handle(self):
        pass


class MouseHandler(Handler):
    def __init__(self, tank):
        self.mouse_key_settings = [Fire(tank), None, None]
        self.mouse_position_settings = Aim(tank)

    def handle(self):
        mouse_position = pygame.mouse.get_pos()
        self.mouse_position_settings(mouse_position)

        mouse_keys = pygame.mouse.get_pressed()
        for key, state in enumerate(mouse_keys):
            if state and self.mouse_key_settings[key] is not None:
                self.mouse_key_settings[key]()


class KeyHandler(Handler):
    def __init__(self, tank):
        forward, backward, left, right, aim, fire = Forward(tank), Backward(tank), Left(tank), Right(tank), Aim(
            tank), Fire(tank)
        self.key_settings = {K_UP: forward, K_w: forward, K_DOWN: backward, K_s: backward, K_LEFT: left, K_a: left,
                             K_RIGHT: right,
                             K_d: right}

    def handle(self):
        keys = pygame.key.get_pressed()
        for key, state in enumerate(keys):
            if key in self.key_settings and state:
                self.key_settings[key]()