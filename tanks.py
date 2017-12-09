import pygame

from tank import Tank
from map import generate_map
from handler import MouseHandler, KeyHandler


pygame.init()
clock = pygame.time.Clock()
map_size = (800, 640)
display_size = map_size  # TODO change in future
display_width, display_height = display_size
pygame.display.set_caption('Tanks')
screen = pygame.display.set_mode(display_size)

white = (255, 255, 255)
black = (0, 0, 0)
fps = 60

players = [Tank((display_height / 2, display_width / 2), pygame.image.load('resources/tank1.png'),
                pygame.image.load('resources/cannon1.png'))]
player = players[0]

# TODO use better render group
tanks = pygame.sprite.RenderPlain(players)
cannons = pygame.sprite.RenderPlain([player.cannon for player in players])
shots = pygame.sprite.RenderPlain()
walls = pygame.sprite.RenderPlain(generate_map())
active_groups = [tanks, cannons, shots]
all_groups = active_groups + [walls]
background = pygame.Surface(map_size)
background.fill(white)
walls.draw(background)
handlers = [KeyHandler(player), MouseHandler(player, shots)]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    for handler in handlers:
        handler.handle()

    screen.blit(background, (0, 0))

    shots.update(fps, walls)
    tanks.update(fps, tanks, shots, walls)
    cannons.update(fps)
    for group in active_groups:
        group.draw(screen)
    pygame.display.update()
    clock.tick(fps)

