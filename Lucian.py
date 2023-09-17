import pygame
import math
from Bullet import *
from keys import *
from Player import *

class Lucian(Player):
    def __init__(self, screen, bullet_sprite_group, sprites_group):
        self.char_image = pygame.transform.scale(pygame.image.load("images/lucian.jpg").convert_alpha(),(PLAYER_WIDTH, PLAYER_HEIGHT))
        self.ability_1_image = pygame.transform.scale(pygame.image.load("images/lucult.png").convert_alpha(),(100, 100))
        self.ability_1_image_grey = pygame.transform.scale(pygame.image.load("images/lucult_grey.png").convert_alpha(),(100, 100))
        self.bullet_speed = 50
        self.bullet_allowed_time = 200
        self.ability_1_cd = 0
        self.ability_1_shoot_cd = 0
        self.ability_1_active = False
        self.gun_offset2 = pygame.math.Vector2(OFFSET_X + 10, OFFSET_Y - 10)
        self.to_rotate = True
        super().__init__(screen, bullet_sprite_group, sprites_group, self.char_image, self.bullet_speed, self.bullet_allowed_time)

    def ability_1_cd_timer(self):
        if self.ability_1_cd >= 300:
            self.ability_1_cd = 0
        elif self.ability_1_cd > 0:
            self.ability_1_cd += 1

    def ability_1_active_timer(self):
        if self.ability_1_shoot_cd >= 40:
            self.ability_1_active = False
            self.ability_1_shoot_cd = 0
            self.to_rotate = True
        elif self.ability_1_shoot_cd > 0:
            self.ability_1_shoot_cd += 1

    def ability_1_input(self):
        self.ability_1_cd_timer()
        input = pygame.key.get_pressed()    # Retrieves the key presses.

        # If ability 1 is not on cooldown and the r key is pressed, fire a large amount of bullets at a fast rate.
        if input[pygame.K_r] and self.ability_1_cd == 0:
            self.ability_1_active = True
            self.to_rotate = False
            self.ability_1_cd = 1
            self.ability_1_shoot_cd = 1

    def ability_1_firing(self):
        if self.ability_1_shoot_cd % 2 == 0 and self.ability_1_active == True:
            start_point = self.position + self.gun_offset.rotate(self.angle)
            self.bullet = Bullet(start_point.x, start_point.y, self.angle, self.bullet_speed, self.bullet_allowed_time)
            self.bullet_sprite_group.add(self.bullet)
            self.sprites_group.add(self.bullet)

        elif self.ability_1_shoot_cd % 2 == 1 and self.ability_1_active == True:
            start_point2 = self.position + self.gun_offset2.rotate(self.angle)
            self.bullet2 = Bullet(start_point2.x, start_point2.y, self.angle, self.bullet_speed, self.bullet_allowed_time)
            self.bullet_sprite_group.add(self.bullet2)
            self.sprites_group.add(self.bullet2)

    def ability_1_update(self):
        self.ability_1_input()
        self.ability_1_active_timer()
        self.ability_1_firing()

    def update(self):
        self.register_player_inputs()
        self.ability_1_update()
        self.hitbox.center = self.position
        self.rect.center = self.hitbox.center
        if self.to_rotate == True:
            self.player_rotation()
        if self.shoot_cd > 0:
            self.shoot_cd -= 1