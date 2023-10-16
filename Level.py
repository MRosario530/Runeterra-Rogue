import pygame
import random
from Enemy import *
from keys import *


class Level(pygame.sprite.Group):
    def __init__(self, enemy_group, all_sprites_group, player, player_group, enemy_bullet_group):
        super().__init__()
        self.enemy_group = enemy_group
        self.all_sprites_group = all_sprites_group
        self.player = player
        self.maximum_enemies = 10
        self.player_group = player_group
        self.enemy_bullet_group = enemy_bullet_group


    def spawn_enemies(self):
        Enemy(self.enemy_group, self.all_sprites_group, (random.randint(0, 4320), random.randint(0, 2280)), self.player, self.player_group, self.enemy_bullet_group)
        

    def update(self, current_time):
        if current_time % 30 == 0:
            self.maximum_enemies += 1
        if current_time % 5 == 0 and len(self.enemy_group.sprites()) < self.maximum_enemies:
            self.spawn_enemies()