from pygame.sprite import Sprite
import pygame

import numpy as np
import random


def collision(sprite, group):
    potential_walls = pygame.sprite.spritecollide(sprite, group, False)
    for wall in potential_walls:
        if pygame.sprite.collide_mask(wall, sprite):
            yield wall


def generate_map(size=(800, 640), walls=list(), filled = 0.1):
    walls.append(Wall((0, 0), (size[0], 10)))
    walls.append(Wall((0, size[1]-10), (size[0], 10)))
    walls.append(Wall((0, 0), (10, size[1])))
    walls.append(Wall((size[0]-10, 0), (10, size[1])))
    for _ in range(0, 100):
        walls.append(Wall((random.randint(0, size[0]), random.randint(0, size[1]))))

    return walls


class Wall(Sprite):
    def __init__(self, position, size=(10, 10)):
        super().__init__()
        self.position = position[0] + size[0]/2, position[1] + size[1]/2
        self.size = size
        self.image = pygame.Surface(size, flags=pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 255))
        self.rect = pygame.Rect(position, size)
        self.mask = pygame.mask.from_surface(self.image)
