import pygame
import sys

# Inicializar o Pygame
pygame.init()

# Dimensões da janela e tabuleiro
BOARD_WIDTH, HEIGHT = 900, 800  # Largura reduzida para dar espaço à janela lateral
SIDE_PANEL_WIDTH = 300
WIDTH = BOARD_WIDTH + SIDE_PANEL_WIDTH
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brasópolis")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Configurações do tabuleiro
HORIZONTAL_CELLS = 14
VERTICAL_CELLS = 6
TOTAL_CELLS = HORIZONTAL_CELLS * 2 + VERTICAL_CELLS * 2
CELL_WIDTH = BOARD_WIDTH // HORIZONTAL_CELLS
CELL_HEIGHT = HEIGHT // (VERTICAL_CELLS + 2)

# Carregar imagens das casas
images = []
for i in range(1, TOTAL_CELLS + 1):
    try:
        image = pygame.image.load(f"brasopolis-POO/tabuleiro/images/{i}.png")
        image = pygame.transform.scale(image, (CELL_WIDTH, CELL_HEIGHT))
        images.append(image)
    except FileNotFoundError:
        images.append(None)

# Configuração do personagem
player_pos = 0  # Posição inicial do jogador

# Texto descritivo das casas
house_descriptions = [f"Descrição da Casa {i}" for i in range(1, TOTAL_CELLS + 1)]

# Função para desenhar o tabuleiro
def draw_board():
    for col in range(HORIZONTAL_CELLS):
        x = col * CELL_WIDTH
        y = 0
        draw_cell(x, y, col)
    for row in range(1, VERTICAL_CELLS + 1):
        x = BOARD_WIDTH - CELL_WIDTH
        y = row * CELL_HEIGHT
        draw_cell(x, y, HORIZONTAL_CELLS + row - 1)
    for col in range(HORIZONTAL_CELLS):
        x = BOARD_WIDTH - (col + 1) * CELL_WIDTH
        y = HEIGHT - CELL_HEIGHT
        draw_cell(x, y, HORIZONTAL_CELLS + VERTICAL_CELLS + col)
    for row in range(1, VERTICAL_CELLS + 1):
        x = 0
        y = HEIGHT - (row + 1) * CELL_HEIGHT
        draw_cell(x, y, 2 * HORIZONTAL_CELLS + VERTICAL_CELLS + row - 1)

    pygame.draw.rect(screen, WHITE, (CELL_WIDTH, CELL_HEIGHT, BOARD_WIDTH - 2 * CELL_WIDTH, HEIGHT - 2 * CELL_HEIGHT))

def draw_cell(x, y, index):
    if images[index] is not None:
        screen.blit(images[index], (x, y))

def draw_player():
    x, y = get_player_position(player_pos)
    pygame.draw.circle(screen, RED, (x + CELL_WIDTH // 2, y + CELL_HEIGHT // 2), 20)

def get_player_position(position):
    if position < HORIZONTAL_CELLS:
        return position * CELL_WIDTH, 0
    elif position < HORIZONTAL_CELLS + VERTICAL_CELLS:
        return BOARD_WIDTH - CELL_WIDTH, (position - HORIZONTAL_CELLS + 1) * CELL_HEIGHT
    elif position < 2 * HORIZONTAL_CELLS + VERTICAL_CELLS:
        return BOARD_WIDTH - (position - HORIZONTAL_CELLS - VERTICAL_CELLS + 1) * CELL_WIDTH, HEIGHT - CELL_HEIGHT
    else:
        return 0, HEIGHT - (position - 2 * HORIZONTAL_CELLS - VERTICAL_CELLS + 1) * CELL_HEIGHT

def move_player(key):
    global player_pos
    if key == pygame.K_RIGHT:
        player_pos = (player_pos + 1) % TOTAL_CELLS
    elif key == pygame.K_LEFT:
        player_pos = (player_pos - 1) % TOTAL_CELLS

def draw_side_panel():
    pygame.draw.rect(screen, WHITE, (BOARD_WIDTH, 0, SIDE_PANEL_WIDTH, HEIGHT))
    font = pygame.font.Font(None, 36)

    # Imagem da casa
    if images[player_pos] is not None:
        original_width, original_height = images[player_pos].get_size()

        # Calcular as dimensões escaladas mantendo a proporção 3:4
        target_width = SIDE_PANEL_WIDTH - 20
        target_height = int(target_width * 4 / 3)

        # Garantir que a imagem caiba no painel sem ultrapassar o limite
        if target_height > HEIGHT // 2:
            target_height = HEIGHT // 2
            target_width = int(target_height * 3 / 4)

        # Redimensionar a imagem
        scaled_image = pygame.transform.scale(images[player_pos], (target_width, target_height))

        # Centralizar a imagem no painel lateral
        image_x = BOARD_WIDTH + (SIDE_PANEL_WIDTH - target_width) // 2
        image_y = 20
        screen.blit(scaled_image, (image_x, image_y))

    # Texto descritivo
    text = font.render(house_descriptions[player_pos], True, BLACK)
    text_rect = text.get_rect(midtop=(BOARD_WIDTH + SIDE_PANEL_WIDTH // 2, HEIGHT // 3 + 40))
    screen.blit(text, text_rect)


def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                move_player(event.key)

        screen.fill(WHITE)
        draw_board()
        draw_player()
        draw_side_panel()
        pygame.display.flip()
        clock.tick(30)

main()
