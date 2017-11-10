import numpy as np
import math
import pygame
from enum import Enum
from pygame.sprite import Sprite


class Direction(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4


class Tank(Sprite):
    def __init__(self, position, tank_image, cannon_image):
        super().__init__()
        self._position = np.array(position)
        self._image = tank_image  # Internal image
        self.cannon = Cannon(cannon_image, self)
        self.velocity = 0
        self.forward = 0
        self.turn = 0
        self.orientation = math.radians(90)
        self.image = pygame.transform.rotate(self._image, math.degrees(self.orientation))  # Image for representation
        self.reload = 0

    def movement(self, direction):
        if direction == Direction.FORWARD:
            self.forward = 1
        elif direction == Direction.BACKWARD:
            self.forward = -1
        elif direction == Direction.LEFT:
            self.turn = 1
        elif direction == Direction.RIGHT:
            self.turn = -1

    def aim(self, cursor_position):
        winkel = -np.arctan2(cursor_position[1] - self.position[1], cursor_position[0] - self.position[0])
        self.cannon.orientation = winkel

    def fire(self):
        if self.reload <= 0:
            self.reload = 30
            return True
        else:
            print('reloading')
            return False

    def update(self, fps):
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

        self.image = pygame.transform.rotate(self._image, math.degrees(self.orientation))
        #self.cannon.update(fps)

        if self.reload > 0:
            self.reload -= fps/100

    @property
    def rect(self):
        image_position = self._position[0] - self.image.get_width()/2, self._position[1] - self.image.get_height()/2
        return pygame.Rect(image_position, self.image.get_size())

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = np.array(value)


class Cannon(Sprite):
    def __init__(self, image, tank):
        super().__init__()
        self._image = image
        self.tank = tank
        self.orientation = math.radians(90)
        self.length = image.get_width()
        self.width = image.get_height()
        self.image = pygame.transform.rotate(self._image, math.degrees(self.orientation))

    @property
    def rect(self):
        sin = math.sin(self.orientation)
        cos = math.cos(self.orientation)
        width_shift = cos < 0
        height_shift = sin > 0
        adjustment_direction = -1 if (width_shift ^ height_shift) else 1

        #print(sin, cos, self.orientation, math.degrees(self.orientation))
        center = self.tank.position
        width, height = self.image.get_size()
        image_position = (center[0] - width_shift*width + adjustment_direction*self.width/2 * sin,
                          center[1] - height_shift*height + adjustment_direction*self.width/2 * -cos)
        return pygame.Rect(image_position, (width, height))

    def update(self, fps):
        self.image = pygame.transform.rotate(self._image, math.degrees(self.orientation))

