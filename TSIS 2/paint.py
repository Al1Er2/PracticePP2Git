import pygame
import datetime
from tools import flood_fill, draw_shape

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Paint Plus - Extended Tools")
    clock = pygame.time.Clock()
    
    # Text Input setup
    pygame.font.init()
    font = pygame.font.SysFont(None, 36)
    
    # Colors
    BLACK, WHITE = (0, 0, 0), (255, 255, 255)
    RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)

    screen.fill(WHITE)
    
    # States
    drawing = False
    last_pos = start_pos = None
    current_tool, current_color, brush_size = 'brush', BLACK, 5
    text_input_mode, text_string, text_pos = False, "", (0, 0)

    canvas = screen.copy()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # --- TEXT INPUT HANDLING ---
            if text_input_mode:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        text_surf = font.render(text_string, True, current_color)
                        canvas.blit(text_surf, text_pos)
                        text_input_mode = False
                    elif event.key == pygame.K_ESCAPE:
                        text_input_mode = False
                    elif event.key == pygame.K_BACKSPACE:
                        text_string = text_string[:-1]
                    else:
                        text_string += event.unicode
                continue 

            # --- KEYBOARD SHORTCUTS ---
            if event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    pygame.image.save(canvas, f"canvas_{timestamp}.png")
                    continue

                # Tool selection
                tools_map = {pygame.K_b:'brush', pygame.K_e:'eraser', pygame.K_r:'rect', 
                             pygame.K_c:'circle', pygame.K_s:'square', pygame.K_t:'right_tri', 
                             pygame.K_i:'eq_tri', pygame.K_h:'rhombus', pygame.K_l:'line', 
                             pygame.K_f:'flood_fill', pygame.K_a:'text'}
                if event.key in tools_map: current_tool = tools_map[event.key]

                # Colors
                colors_map = {pygame.K_1:BLACK, pygame.K_2:RED, pygame.K_3:GREEN, pygame.K_4:BLUE}
                if event.key in colors_map: current_color = colors_map[event.key]
                
                # Brush Sizes
                if event.key == pygame.K_UP: brush_size = min(10, brush_size + 3) if brush_size < 10 else 10
                if event.key == pygame.K_DOWN: brush_size = max(2, brush_size - 3) if brush_size > 2 else 2

            # --- MOUSE INTERACTIONS ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_tool == 'text':
                    text_input_mode, text_string, text_pos = True, "", event.pos
                elif current_tool == 'flood_fill':
                    flood_fill(canvas, event.pos, current_color)
                else:
                    drawing, start_pos, last_pos = True, event.pos, event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    drawing = False
                    canvas.blit(screen, (0, 0)) 

            if event.type == pygame.MOUSEMOTION and drawing:
                if current_tool == 'brush':
                    pygame.draw.line(canvas, current_color, last_pos, event.pos, brush_size)
                    last_pos = event.pos
                elif current_tool == 'eraser':
                    pygame.draw.line(canvas, WHITE, last_pos, event.pos, brush_size * 4)
                    last_pos = event.pos

        # --- DRAWING PHASE ---
        screen.blit(canvas, (0, 0)) 

        if text_input_mode:
            text_surf = font.render(text_string + "|", True, current_color)
            screen.blit(text_surf, text_pos)

        if drawing and current_tool not in ['brush', 'eraser']:
            draw_shape(screen, current_tool, current_color, start_pos, pygame.mouse.get_pos(), brush_size)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()