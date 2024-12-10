import pygame
from pytmx.util_pygame import load_pygame

pygame.init()

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

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

zoom = 0.6
min_zoom = 0.2  # Zoom mínimo
max_zoom = 2.0  # Zoom máximo


def getScale():
    new_width = int(map_surface.get_width() * zoom)
    new_height = int(map_surface.get_height() * zoom)
    return pygame.transform.smoothscale(map_surface, (new_width, new_height))


# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS
            ):  # Tecla '+' ou '='
                zoom = min(zoom + 0.025, max_zoom)
            elif event.key == pygame.K_MINUS:  # Tecla '-'
                zoom = max(zoom - 0.025, min_zoom)
            elif event.key == pygame.K_ESCAPE:  # Tecla 'ESC' para do fullscreen
                running = False

    scaled_map_surface = getScale()

    map_rect = scaled_map_surface.get_rect(
        center=(screen_width // 2, screen_height // 2)
    )

    screen.fill((0, 0, 0))
    screen.blit(scaled_map_surface, map_rect.topleft)
    pygame.display.flip()

pygame.quit()
