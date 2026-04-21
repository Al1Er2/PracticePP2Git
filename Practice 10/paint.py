import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Paint Plus")
    clock = pygame.time.Clock()
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    screen.fill(WHITE)
    
    # State variables
    drawing = False
    last_pos = None
    start_pos = None
    current_tool = 'brush' # Options: brush, eraser, rect, circle
    current_color = BLACK
    brush_size = 5

    # Surface to store the drawing (so shapes don't disappear)
    canvas = screen.copy()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # Tool Selection via Keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: current_tool = 'brush'
                if event.key == pygame.K_e: current_tool = 'eraser'
                if event.key == pygame.K_r: current_tool = 'rect'
                if event.key == pygame.K_c: current_tool = 'circle'
                # Color Selection
                if event.key == pygame.K_1: current_color = BLACK
                if event.key == pygame.K_2: current_color = RED
                if event.key == pygame.K_3: current_color = GREEN
                if event.key == pygame.K_4: current_color = BLUE

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                # Finalize the shape onto the canvas
                canvas.blit(screen, (0, 0))

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    mouse_pos = event.pos
                    
                    if current_tool == 'brush':
                        pygame.draw.line(canvas, current_color, last_pos, mouse_pos, brush_size)
                        last_pos = mouse_pos
                    elif current_tool == 'eraser':
                        pygame.draw.line(canvas, WHITE, last_pos, mouse_pos, 20)
                        last_pos = mouse_pos

        # --- DRAWING PHASE ---
        screen.blit(canvas, (0, 0)) # Redraw the permanent canvas

        if drawing:
            mouse_pos = pygame.mouse.get_pos()
            if current_tool == 'rect':
                # Calculate width and height relative to where we first clicked
                width = mouse_pos[0] - start_pos[0]
                height = mouse_pos[1] - start_pos[1]
                rect = pygame.Rect(start_pos, (width, height))
                rect.normalize() # Handles drawing backwards
                pygame.draw.rect(screen, current_color, rect, 2)
                
            elif current_tool == 'circle':
                # Calculate radius using distance formula
                radius = int(((mouse_pos[0] - start_pos[0])**2 + (mouse_pos[1] - start_pos[1])**2)**0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius, 2)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
