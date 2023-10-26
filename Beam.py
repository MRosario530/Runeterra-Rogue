import pygame
from keys import *

class Beam(pygame.sprite.Sprite):
    def __init__(self, beam_image, pivot, angle, duration, offset, target_group, damage):
        super().__init__()
        self.damage = damage    # Damage value
        self.angle = angle      # Following values are related to sprites/images and the angles
        self.pivot = pivot
        self.start_image = beam_image
        self.pre_rotate_rect = self.start_image.get_rect()
        self.image = pygame.transform.rotozoom(self.start_image, -self.angle, 1)
        self.rotated_offset = offset.rotate(self.angle)
        self.rect = self.image.get_rect(center = pivot + self.rotated_offset)
        self.ability_duration = duration    # Length of time the beam should last
        self.start_time = pygame.time.get_ticks() # Starting point for the timer for the beam
        self.target_group = target_group    # Which type of sprite the ability affects (ally or enemy)
    
    def beam_travel(self):  # Function that updates the beam location and display.
        alpha = (int)((pygame.time.get_ticks() - self.start_time)/self.ability_duration*(255)) # Values that enable the beam to fade in/out.
        self.image.set_alpha(255 - alpha)
        if pygame.time.get_ticks() - self.start_time > self.ability_duration: # End the beam after the timer ends.
            self.kill()

    def beam_collision(self, beam): # Detects collision between the beam and target group (ally or enemy). (SET TO BE REMOVED AND COMBINED WITH COLLISION CLASS)
        collisions = pygame.sprite.spritecollide(beam, self.target_group, False)

        for collision in collisions:
            collision.currenthp -= self.damage

    def update(self):
        self.beam_travel()