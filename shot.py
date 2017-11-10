import pygame
import math
import numpy as np
from pygame.sprite import Sprite


class Shot(Sprite):
    def __init__(self, position, orientation):
        super().__init__()
        self.position = position
        self.orientation = orientation
        self.image = pygame.transform.rotate(pygame.image.load('resources/bullet1.png'), math.degrees(self.orientation))
        self.size = self.image.get_size()

    def update(self, fps):
        velocity = 1000
        self.position = self.position - velocity * 1/fps * np.array([-math.cos(self.orientation), math.sin(self.orientation)])

    @property
    def rect(self):
        image_position = self.position[0] - self.image.get_width()/2, self.position[1] - self.image.get_height()/2
        return pygame.Rect(image_position, self.size)



