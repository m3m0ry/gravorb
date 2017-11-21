import pygame

from tank import Tank
from handler import MouseHandler, KeyHandler


pygame.init()
clock = pygame.time.Clock()
display_width, display_height = (800, 640)
pygame.display.set_caption('Tanks')
screen = pygame.display.set_mode((display_width, display_height))

white = (255, 255, 255)
black = (0, 0, 0)
background = pygame.image.load('resources/world1.png')
fps = 60


players = [Tank((display_height / 2, display_width / 2), pygame.image.load('resources/tank1.png'),
                pygame.image.load('resources/cannon1.png'))]
player = players[0]

# TODO use better render group
tanks = pygame.sprite.RenderPlain(players)
cannons = pygame.sprite.RenderPlain([player.cannon for player in players])
shots = pygame.sprite.RenderPlain()
groups = [tanks, cannons, shots]
handlers = [KeyHandler(player), MouseHandler(player, shots)]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    for handler in handlers:
        handler.handle()

    print(shots)

    screen.blit(background, (0, 0))
    for group in groups:
        group.update(fps)
        group.draw(screen)
    pygame.display.update()
    clock.tick(fps)

