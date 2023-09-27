import pygame
import math
from keys import *


class Beam(pygame.sprite.Sprite):
    def __init__(self, beam_image, pivot, angle, duration, offset, target_group):
        super().__init__()
        self.angle = angle
        self.pivot = pivot
        self.start_image = beam_image
        self.pre_rotate_rect = self.start_image.get_rect()
        self.image = pygame.transform.rotozoom(self.start_image, -self.angle, 1)
        self.rotated_offset = offset.rotate(self.angle)
        self.rect = self.image.get_rect(center = pivot + self.rotated_offset)
        self.ability_duration = duration
        self.start_time = pygame.time.get_ticks()
        self.target_group = target_group

    
    def beam_travel(self):
        alpha = (int)((pygame.time.get_ticks() - self.start_time)/self.ability_duration*(255))
        self.image.set_alpha(255 - alpha)
        if pygame.time.get_ticks() - self.start_time > self.ability_duration:
            self.kill()

    def beam_collision(self):
        collisions = pygame.sprite.spritecollide(self.rect, self.target_group, False, False)

        for collision in collisions:
            collision.hp -= 10

    def update(self):
        self.beam_collision()
        self.beam_travel()