import pygame
import math
from keys import *
from Bullet import *



class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_group, all_sprites_group, pos, player, player_group, enemy_bullet_group):
        super().__init__(enemy_group, all_sprites_group)
        self.image = pygame.image.load("images/cannon.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.25)

        self.all_sprites_group = all_sprites_group
        self.player_group = player_group
        self.enemy_bullet_group = enemy_bullet_group

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.enemy_direction = pygame.math.Vector2()
        self.enemy_velocity = pygame.math.Vector2()
        self.enemy_speed = 2

        self.position = pygame.math.Vector2(pos)
        self.player = player

        self.player_pos = pygame.math.Vector2(self.player.hitbox.center)
        self.hp = 100

        self.shoot_cd = ENEMY_SHOOT_CD


    def aggro(self):
        distance = (self.player_pos - self.rect.center).magnitude()

        if distance > 200:
            self.enemy_direction = (self.player_pos - self.rect.center).normalize()
        else:
            self.enemy_direction = pygame.math.Vector2()

        self.enemy_velocity = self.enemy_direction * self.enemy_speed
        self.position += self.enemy_velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def attack(self):
        if self.shoot_cd == 0:
            self.shoot_cd = ENEMY_SHOOT_CD
            start_point = self.position
            dx = self.player_pos.x - self.rect.centerx
            dy = self.player_pos.y - self.rect.centery
            rads = math.atan2(dy,dx)
            degs = math.degrees(rads)

            self.bullet = Bullet(start_point.x, start_point.y, degs, ENEMY_BULLET_SPEED, ENEMY_BULLET_TIME, self.enemy_bullet_group, self.player_group)
            self.enemy_bullet_group.add(self.bullet)
            self.all_sprites_group.add(self.bullet)

    def update(self):
        self.player_pos = pygame.math.Vector2(self.player.hitbox.center)
        self.attack()
        self.aggro()
        if self.hp <= 0:
            self.kill()
        if self.shoot_cd > 0:
            self.shoot_cd -= 1
