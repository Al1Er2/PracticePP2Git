import pygame
import os
from player import Player
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Music player")
clock = pygame.time.Clock()
done = False

def draw():
    screen.fill((0, 0, 0))
    
    for i, track_path in enumerate(bro.playlist):
        track_name = os.path.basename(track_path)
        if i == bro.current_track:
            colour = (0, 255, 0)
        else:
            colour = (255, 0, 0)
        text_playlist = font2.render(f"{i + 1}. {track_name}", True, colour)
        screen.blit(text_playlist, (20, 25 + i * 25))

    text = font.render(f"Track: {bro.get_current_track_name()}", True, (255, 255, 255))
    screen.blit(text, (300, 300))

    status = "Playing" if bro.isplay else "Stopped"
    text_2 = font.render(f"Status: {status}", True, (255, 255, 255))
    screen.blit(text_2, (300, 340))

    current, full = bro.get_info()
    progress_text = font.render(f"Time: {current} / {full}", True, (255, 255, 255))
    screen.blit(progress_text, (300, 380))

    bar_x = 300
    bar_y = 430
    bar_width = 400
    pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, 40))
    
    filled_width = (current / full) * bar_width
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, filled_width, 40))

    pygame.display.flip()
font = pygame.font.SysFont("comicsansms", 40)
font2 = pygame.font.SysFont("comicsansms", 25)

bro = Player("music")
while not done:
    #Автоматическое переключение трека, если он закончился
    if bro.isplay and not pygame.mixer.music.get_busy():
        bro.next_track()
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x < 200:
                clicked_index = (y - 25) // 25
                if 0 <= clicked_index < len(bro.playlist):
                    bro.current_track = clicked_index
                    bro.play()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                bro.play()
            if event.key == pygame.K_s:
                bro.stop()
            if event.key == pygame.K_n:
                bro.next_track()
            if event.key == pygame.K_b:
                bro.previous_track()
            if event.key == pygame.K_q:
                done = True
            if event.key == pygame.K_v:
                bro.pause()
            if event.key == pygame.K_u:
                bro.unpause()
    clock.tick(60)
