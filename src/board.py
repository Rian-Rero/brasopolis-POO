import pygame
from pytmx.util_pygame import load_pygame
from house import House


class Board:
    """Gerencia o tabuleiro e suas casas."""

    def __init__(self):
        self.tmx_data = None
        self.map_surface = None
        self.houses = []
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

        # Criar objetos House
        self.houses = []
        for obj in self.tmx_data.objects:
            house = House(
                name=obj.name,
                custom_name=obj.properties.get("customName", "Sem Nome"),
                custom_type=obj.properties.get("customType", "Sem Tipo"),
                custom_price=obj.properties.get("customPrice", 0),
                x=obj.x,
                y=obj.y,
                width=obj.width,
                height=obj.height,
            )
            self.houses.append(house)

    # def load_houses(self):
    #     """Carrega as casas da camada de objetos."""
    #     for obj in self.tmx_data.objects:
    #         print(self.tmx_data.objects)
    #         if obj.type == "House":
    #             house = House(
    #                 name=obj.name,
    #                 x=obj.x,
    #                 y=obj.y,
    #                 width=obj.width,
    #                 height=obj.height,
    #                 properties=obj.properties,
    #             )
    #             self.houses.append(house)

    def showHouses(self):
        for house in self.houses:
            print(house)

    def handle_event(self, event):
        """Trata eventos para controle de zoom."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_PLUS, pygame.K_EQUALS):  # Zoom in
                self.zoom = min(self.zoom + 0.025, self.max_zoom)
            elif event.key == pygame.K_MINUS:  # Zoom out
                self.zoom = max(self.zoom - 0.025, self.min_zoom)

    def draw(self, screen):
        """Desenha o tabuleiro e as casas."""
        scaled_map = self.get_scaled_map()
        map_rect = scaled_map.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2)
        )
        screen.blit(scaled_map, map_rect.topleft)

    def get_scaled_map(self):
        """Obtém o mapa com o zoom aplicado."""
        new_width = int(self.map_surface.get_width() * self.zoom)
        new_height = int(self.map_surface.get_height() * self.zoom)
        return pygame.transform.smoothscale(self.map_surface, (new_width, new_height))
