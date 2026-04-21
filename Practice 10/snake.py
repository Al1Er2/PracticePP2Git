import pygame
import random
import time

# Initialize Pygame
pygame.init()

# --- Configuration & Constants ---
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20  # Size of snake segment and food

# Initialize Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Level Up Edition')
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def display_score(score, level):
    """Displays current score and level on the screen."""
    value = score_font.render(f"Score: {score}  Level: {level}", True, YELLOW)
    screen.blit(value, [10, 10])

def draw_snake(block_size, snake_list):
    """Draws each segment of the snake."""
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], block_size, block_size])

def generate_food(snake_list):
    """Generates random food position that doesn't collide with the snake body."""
    while True:
        food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        
        # Ensure food is not spawning inside the snake body
        if [food_x, food_y] not in snake_list:
            return food_x, food_y

def game_loop():
    game_over = False
    game_close = False

    # Snake Initial Position
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1

    # Initial Stats
    score = 0
    level = 1
    speed = 10 
    food_x, food_y = generate_food(snake_list)

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            msg = font_style.render("Game Over! Press C-Play Again or Q-Quit", True, RED)
            screen.blit(msg, [WIDTH / 6, HEIGHT / 3])
            display_score(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        # --- 1. Border Collision Detection ---
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        
        # Draw Food
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
        
        # Snake Movement Logic
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # --- 2. Self Collision Detection ---
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)
        display_score(score, level)

        pygame.display.update()

        # --- 3. Eating Food & Leveling Up ---
        if x1 == food_x and y1 == food_y:
            food_x, food_y = generate_food(snake_list)
            length_of_snake += 1
            score += 1

            # Check for level up every 3 foods
            if score % 3 == 0:
                level += 1
                speed += 2 # Increase speed/difficulty
                print(f"Level Up! Current Speed: {speed}")

        clock.tick(speed)

    pygame.quit()
    quit()

game_loop()
