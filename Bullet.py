import pygame
import math
from keys import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, bullet_speed, allowed_time, attack_damage):
        super().__init__()
        self.image = pygame.image.load("images/bullet1.png").convert_alpha()    # Image/location related variables.
        self.image = pygame.transform.rotozoom(self.image, 0, 1)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.angle = angle
        self.bullet_speed = bullet_speed    # Variables related to bullet traveling.
        self.x_bullet_speed = math.cos(self.angle * (2*math.pi/360)) * self.bullet_speed
        self.y_bullet_speed = math.sin(self.angle * (2*math.pi/360)) * self.bullet_speed
        self.bullet_duration = allowed_time
        self.start_time = pygame.time.get_ticks()
        self.damage = attack_damage     # Damage of the bullet.
    
    def bullet_travel(self):    # Function that updates the location of the bullet until it times out.
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.x += self.x_bullet_speed
        self.y += self.y_bullet_speed

        if pygame.time.get_ticks() - self.start_time > self.bullet_duration:
            self.kill()

    def update(self):
        self.bullet_travel()
