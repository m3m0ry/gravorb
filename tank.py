import numpy as np
import math
import pygame
from enum import Enum


class Direction(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4


class Tank(object):
    def __init__(self, position, image):
        self._position = np.array(position)
        self._image = image
        self.velocity = 0
        self.acceleration = np.array([0, 0])
        self.forward = 0
        self.turn = 0
        self.orientation = math.radians(90)

    def movement(self, direction):
        if direction == Direction.FORWARD:
            self.forward = 1
        elif direction == Direction.BACKWARD:
            self.forward = -1
        elif direction == Direction.LEFT:
            self.turn = 1
        elif direction == Direction.RIGHT:
            self.turn = -1

    def tick(self, fps):
        if self.forward == 0 or (self.forward < 0 < self.velocity) or (self.forward > 0 > self.velocity):
            if math.fabs(self.velocity) > 3:
                self.velocity = self.velocity + (6 if self.velocity < 0 else -6)
            else:
                self.velocity = 0
        new_velocity = self.velocity + self.forward * 3
        self.velocity = new_velocity if np.linalg.norm(new_velocity) <= 180 else self.velocity
        self._position = self._position - self.velocity * 1/fps * np.array([-math.cos(self.orientation), math.sin(self.orientation)])

        self.orientation += math.radians(self.turn*2)
        self.forward = 0
        self.turn = 0

    @property
    def position(self):
        return self._position[0] - self.image.get_width()/2, self._position[1] - self.image.get_height()/2

    @position.setter
    def position(self, value):
        self._position = np.array(value)

    @property
    def image(self):
        return pygame.transform.rotate(self._image, math.degrees(self.orientation))

