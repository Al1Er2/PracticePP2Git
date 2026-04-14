import pygame
import os
from clock import MickeyClock

pygame.init()

screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Mickey Clock")

WHITE = (255, 255, 255)

base_path = os.path.join(os.path.dirname(__file__), "images")

mickey_clock = MickeyClock(base_path)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # рисуем часы
    mickey_clock.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
