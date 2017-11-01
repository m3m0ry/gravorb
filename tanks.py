import pygame

from tank import Tank
from handler import MouseHandler, KeyHandler


pygame.init()
clock = pygame.time.Clock()
display_width, display_height = (800, 640)
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tanks')
fps = 60

white = (255, 255, 255)
black = (0, 0, 0)

players = [Tank((display_height / 2, display_width / 2), pygame.image.load('resources/tank2.png'),
                pygame.image.load('resources/cannon1.png'))]
player = players[0]
shots = []
handlers = [KeyHandler(player), MouseHandler(player, shots)]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    for handler in handlers:
        handler.handle()

    print(shots)
    screen.fill(white)
    for player in players:
        player.tick(fps)
        screen.blit(player.image, player.image_position)
        screen.blit(player.cannon.image, player.cannon.image_position)
    for shot in shots:
        shot.tick(fps)
        screen.blit(shot.image, shot.image_position)

    pygame.display.update()
    clock.tick(fps)

