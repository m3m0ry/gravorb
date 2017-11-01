import pygame
import math
import numpy as np


class Shot:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation
        self.image = pygame.transform.rotate(pygame.image.load('resources/bullet1.png'), math.degrees(self.orientation))

    def tick(self, fps):
        velocity = 1000
        self.position = self.position - velocity * 1/fps * np.array([-math.cos(self.orientation), math.sin(self.orientation)])

    @property
    def image_position(self):
        return self.position[0] - self.image.get_width()/2, self.position[1] - self.image.get_height()/2



