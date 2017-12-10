import pygame
import math
import numpy as np
from pygame.sprite import Sprite

from client.map import collision


class Shot(Sprite):
    def __init__(self, position, orientation, tank=None, live=10):
        super().__init__()
        self.position = position
        self.orientation = orientation
        self.image = pygame.transform.rotate(pygame.image.load('resources/bullet1.png'), math.degrees(self.orientation))
        self.live = live
        self.tank = tank

    def update(self, fps, walls):
        self.live -= 1/fps
        if self.live < 0:
            self.kill()
        velocity = 800
        self.position = self.position - velocity * 1/fps * np.array([-math.cos(self.orientation), math.sin(self.orientation)])
        for _ in collision(self, walls):
            self.kill()

    @property
    def rect(self):
        return self.image.get_rect(center=self.position)



