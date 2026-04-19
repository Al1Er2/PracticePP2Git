import pygame
import os
pygame.mixer.init()
class Player:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        self.current_track = 0
        self.playlist = self.load_music()
        self.isplay = False
        self.track_duration = 1

    def load_music(self):
        files = []
        for file in os.listdir(self.music_folder):
            full_path = os.path.join(self.music_folder, file)
            files.append(full_path)
        return files

    def update_duration(self):
        sound = pygame.mixer.Sound(self.playlist[self.current_track])
        self.track_duration = int(sound.get_length())

    def play(self):
        pygame.mixer.music.load(self.playlist[self.current_track])
        pygame.mixer.music.play(0)
        self.isplay = True
        self.update_duration()

    def stop(self):
        pygame.mixer.music.stop()
        self.isplay = False
    
    def pause(self):
        pygame.mixer.music.pause()
        self.isplay = False

    def unpause(self):
        pygame.mixer.music.unpause()
        self.isplay = True

    def next_track(self):
        pygame.mixer.music.stop()
        self.current_track = (self.current_track + 1) % len(self.playlist)
        pygame.mixer.music.load(self.playlist[self.current_track])
        pygame.mixer.music.play(0)
        self.isplay = True
        self.update_duration()

    def previous_track(self):
        pygame.mixer.music.stop()
        self.current_track = (self.current_track - 1) % len(self.playlist)
        pygame.mixer.music.load(self.playlist[self.current_track])
        pygame.mixer.music.play(0)
        self.isplay = True
        self.update_duration()
    
    def get_current_track_name(self):
        return os.path.basename(self.playlist[self.current_track])
    
    def get_info(self):
        current = int(pygame.mixer.music.get_pos() / 1000)
        if current < 0:
            current = 0
        return current, self.track_duration
