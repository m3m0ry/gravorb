import pygame
from pygame.locals import *

from tank import Tank, Direction
from actions import Forward, Backward, Left, Right


pygame.init()
clock = pygame.time.Clock()
display_width, display_height = (800, 640)
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tanks')
fps = 60

white = (255, 255, 255)
black = (0, 0, 0)

players = [Tank((display_height / 2, display_width / 2), pygame.image.load('resources/tank1.png'))]
player = players[0]
forward, backward, left, right = Forward(player), Backward(player), Left(player), Right(player)
key_handlers = {K_UP: forward, K_w: forward, K_DOWN: backward, K_s: backward, K_LEFT: left, K_a: left, K_RIGHT: right, K_d: right}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Handle pressed keys
    keys = pygame.key.get_pressed()
    for key, state in enumerate(keys):
        if state and key in key_handlers:
            key_handlers[key]()

    screen.fill(white)
    for player in players:
        player.tick(fps)
        screen.blit(player.image, player.position)
    pygame.display.update()
    clock.tick(fps)

