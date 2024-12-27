import pygame
from pytmx.util_pygame import load_pygame


class Board:
    def __init__(self):
        self.tmx_data = None
        self.map_surface = None
        self.zoom = 0.6
        self.min_zoom = 0.2
        self.max_zoom = 2.0

    def load_map(self):
        self.tmx_data = load_pygame("Board/board.tmx")
        self.map_surface = pygame.Surface(
            (
                self.tmx_data.width * self.tmx_data.tilewidth,
                self.tmx_data.height * self.tmx_data.tileheight,
            )
        )
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "data"):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        self.map_surface.blit(
                            tile,
                            (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight),
                        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_PLUS, pygame.K_EQUALS):  # Zoom in
                self.zoom = min(self.zoom + 0.025, self.max_zoom)
            elif event.key == pygame.K_MINUS:  # Zoom out
                self.zoom = max(self.zoom - 0.025, self.min_zoom)

    def draw(self, screen):
        scaled_map = self.get_scaled_map()
        map_rect = scaled_map.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2)
        )
        screen.blit(scaled_map, map_rect.topleft)

    def get_scaled_map(self):
        new_width = int(self.map_surface.get_width() * self.zoom)
        new_height = int(self.map_surface.get_height() * self.zoom)
        return pygame.transform.smoothscale(self.map_surface, (new_width, new_height))
