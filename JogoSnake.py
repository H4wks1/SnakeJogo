import pygame
import random
import sys

# --- Configurações Globais ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20  # Tamanho de cada quadrado da cobrinha
MAX_FOODS = 5    # Número máximo de comidas na tela
SNAKE_SPEED = 8  # Velocidade inicial da cobra

# Cores (Padrão RGB)
COLOR_BACKGROUND = (144, 238, 144) # Verde claro
COLOR_GRID = (130, 210, 130)       # Verde grade
COLOR_SNAKE_HEAD = (0, 100, 0)     # Verde escuro
COLOR_SNAKE_BODY = (0, 150, 0)     # Verde médio
COLOR_VEGETABLE = (255, 165, 0)    # Laranja
COLOR_FASTFOOD = (139, 69, 19)     # Marrom
COLOR_TEXT = (0, 0, 0)             # Preto (Melhor legibilidade no fundo verde)
COLOR_GAMEOVER = (200, 0, 0)       # Vermelho

# --- Inicialização do Pygame (DEVE VIR ANTES DE USAR FONTES OU TELA) ---
pygame.init() 

# Configuração da fonte
font = pygame.font.SysFont('Consolas', 25) 

# Cria a tela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jogo da Cobrinha na Horta')
clock = pygame.time.Clock()

# --- Funções do Jogo ---

def draw_grid():
    """Desenha uma grade no fundo para simular a horta."""
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, COLOR_GRID, (0, y), (SCREEN_WIDTH, y))

def spawn_food(snake_body, current_foods):
    """
    Gera uma nova comida em uma posição aleatória que não esteja sobre a cobra
    ou sobre outras comidas.
    """
    while True:
        food_pos = [
            random.randrange(0, SCREEN_WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
            random.randrange(0, SCREEN_HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
        ]
        
        # 1. Checa se está sobre a cobra
        on_snake = food_pos in snake_body
        
        # 2. Checa se está sobre outras comidas
        on_other_food = any(food_pos == f['pos'] for f in current_foods)
        
        if not on_snake and not on_other_food:
            break
            
    # Define o tipo de comida: 80% vegetal, 20% fast food
    if random.random() < 0.8:
        food_type = 'vegetable'
    else:
        food_type = 'fast_food'
        
    return {'pos': food_pos, 'type': food_type}

def manage_food(snake_body, current_foods):
    """Garante que haja MAX_FOODS na tela."""
    while len(current_foods) < MAX_FOODS:
        # Passa a lista atual para evitar sobreposição
        new_food = spawn_food(snake_body, current_foods)
        current_foods.append(new_food)
    return current_foods

def draw_elements(snake_body, foods, score): # MUDANÇA: 'food' para 'foods'
    """Desenha todos os elementos na tela: fundo, cobra, **todas as comidas** e pontuação."""
    screen.fill(COLOR_BACKGROUND)
    draw_grid()

    # Desenha o corpo da cobra
    for i, block in enumerate(snake_body):
        rect = pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE)
        if i == 0: # Cabeça da cobra
            pygame.draw.rect(screen, COLOR_SNAKE_HEAD, rect)
            pygame.draw.rect(screen, COLOR_TEXT, rect, 1) # Borda
        else: # Corpo
            pygame.draw.rect(screen, COLOR_SNAKE_BODY, rect)

    # Desenha TODAS as comidas
    for food in foods:
        food_rect = pygame.Rect(food['pos'][0], food['pos'][1], BLOCK_SIZE, BLOCK_SIZE)
        color = COLOR_VEGETABLE if food['type'] == 'vegetable' else COLOR_FASTFOOD
        pygame.draw.rect(screen, color, food_rect)

    # Desenha a pontuação
    score_text = font.render(f"Pontos: {score}", True, COLOR_TEXT)
    screen.blit(score_text, [10, 10])

def game_over_screen(score):
    """Mostra a tela de fim de jogo e aguarda uma ação do jogador."""
    game_over_font_big = pygame.font.SysFont('Consolas', 50)
    game_over_font_small = pygame.font.SysFont('Consolas', 25)

    # ... (Lógica de desenho da tela de Game Over)

    text_surface_big = game_over_font_big.render("FIM DE JOGO", True, COLOR_GAMEOVER)
    text_rect_big = text_surface_big.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    
    score_surface = game_over_font_small.render(f"Pontuação final: {score}", True, COLOR_TEXT)
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
    
    restart_surface = game_over_font_small.render("Pressione 'R' para reiniciar ou 'Q' para sair", True, COLOR_TEXT)
    restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 70))

    screen.blit(text_surface_big, text_rect_big)
    screen.blit(score_surface, score_rect)
    screen.blit(restart_surface, restart_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    # Chamar main() diretamente pode causar problemas de memória. 
                    # Uma abordagem melhor seria usar uma variável de estado, mas 
                    # para este exemplo, manteremos a chamada recursiva.
                    main() 

def main():
    """Função principal que executa o loop do jogo."""
    # Estado inicial do jogo
    snake_pos = [100, 60]
    snake_body = [
        [100, 60],
        [80, 60],
        [60, 60]
    ]
    direction = 'RIGHT'
    change_to = direction
    score = 0
    
    foods = []
    # Gera o número inicial de comidas
    foods = manage_food(snake_body, foods)

    # Loop principal do jogo
    while True:
        # --- Tratamento de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Lógica de mudança de direção
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                if event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'
        
        direction = change_to

        # --- Lógica de Movimento ---
        if direction == 'UP':
            snake_pos[1] -= BLOCK_SIZE
        elif direction == 'DOWN':
            snake_pos[1] += BLOCK_SIZE
        elif direction == 'LEFT':
            snake_pos[0] -= BLOCK_SIZE
        elif direction == 'RIGHT':
            snake_pos[0] += BLOCK_SIZE

        # --- Lógica das Bordas (Teleporte) ---
        if snake_pos[0] < 0:
            snake_pos[0] = SCREEN_WIDTH - BLOCK_SIZE
        elif snake_pos[0] >= SCREEN_WIDTH:
            snake_pos[0] = 0
        if snake_pos[1] < 0:
            snake_pos[1] = SCREEN_HEIGHT - BLOCK_SIZE
        elif snake_pos[1] >= SCREEN_HEIGHT:
            snake_pos[1] = 0
            
        # Adiciona a nova posição à cabeça da cobra
        snake_body.insert(0, list(snake_pos))
        
        food_eaten = False
        
        # --- Lógica de Colisão com Comida (Itera sobre TODAS as comidas) ---
        for food in list(foods): # Usamos list(foods) para iterar enquanto removemos
            if snake_pos == food['pos']:
                food_eaten = True
                foods.remove(food) # Remove a comida comida
                
                if food['type'] == 'vegetable':
                    score += 10
                    # A cobra cresce (não remove o rabo)
                elif food['type'] == 'fast_food':
                    score -= 5 # Penaliza por fast food
                    # Remove 3 blocos, mas garante que a cobra não desapareça
                    for _ in range(3):
                        if len(snake_body) > 3: # Garante tamanho mínimo
                            snake_body.pop()
                
                # Garante que uma nova comida seja gerada
                foods = manage_food(snake_body, foods)
                break # Sai do loop de comidas após a colisão

        # --- Lógica de Crescimento ---
        if not food_eaten: 
            snake_body.pop() # Se não comeu, remove o último bloco (movimento normal)

        # --- Lógica de Colisão com o Próprio Corpo ---
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over_screen(score)
                return # Encerra a função main atual

        # --- Atualização da Tela ---
        draw_elements(snake_body, foods, score) # MUDANÇA: Passa 'foods' (lista)
        pygame.display.flip()
        
        # Define a velocidade do jogo
        clock.tick(SNAKE_SPEED)

# Inicia o jogo
if __name__ == '__main__':
    main()