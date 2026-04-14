import pygame
import datetime
import os

class MickeyClock:
    def __init__(self, base_path):
        self.clock_img = pygame.image.load(os.path.join(base_path, 'clock.png')).convert_alpha()
        self.mickey = pygame.image.load(os.path.join(base_path, 'mUmrP.png')).convert_alpha()
        self.hand_l = pygame.image.load(os.path.join(base_path, 'hand_left.png')).convert_alpha()
        self.hand_r = pygame.image.load(os.path.join(base_path, 'hand_right.png')).convert_alpha()

        self.clock_img = pygame.transform.scale(self.clock_img, (800, 600))
        self.mickey = pygame.transform.scale(self.mickey, (350, 350))

        self.hand_l_base = pygame.transform.scale(self.hand_l, (80, 80))     
        self.hand_r_base = pygame.transform.scale(self.hand_r, (100, 100))   

        self.center = (600, 340)

    def get_angles(self):
        now = datetime.datetime.now()
        m = now.minute
        s = now.second

        seconds_angle = -(s * 6)
        minutes_angle = -(m * 6 + s * 0.1)

        return seconds_angle, minutes_angle

    def draw(self, screen):
   
        clock_rect = self.clock_img.get_rect(center=self.center)
        screen.blit(self.clock_img, clock_rect)

       
        mic_rect = self.mickey.get_rect(center=(600, 320))
        screen.blit(self.mickey, mic_rect)

      
        seconds_angle, minutes_angle = self.get_angles()

        
        rotated_seconds = pygame.transform.rotate(self.hand_l_base, seconds_angle)
        rotated_minutes = pygame.transform.rotate(self.hand_r_base, minutes_angle)

        
        seconds_rect = rotated_seconds.get_rect(center=self.center)
        minutes_rect = rotated_minutes.get_rect(center=self.center)

        
        screen.blit(rotated_minutes, minutes_rect)   # правая (минуты)
        screen.blit(rotated_seconds, seconds_rect)   # левая (секунды)
