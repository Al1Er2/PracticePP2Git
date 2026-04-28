import pygame
import random
import sys
from pygame.locals import *
from persistence import load_settings, save_settings, add_score
from ui import Button, draw_text, draw_leaderboard

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (230, 40, 40)
BLUE = (40, 90, 230)
GREEN = (40, 200, 80)
YELLOW = (240, 220, 40)
ORANGE = (255, 150, 40)
PURPLE = (160, 70, 220)
GRAY = (160, 160, 160)
DARK_GRAY = (70, 70, 70)
PINK = (255, 170, 210)
CYAN = (40, 220, 220)

CAR_COLORS = {
    "blue": BLUE,
    "red": RED,
    "green": GREEN,
    "pink": PINK
}

DIFFICULTY = {
    "easy": {"speed": 2.5, "enemy_count": 1, "obstacle_count": 1},
    "normal": {"speed": 3.5, "enemy_count": 2, "obstacle_count": 1},
    "hard": {"speed": 4.5, "enemy_count": 3, "obstacle_count": 2}
}

class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, 520)
        self.speed = 6

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)

        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(self.speed, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-600, -80))

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.reset()

    def reset(self):
        self.weight = random.choice([1, 3, 5])
        self.image = pygame.Surface((22, 22))

        if self.weight == 1:
            self.image.fill(YELLOW)
        elif self.weight == 3:
            self.image.fill(ORANGE)
        else:
            self.image.fill(PURPLE)

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-500, -50))

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((45, 35))
        self.image.fill(DARK_GRAY)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-700, -100))

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

class OilSpill(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((55, 25))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-800, -150))

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.spawn_time = pygame.time.get_ticks()
        self.type = random.choice(["nitro", "shield", "repair"])

        self.image = pygame.Surface((28, 28))

        if self.type == "nitro":
            self.image.fill(GREEN)
        elif self.type == "shield":
            self.image.fill(CYAN)
        else:
            self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-700, -100))

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

        if pygame.time.get_ticks() - self.spawn_time > 120000:
            self.kill()

class NitroStrip(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((90, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(80, SCREEN_WIDTH - 80), random.randint(-900, -250))

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("TSIS3 Racer")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 38)
        self.small_font = pygame.font.SysFont("Verdana", 18)
        self.tiny_font = pygame.font.SysFont("Verdana", 14)

        self.settings = load_settings()
        self.state = "menu"
        self.username = ""
        self.running = True

        self.play_button = Button(100, 180, 200, 45, "Play")
        self.leaderboard_button = Button(100, 245, 200, 45, "Leaderboard")
        self.settings_button = Button(100, 310, 200, 45, "Settings")
        self.quit_button = Button(100, 375, 200, 45, "Quit")
        self.back_button = Button(100, 520, 200, 45, "Back")
        self.retry_button = Button(100, 360, 200, 45, "Retry")
        self.menu_button = Button(100, 430, 200, 45, "Main Menu")

        self.reset_game()

    def reset_game(self):
        difficulty = DIFFICULTY[self.settings["difficulty"]]

        self.base_speed = difficulty["speed"]
        self.speed = self.base_speed

        self.score = 0
        self.coins = 0
        self.distance = 0
        self.finish_distance = 2000

        self.active_power = None
        self.power_start = 0
        self.shield = False
        self.repairs = 0
        self.saved_score = False

        color = CAR_COLORS[self.settings["car_color"]]
        self.player = Player(color)

        self.enemies = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.oils = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.strips = pygame.sprite.Group()

        for _ in range(difficulty["enemy_count"]):
            self.enemies.add(Enemy(self.speed))

        for _ in range(2):
            self.coins_group.add(Coin(self.speed))

        for _ in range(difficulty["obstacle_count"]):
            self.obstacles.add(Obstacle(self.speed))

        self.oils.add(OilSpill(self.speed))
        self.strips.add(NitroStrip(self.speed))

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.enemies)
        self.all_sprites.add(self.coins_group)
        self.all_sprites.add(self.obstacles)
        self.all_sprites.add(self.oils)
        self.all_sprites.add(self.strips)

        self.POWERUP_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.POWERUP_EVENT, 5000)

    def update_speed_for_all(self):
        for group in [self.enemies, self.coins_group, self.obstacles, self.oils, self.powerups, self.strips]:
            for sprite in group:
                sprite.speed = self.speed

    def draw_road(self):
        self.screen.fill((50, 50, 50))

        pygame.draw.rect(self.screen, WHITE, (40, 0, 5, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, WHITE, (355, 0, 5, SCREEN_HEIGHT))

        for y in range(0, SCREEN_HEIGHT, 80):
            pygame.draw.rect(self.screen, WHITE, (195, y, 10, 40))

    def calculate_score(self):
        return int(self.coins * 10 + self.distance + self.score * 5 + self.repairs * 25)

    def end_game(self):
        if not self.saved_score:
            final_score = self.calculate_score()
            name = self.username if self.username else "Player"
            add_score(name, final_score, self.distance, self.coins)
            self.saved_score = True

        self.state = "game_over"

    def handle_collision(self, obstacle=None):
        if self.shield:
            self.shield = False
            self.active_power = None

            if obstacle:
                obstacle.kill()

            return

        if self.repairs > 0:
            self.repairs -= 1

            if obstacle:
                obstacle.kill()

            return

        self.end_game()

    def game_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            if event.type == self.POWERUP_EVENT and self.state == "game":
                if len(self.powerups) < 1:
                    power = PowerUp(self.speed)
                    self.powerups.add(power)
                    self.all_sprites.add(power)

            if self.state == "name_input":
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if self.username.strip() == "":
                            self.username = "Player"
                        self.reset_game()
                        self.state = "game"

                    elif event.key == K_BACKSPACE:
                        self.username = self.username[:-1]

                    else:
                        if len(self.username) < 12:
                            self.username += event.unicode

            elif self.state == "menu":
                if self.play_button.clicked(event):
                    self.username = ""
                    self.state = "name_input"

                if self.leaderboard_button.clicked(event):
                    self.state = "leaderboard"

                if self.settings_button.clicked(event):
                    self.state = "settings"

                if self.quit_button.clicked(event):
                    self.running = False

            elif self.state == "leaderboard":
                if self.back_button.clicked(event):
                    self.state = "menu"

            elif self.state == "settings":
                if event.type == KEYDOWN:
                    if event.key == K_s:
                        self.settings["sound"] = not self.settings["sound"]
                        save_settings(self.settings)

                    if event.key == K_c:
                        colors = list(CAR_COLORS.keys())
                        current = colors.index(self.settings["car_color"])
                        self.settings["car_color"] = colors[(current + 1) % len(colors)]
                        save_settings(self.settings)

                    if event.key == K_d:
                        difficulties = list(DIFFICULTY.keys())
                        current = difficulties.index(self.settings["difficulty"])
                        self.settings["difficulty"] = difficulties[(current + 1) % len(difficulties)]
                        save_settings(self.settings)

                if self.back_button.clicked(event):
                    self.state = "menu"

            elif self.state == "game_over":
                if self.retry_button.clicked(event):
                    self.username = self.username if self.username else "Player"
                    self.reset_game()
                    self.state = "game"

                if self.menu_button.clicked(event):
                    self.state = "menu"

    def update_game(self):
        self.distance += self.speed * 0.08
        self.score = int(self.distance // 50)

        if self.settings["difficulty"] == "easy":
            self.speed = self.base_speed + self.distance / 2000
        elif self.settings["difficulty"] == "normal":
            self.speed = self.base_speed + self.distance / 1500
        else:
            self.speed = self.base_speed + self.distance / 1000

        if self.active_power == "nitro":
            self.speed = self.base_speed + 5

        self.update_speed_for_all()

        self.player.move()

        for group in [self.enemies, self.coins_group, self.obstacles, self.oils, self.powerups, self.strips]:
            for sprite in group:
                sprite.move()

        for coin in pygame.sprite.spritecollide(self.player, self.coins_group, False):
            self.coins += coin.weight
            coin.reset()

        power = pygame.sprite.spritecollideany(self.player, self.powerups)

        if power:
            if power.type == "nitro":
                self.active_power = "nitro"
                self.power_start = pygame.time.get_ticks()

            elif power.type == "shield":
                self.active_power = "shield"
                self.shield = True

            elif power.type == "repair":
                self.repairs += 1
                self.active_power = None

            power.kill()

        if pygame.sprite.spritecollideany(self.player, self.strips):
            self.active_power = "nitro"
            self.power_start = pygame.time.get_ticks()

        if self.active_power == "nitro":
            if pygame.time.get_ticks() - self.power_start > 4000:
                self.active_power = None

        enemy_hit = pygame.sprite.spritecollideany(self.player, self.enemies)
        if enemy_hit:
            self.handle_collision(enemy_hit)

        obstacle_hit = pygame.sprite.spritecollideany(self.player, self.obstacles)
        if obstacle_hit:
            self.handle_collision(obstacle_hit)

        oil = pygame.sprite.spritecollideany(self.player, self.oils)
        if oil:
            self.player.speed = 3
        else:
            self.player.speed = 6

        if self.distance >= self.finish_distance:
            self.end_game()

    def draw_game(self):
        self.draw_road()

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect)

        score_text = self.tiny_font.render(f"Score: {self.calculate_score()}", True, WHITE)
        coin_text = self.tiny_font.render(f"Coins: {self.coins}", True, WHITE)
        dist_text = self.tiny_font.render(f"Distance: {int(self.distance)}/{self.finish_distance}", True, WHITE)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(coin_text, (10, 30))
        self.screen.blit(dist_text, (10, 50))

        if self.active_power:
            power_text = self.tiny_font.render(f"Power: {self.active_power}", True, WHITE)
            self.screen.blit(power_text, (250, 10))

        if self.shield:
            shield_text = self.tiny_font.render("Shield: ON", True, CYAN)
            self.screen.blit(shield_text, (250, 30))

        repair_text = self.tiny_font.render(f"Repairs: {self.repairs}", True, WHITE)
        self.screen.blit(repair_text, (250, 50))

    def draw_menu(self):
        self.screen.fill(WHITE)
        draw_text(self.screen, "TSIS3 Racer", self.font, BLACK, 70, 80)

        self.play_button.draw(self.screen, self.small_font)
        self.leaderboard_button.draw(self.screen, self.small_font)
        self.settings_button.draw(self.screen, self.small_font)
        self.quit_button.draw(self.screen, self.small_font)

    def draw_name_input(self):
        self.screen.fill(WHITE)
        draw_text(self.screen, "Enter Name", self.font, BLACK, 80, 160)
        draw_text(self.screen, self.username + "|", self.small_font, BLACK, 120, 260)
        draw_text(self.screen, "Press ENTER to start", self.tiny_font, BLACK, 110, 330)

    def draw_settings(self):
        self.screen.fill(WHITE)
        draw_text(self.screen, "Settings", self.font, BLACK, 110, 60)

        draw_text(self.screen, f"S - Sound: {self.settings['sound']}", self.small_font, BLACK, 60, 160)
        draw_text(self.screen, f"C - Car Color: {self.settings['car_color']}", self.small_font, BLACK, 60, 210)
        draw_text(self.screen, f"D - Difficulty: {self.settings['difficulty']}", self.small_font, BLACK, 60, 260)

        draw_text(self.screen, "Press S, C, or D to change", self.tiny_font, BLACK, 85, 330)

        self.back_button.draw(self.screen, self.small_font)

    def draw_game_over(self):
        self.screen.fill(PINK)

        draw_text(self.screen, "Game Over", self.font, BLACK, 75, 90)
        draw_text(self.screen, f"Score: {self.calculate_score()}", self.small_font, BLACK, 105, 180)
        draw_text(self.screen, f"Distance: {int(self.distance)}", self.small_font, BLACK, 105, 220)
        draw_text(self.screen, f"Coins: {self.coins}", self.small_font, BLACK, 105, 260)
        draw_text(self.screen, f"Repairs left: {self.repairs}", self.small_font, BLACK, 105, 300)

        self.retry_button.draw(self.screen, self.small_font)
        self.menu_button.draw(self.screen, self.small_font)

    def run(self):
        while self.running:
            self.game_events()

            if self.state == "menu":
                self.draw_menu()

            elif self.state == "name_input":
                self.draw_name_input()

            elif self.state == "settings":
                self.draw_settings()

            elif self.state == "leaderboard":
                draw_leaderboard(self.screen, self.font, self.tiny_font)
                self.back_button.draw(self.screen, self.small_font)

            elif self.state == "game":
                self.update_game()
                self.draw_game()

            elif self.state == "game_over":
                self.draw_game_over()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()