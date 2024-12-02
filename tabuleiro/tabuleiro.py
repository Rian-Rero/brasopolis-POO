import pygame
import sys

# Inicializar o Pygame
pygame.init()

# Definir as dimensões da janela e do tabuleiro
WIDTH, HEIGHT = 1200, 800  # Ajustar proporções para retangular
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brasópolis")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Cor para o personagem

# Configurações do tabuleiro
HORIZONTAL_CELLS = 14  # Número de casas horizontais (superior/inferior)
VERTICAL_CELLS = 6     # Número de casas verticais (laterais)
TOTAL_CELLS = HORIZONTAL_CELLS * 2 + VERTICAL_CELLS * 2
CELL_WIDTH = WIDTH // HORIZONTAL_CELLS
CELL_HEIGHT = HEIGHT // (VERTICAL_CELLS + 2)

# Verificando caminho das imagens
import os
print("Caminho atual:", os.getcwd())

# Carregar imagens para as casas
images = []
for i in range(1, TOTAL_CELLS + 1):
    try:
        image = pygame.image.load(f"brasopolis-POO/tabuleiro/images/{i}.png")
        image = pygame.transform.scale(image, (CELL_WIDTH, CELL_HEIGHT))
        images.append(image)
    except FileNotFoundError:
        images.append(None)

# Configuração do personagem
player_pos = 0  # Posição inicial do jogador na borda

# Função para desenhar o tabuleiro
def draw_board():
    # Bordas horizontais superiores
    for col in range(HORIZONTAL_CELLS):
        x = col * CELL_WIDTH
        y = 0
        draw_cell(x, y, col)

    # Bordas verticais direitas
    for row in range(1, VERTICAL_CELLS + 1):
        x = WIDTH - CELL_WIDTH
        y = row * CELL_HEIGHT
        draw_cell(x, y, HORIZONTAL_CELLS + row - 1)

    # Bordas horizontais inferiores
    for col in range(HORIZONTAL_CELLS):
        x = WIDTH - (col + 1) * CELL_WIDTH
        y = HEIGHT - CELL_HEIGHT
        draw_cell(x, y, HORIZONTAL_CELLS + VERTICAL_CELLS + col)

    # Bordas verticais esquerdas
    for row in range(1, VERTICAL_CELLS + 1):
        x = 0
        y = HEIGHT - (row + 1) * CELL_HEIGHT
        draw_cell(x, y, 2 * HORIZONTAL_CELLS + VERTICAL_CELLS + row - 1)

    # Espaço central
    pygame.draw.rect(
        screen,
        WHITE,
        (CELL_WIDTH, CELL_HEIGHT, WIDTH - 2 * CELL_WIDTH, HEIGHT - 2 * CELL_HEIGHT),
    )

# Função para desenhar uma casa individual
def draw_cell(x, y, index):
    # Alternar cores
    #color = WHITE if index % 2 == 0 else BLACK
    #pygame.draw.rect(screen, color, (x, y, CELL_WIDTH, CELL_HEIGHT))

    # Inserir a imagem na casa, se disponível
    if images[index] is not None:
        screen.blit(images[index], (x, y))

    # Desenhar número da casa
    #font = pygame.font.Font(None, 36)
    #text = font.render(str(index + 1), True, BLACK if color == WHITE else WHITE)
    #text_rect = text.get_rect(center=(x + CELL_WIDTH // 2, y + CELL_HEIGHT // 2))
    #screen.blit(text, text_rect)

# Função para desenhar o personagem
def draw_player():
    x, y = get_player_position(player_pos)
    pygame.draw.circle(screen, RED, (x + CELL_WIDTH // 2, y + CELL_HEIGHT // 2), 20)

# Calcular posição do jogador
def get_player_position(position):
    if position < HORIZONTAL_CELLS:  # Topo
        return position * CELL_WIDTH, 0
    elif position < HORIZONTAL_CELLS + VERTICAL_CELLS:  # Direita
        return WIDTH - CELL_WIDTH, (position - HORIZONTAL_CELLS + 1) * CELL_HEIGHT
    elif position < 2 * HORIZONTAL_CELLS + VERTICAL_CELLS:  # Base
        return WIDTH - (position - HORIZONTAL_CELLS - VERTICAL_CELLS + 1) * CELL_WIDTH, HEIGHT - CELL_HEIGHT
    else:  # Esquerda
        return 0, HEIGHT - (position - 2 * HORIZONTAL_CELLS - VERTICAL_CELLS + 1) * CELL_HEIGHT

# Função para mover o jogador
def move_player(key):
    global player_pos
    if key == pygame.K_RIGHT:
        player_pos = (player_pos + 1) % TOTAL_CELLS
    elif key == pygame.K_LEFT:
        player_pos = (player_pos - 1) % TOTAL_CELLS

# Loop principal do jogo
def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                move_player(event.key)

        # Atualizar a tela
        screen.fill(WHITE)
        draw_board()
        draw_player()
        pygame.display.flip()
        clock.tick(30)

# Executar o jogo
main()
