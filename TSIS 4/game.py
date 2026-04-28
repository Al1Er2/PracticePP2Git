import pygame
import random
import json
import os
from db import save_result, get_personal_best, get_top_scores

pygame.init()

WIDTH = 800
HEIGHT = 600
BLOCK = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
DARK_GRAY = (35, 35, 35)
RED = (220, 50, 50)
DARK_RED = (100, 0, 0)
BLUE = (60, 140, 255)
YELLOW = (255, 220, 70)
PURPLE = (180, 80, 255)
CYAN = (0, 220, 220)
ORANGE = (255, 160, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake Game")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("arial", 22)
font_medium = pygame.font.SysFont("arial", 30)
font_big = pygame.font.SysFont("arial", 48)

SETTINGS_FILE = "settings.json"


def load_settings():
    default = {
        "snake_color": [0, 255, 0],
        "grid": True,
        "sound": False
    }

    if not os.path.exists(SETTINGS_FILE):
        save_settings(default)
        return default

    try:
        with open(SETTINGS_FILE, "r") as file:
            data = json.load(file)
    except:
        save_settings(default)
        return default

    for key in default:
        if key not in data:
            data[key] = default[key]

    save_settings(data)
    return data


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def draw_text(text, font, color, x, y, center=False):
    image = font.render(text, True, color)
    rect = image.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(image, rect)


def draw_button(text, x, y, w, h):
    mouse = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)

    color = GRAY if rect.collidepoint(mouse) else DARK_GRAY

    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    draw_text(text, font_medium, WHITE, x + w // 2, y + h // 2, True)

    return rect


def draw_grid():
    for x in range(0, WIDTH, BLOCK):
        pygame.draw.line(screen, (25, 25, 25), (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, BLOCK):
        pygame.draw.line(screen, (25, 25, 25), (0, y), (WIDTH, y))


def valid_position(pos, snake, obstacles, extra=[]):
    return (
        pos not in snake
        and pos not in obstacles
        and pos not in extra
        and 0 <= pos[0] < WIDTH
        and 0 <= pos[1] < HEIGHT
    )


def random_position(snake, obstacles, extra=[]):
    while True:
        pos = [
            random.randrange(0, WIDTH, BLOCK),
            random.randrange(0, HEIGHT, BLOCK)
        ]

        if valid_position(pos, snake, obstacles, extra):
            return pos


def generate_obstacles(level, snake):
    obstacles = []

    if level < 3:
        return obstacles

    count = min(8 + level * 2, 35)
    head = snake[-1]

    safe_zone = []

    for dx in [-BLOCK, 0, BLOCK]:
        for dy in [-BLOCK, 0, BLOCK]:
            safe_zone.append([head[0] + dx, head[1] + dy])

    while len(obstacles) < count:
        pos = [
            random.randrange(0, WIDTH, BLOCK),
            random.randrange(0, HEIGHT, BLOCK)
        ]

        if pos not in snake and pos not in safe_zone and pos not in obstacles:
            obstacles.append(pos)

    return obstacles


def username_screen():
    username = ""

    while True:
        screen.fill(BLACK)

        draw_text("TSIS4 Snake Game", font_big, YELLOW, WIDTH // 2, 120, True)
        draw_text("Enter username:", font_medium, WHITE, WIDTH // 2, 220, True)

        pygame.draw.rect(screen, DARK_GRAY, (250, 260, 300, 45), border_radius=8)
        pygame.draw.rect(screen, WHITE, (250, 260, 300, 45), 2, border_radius=8)

        draw_text(username, font_medium, WHITE, WIDTH // 2, 282, True)
        draw_text("Press ENTER to continue", font_small, GRAY, WIDTH // 2, 340, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    return username.strip()

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif len(username) < 15 and event.unicode.isprintable():
                    username += event.unicode

        pygame.display.update()
        clock.tick(60)


def main_menu(username):
    while True:
        screen.fill(BLACK)

        draw_text("Main Menu", font_big, YELLOW, WIDTH // 2, 100, True)
        draw_text(f"Player: {username}", font_small, WHITE, WIDTH // 2, 155, True)

        play_btn = draw_button("Play", 300, 220, 200, 50)
        leaderboard_btn = draw_button("Leaderboard", 300, 290, 200, 50)
        settings_btn = draw_button("Settings", 300, 360, 200, 50)
        quit_btn = draw_button("Quit", 300, 430, 200, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_btn.collidepoint(event.pos):
                    return "play"

                elif leaderboard_btn.collidepoint(event.pos):
                    return "leaderboard"

                elif settings_btn.collidepoint(event.pos):
                    return "settings"

                elif quit_btn.collidepoint(event.pos):
                    return "quit"

        pygame.display.update()
        clock.tick(60)


def leaderboard_screen():
    while True:
        screen.fill(BLACK)

        draw_text("Leaderboard - Top 10", font_big, YELLOW, WIDTH // 2, 60, True)

        try:
            scores = get_top_scores()
        except Exception as e:
            scores = []
            draw_text("Database error", font_medium, RED, WIDTH // 2, 130, True)
            draw_text(str(e), font_small, WHITE, WIDTH // 2, 165, True)

        y = 130

        if scores:
            draw_text("Rank   Username          Score   Level   Date", font_small, CYAN, 90, y)
            y += 35

            for i, row in enumerate(scores, start=1):
                username, score, level, played_at = row
                date = played_at.strftime("%Y-%m-%d")
                text = f"{i:<6} {username:<16} {score:<7} {level:<7} {date}"
                draw_text(text, font_small, WHITE, 90, y)
                y += 32
        else:
            draw_text("No scores yet", font_medium, WHITE, WIDTH // 2, 270, True)

        back_btn = draw_button("Back", 300, 520, 200, 45)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.collidepoint(event.pos):
                    return "menu"

        pygame.display.update()
        clock.tick(60)


def settings_screen():
    settings = load_settings()

    colors = [
        [0, 255, 0],
        [255, 0, 120],
        [0, 200, 255],
        [255, 255, 0],
        [180, 80, 255]
    ]

    color_index = 0

    if settings["snake_color"] in colors:
        color_index = colors.index(settings["snake_color"])

    while True:
        screen.fill(BLACK)

        draw_text("Settings", font_big, YELLOW, WIDTH // 2, 80, True)

        draw_text(f"Grid: {'ON' if settings['grid'] else 'OFF'}", font_medium, WHITE, 250, 170)
        draw_text(f"Sound: {'ON' if settings['sound'] else 'OFF'}", font_medium, WHITE, 250, 240)
        draw_text("Snake Color:", font_medium, WHITE, 250, 310)

        pygame.draw.rect(screen, tuple(colors[color_index]), (470, 310, 40, 40))

        grid_btn = draw_button("Toggle Grid", 250, 190, 300, 40)
        sound_btn = draw_button("Toggle Sound", 250, 260, 300, 40)
        color_btn = draw_button("Change Color", 250, 360, 300, 40)
        save_btn = draw_button("Save & Back", 250, 460, 300, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if grid_btn.collidepoint(event.pos):
                    settings["grid"] = not settings["grid"]

                elif sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]

                elif color_btn.collidepoint(event.pos):
                    color_index = (color_index + 1) % len(colors)
                    settings["snake_color"] = colors[color_index]

                elif save_btn.collidepoint(event.pos):
                    save_settings(settings)
                    return "menu"

        pygame.display.update()
        clock.tick(60)


def game_over_screen(username, score, level, best):
    try:
        save_result(username, score, level)
    except Exception as e:
        print("Score save error:", e)

    while True:
        screen.fill(BLACK)

        draw_text("Game Over", font_big, RED, WIDTH // 2, 120, True)
        draw_text(f"Final Score: {score}", font_medium, WHITE, WIDTH // 2, 210, True)
        draw_text(f"Level Reached: {level}", font_medium, WHITE, WIDTH // 2, 255, True)
        draw_text(f"Personal Best: {max(best, score)}", font_medium, YELLOW, WIDTH // 2, 300, True)

        retry_btn = draw_button("Retry", 250, 380, 300, 50)
        menu_btn = draw_button("Main Menu", 250, 450, 300, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if retry_btn.collidepoint(event.pos):
                    return "retry"

                elif menu_btn.collidepoint(event.pos):
                    return "menu"

        pygame.display.update()
        clock.tick(60)


def play_game(username):
    settings = load_settings()
    snake_color = tuple(settings["snake_color"])

    try:
        personal_best = get_personal_best(username)
    except:
        personal_best = 0

    x = WIDTH // 2
    y = HEIGHT // 2

    dx = 0
    dy = 0

    snake = [[x, y]]
    length = 1

    score = 0
    level = 1

    base_speed = 10
    speed = base_speed

    obstacles = []

    food = random_position(snake, obstacles)
    poison = random_position(snake, obstacles, [food])

    special_food = None
    special_food_timer = 0
    special_food_duration = 5000

    powerup = None
    powerup_type = None
    powerup_spawn_time = 0
    powerup_lifetime = 8000

    active_speed_effect = None
    speed_effect_start = 0
    speed_effect_duration = 5000

    shield = False

    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -BLOCK
                    dy = 0

                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = BLOCK
                    dy = 0

                elif event.key == pygame.K_UP and dy == 0:
                    dx = 0
                    dy = -BLOCK

                elif event.key == pygame.K_DOWN and dy == 0:
                    dx = 0
                    dy = BLOCK

        x += dx
        y += dy

        head = [x, y]
        collision = False

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            collision = True

        if head in snake[:-1]:
            collision = True

        if head in obstacles:
            collision = True

        if collision:
            if shield:
                shield = False

                if x < 0:
                    x = 0
                elif x >= WIDTH:
                    x = WIDTH - BLOCK

                if y < 0:
                    y = 0
                elif y >= HEIGHT:
                    y = HEIGHT - BLOCK

                head = [x, y]
            else:
                return game_over_screen(username, score, level, personal_best)

        snake.append(head)

        if len(snake) > length:
            snake.pop(0)

        if head == food:
            score += 1
            length += 1

            food = random_position(
                snake,
                obstacles,
                [poison] + ([special_food] if special_food else []) + ([powerup] if powerup else [])
            )

            if random.randint(1, 4) == 1 and special_food is None:
                special_food = random_position(snake, obstacles, [food, poison])
                special_food_timer = current_time

            if random.randint(1, 4) == 1 and powerup is None:
                powerup = random_position(snake, obstacles, [food, poison])
                powerup_type = random.choice(["speed", "slow", "shield"])
                powerup_spawn_time = current_time

        if head == poison:
            length -= 2
            poison = random_position(snake, obstacles, [food])

            if length <= 1:
                return game_over_screen(username, score, level, personal_best)

            while len(snake) > length:
                snake.pop(0)

        if special_food and head == special_food:
            score += 3
            length += 3
            special_food = None

        if special_food and current_time - special_food_timer > special_food_duration:
            special_food = None

        if powerup and current_time - powerup_spawn_time > powerup_lifetime:
            powerup = None
            powerup_type = None

        if powerup and head == powerup:
            if powerup_type == "speed":
                active_speed_effect = "speed"
                speed_effect_start = current_time

            elif powerup_type == "slow":
                active_speed_effect = "slow"
                speed_effect_start = current_time

            elif powerup_type == "shield":
                shield = True

            powerup = None
            powerup_type = None

        expected_level = score // 3 + 1

        if expected_level > level:
            level = expected_level
            base_speed += 2
            obstacles = generate_obstacles(level, snake)

            food = random_position(snake, obstacles, [poison])
            poison = random_position(snake, obstacles, [food])

        if active_speed_effect:
            if current_time - speed_effect_start <= speed_effect_duration:
                if active_speed_effect == "speed":
                    speed = base_speed + 5
                elif active_speed_effect == "slow":
                    speed = max(5, base_speed - 5)
            else:
                active_speed_effect = None
                speed = base_speed
        else:
            speed = base_speed

        screen.fill(BLACK)

        if settings["grid"]:
            draw_grid()

        pygame.draw.rect(screen, RED, (*food, BLOCK, BLOCK))
        pygame.draw.rect(screen, DARK_RED, (*poison, BLOCK, BLOCK))

        if special_food:
            pygame.draw.rect(screen, YELLOW, (*special_food, BLOCK, BLOCK))

        if powerup:
            if powerup_type == "speed":
                power_color = ORANGE
            elif powerup_type == "slow":
                power_color = CYAN
            else:
                power_color = BLUE

            pygame.draw.rect(screen, power_color, (*powerup, BLOCK, BLOCK))

        for obstacle in obstacles:
            pygame.draw.rect(screen, GRAY, (*obstacle, BLOCK, BLOCK))

        for part in snake:
            pygame.draw.rect(screen, snake_color, (*part, BLOCK, BLOCK))

        draw_text(f"Player: {username}", font_small, WHITE, 10, 10)
        draw_text(f"Score: {score}", font_small, WHITE, 10, 35)
        draw_text(f"Level: {level}", font_small, WHITE, 10, 60)
        draw_text(f"Best: {personal_best}", font_small, YELLOW, 10, 85)

        if shield:
            draw_text("Shield: ON", font_small, BLUE, 650, 10)

        if active_speed_effect == "speed":
            draw_text("Speed Boost", font_small, ORANGE, 650, 40)

        if active_speed_effect == "slow":
            draw_text("Slow Motion", font_small, CYAN, 650, 40)

        pygame.display.update()
        clock.tick(speed)