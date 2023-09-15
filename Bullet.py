import pygame
import math
from keys import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load("images/bullet1.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 1)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.angle = angle
        self.bullet_speed = BULLET_SPEED
        self.x_bullet_speed = math.cos(self.angle * (2*math.pi/360)) * self.bullet_speed
        self.y_bullet_speed = math.sin(self.angle * (2*math.pi/360)) * self.bullet_speed
        self.bullet_allowed_time = BULLET_TIME
        self.start_time = pygame.time.get_ticks()


    
    def bullet_travel(self):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.x += self.x_bullet_speed
        self.y += self.y_bullet_speed

        if pygame.time.get_ticks() - self.start_time > self.bullet_allowed_time:
            self.kill()

    def update(self):
        self.bullet_travel()