import pygame
from persistence import load_leaderboard

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (80, 80, 80)

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, GRAY, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)

        text_img = font.render(self.text, True, BLACK)
        text_rect = text_img.get_rect(center=self.rect.center)
        screen.blit(text_img, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

def draw_text(screen, text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_leaderboard(screen, font, small_font):
    screen.fill(WHITE)
    draw_text(screen, "Leaderboard", font, BLACK, 80, 40)

    data = load_leaderboard()

    y = 120
    if not data:
        draw_text(screen, "No scores yet", small_font, BLACK, 120, y)
    else:
        for i, item in enumerate(data):
            line = f"{i + 1}. {item['name']} | Score: {item['score']} | Dist: {item['distance']}"
            draw_text(screen, line, small_font, BLACK, 20, y)
            y += 35