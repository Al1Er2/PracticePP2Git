import pygame
import math

def flood_fill(surface, position, fill_color):
    """Fills an enclosed area using a stack-based DFS."""
    fill_mapped = surface.map_rgb(fill_color)
    target_mapped = surface.get_at_mapped(position)
    
    if target_mapped == fill_mapped:
        return

    w, h = surface.get_size()
    pa = pygame.PixelArray(surface)
    stack = [position]
    
    while stack:
        x, y = stack.pop()
        if 0 <= x < w and 0 <= y < h:
            if pa[x, y] == target_mapped:
                pa[x, y] = fill_mapped
                stack.append((x + 1, y))
                stack.append((x - 1, y))
                stack.append((x, y + 1))
                stack.append((x, y - 1))
    
    pa.close()

def draw_shape(surface, tool, color, start_pos, mouse_pos, brush_size):
    """Handles the geometric logic for various shape tools."""
    dx = mouse_pos[0] - start_pos[0]
    dy = mouse_pos[1] - start_pos[1]

    if tool == 'line':
        pygame.draw.line(surface, color, start_pos, mouse_pos, brush_size)

    elif tool == 'rect':
        rect = pygame.Rect(start_pos, (dx, dy))
        rect.normalize()
        pygame.draw.rect(surface, color, rect, brush_size)
        
    elif tool == 'circle':
        radius = int((dx**2 + dy**2)**0.5)
        pygame.draw.circle(surface, color, start_pos, radius, brush_size)

    elif tool == 'square':
        side = max(abs(dx), abs(dy))
        s_x = start_pos[0] if dx > 0 else start_pos[0] - side
        s_y = start_pos[1] if dy > 0 else start_pos[1] - side
        pygame.draw.rect(surface, color, (s_x, s_y, side, side), brush_size)

    elif tool == 'right_tri':
        points = [start_pos, (start_pos[0], mouse_pos[1]), mouse_pos]
        pygame.draw.polygon(surface, color, points, brush_size)

    elif tool == 'eq_tri':
        side = dx 
        height = (math.sqrt(3) / 2) * side
        points = [
            (start_pos[0], start_pos[1]), 
            (start_pos[0] - side/2, start_pos[1] + height), 
            (start_pos[0] + side/2, start_pos[1] + height)  
        ]
        pygame.draw.polygon(surface, color, points, brush_size)

    elif tool == 'rhombus':
        points = [
            (start_pos[0], start_pos[1] + dy), 
            (start_pos[0] + dx, start_pos[1]), 
            (start_pos[0], start_pos[1] - dy), 
            (start_pos[0] - dx, start_pos[1])  
        ]
        pygame.draw.polygon(surface, color, points, brush_size)