import pygame
from ball import Ball
pygame.init()
width = 1400
height = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball game bro")
clock = pygame.time.Clock()

my_ball = Ball(width / 2, height / 2, 25, 20)

done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
    key = pygame.key.get_pressed()

    my_ball.move(key, width, height)
    screen.fill((255, 255, 255))

    my_ball.draw(screen)
    pygame.display.flip()
    clock.tick(60)
