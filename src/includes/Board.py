import pygame
from pytmx.util_pygame import load_pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

tmxData = load_pygame("TabuleiroMap.tmx")
map_surface = pygame.Surface(
    (tmxData.width * tmxData.tilewidth, tmxData.height * tmxData.tileheight)
)

for layer in tmxData.visible_layers:
    if hasattr(layer, "data"):
        for x, y, gid in layer:
            tile = tmxData.get_tile_image_by_gid(gid)
            if tile:
                map_surface.blit(tile, (x * tmxData.tilewidth, y * tmxData.tileheight))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(map_surface, (0, 0))
    pygame.display.flip()

pygame.quit()
