import pygame
import sys

def main():
    # 1. Setup
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball Game")
    
    # Ball properties
    ball_color = (255, 0, 0)  # Red
    ball_radius = 25
    step = 20
    
    # Starting position (center of screen)
    x, y = WIDTH // 2, HEIGHT // 2

    clock = pygame.time.Clock()

    while True:
        # 2. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Key Press logic
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and y - step >= ball_radius:
                    y -= step
                if event.key == pygame.K_DOWN and y + step <= HEIGHT - ball_radius:
                    y += step
                if event.key == pygame.K_LEFT and x - step >= ball_radius:
                    x -= step
                if event.key == pygame.K_RIGHT and x + step <= WIDTH - ball_radius:
                    x += step

        # 3. Drawing
        screen.fill((255, 255, 255)) # White background
        pygame.draw.circle(screen, ball_color, (x, y), ball_radius)
        
        pygame.display.flip()
        clock.tick(60) # Smooth 60 FPS

if __name__ == "__main__":
    main()
