import numpy as np


class Player:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation
        self.velocity = np.array([0,0], dtype=float)
        self.keys_pressed = {'up': False, 'down': False, 'left': False, 'right': False}
