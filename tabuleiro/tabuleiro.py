import pygame
import sys

# Inicializar o Pygame
pygame.init()

# Definir as dimensões da janela e do tabuleiro
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brasópolis")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Cor para o personagem

# Configurações do tabuleiro
BOARD_SIZE = 8  # Número de casas em cada linha e coluna
CELL_SIZE = WIDTH // BOARD_SIZE  # Tamanho de cada casa

# Carregar imagens para as casas
images = []
for i in range(1, BOARD_SIZE ** 2 + 1):
    try:
        image = pygame.image.load(f"images/{i}.png")  # Nomeie as imagens como 1.png, 2.png, etc.
        image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))  # Ajustar ao tamanho da casa
        images.append(image)
    except FileNotFoundError:
        images.append(None)  # Se a imagem não existir, coloca None

# Configuração do personagem
player_pos = [0, 0]  # Começa na posição inicial (0,0)

# Função para desenhar o tabuleiro
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Calcular a posição da casa
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            # Alternar a cor de cada casa (xadrez)
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

            # Desenhar o número da casa
            cell_number = row * BOARD_SIZE + col + 1
            font = pygame.font.Font(None, 36)
            text = font.render(str(cell_number), True, BLACK if color == WHITE else WHITE)
            text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            screen.blit(text, text_rect)

            # Inserir a imagem na casa, se disponível
            image_index = cell_number - 1
            if images[image_index] is not None:
                screen.blit(images[image_index], (x, y))

# Função para desenhar o personagem
def draw_player():
    x, y = player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE
    pygame.draw.circle(screen, RED, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 4)

# Função para mover o personagem
def move_player(key):
    if key == pygame.K_UP and player_pos[0] > 0:
        player_pos[0] -= 1
    elif key == pygame.K_DOWN and player_pos[0] < BOARD_SIZE - 1:
        player_pos[0] += 1
    elif key == pygame.K_LEFT and player_pos[1] > 0:
        player_pos[1] -= 1
    elif key == pygame.K_RIGHT and player_pos[1] < BOARD_SIZE - 1:
        player_pos[1] += 1

# Loop principal do jogo
def main():
    clock = pygame.time.Clock()
    
    while True:
        # Verificar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                move_player(event.key)

        # Desenhar o tabuleiro e o personagem
        screen.fill(WHITE)
        draw_board()
        draw_player()
        
        # Atualizar a tela
        pygame.display.flip()
        clock.tick(30)  # Limita a 30 FPS

# Executar o jogo
main()
