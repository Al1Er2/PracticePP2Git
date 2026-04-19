import pygame

class Ball:
    def __init__(self, x, y, radius, step):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = ((0, 0, 255))
        self.step = step

    def move(self, keys, screen_width, screen_height):
        if keys[pygame.K_UP] and self.y - self.step >= self.radius:
            self.y -= self.step
        if keys[pygame.K_DOWN] and self.y + self.step <= screen_height - self.radius:
            self.y += self.step
        if keys[pygame.K_RIGHT] and self.x + self.step <= screen_width - self.radius:
            self.x += self.step
        if keys[pygame.K_LEFT] and self.x - self.step >= self.radius:
            self.x -= self.step

    def draw(self, surface):
        pygame.draw.circle(surface, self.colour, (self.x, self.y), self.radius)
