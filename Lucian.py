import pygame
import math
from Bullet import *
from keys import *
from Player import *
from Beam import *

class Lucian(Player):
    def __init__(self, screen, ally_bullet_group, sprites_group, enemy_group):
        # Character specific image.
        self.char_image = pygame.transform.scale(pygame.image.load("images/lucian.jpg").convert_alpha(),(PLAYER_WIDTH, PLAYER_HEIGHT))

        # Ability Assets.
        self.ability_ult_image = pygame.transform.scale(pygame.image.load("images/lucult.png").convert_alpha(),(100, 100))
        self.ability_ult_image_grey = pygame.transform.scale(pygame.image.load("images/lucult_grey.png").convert_alpha(),(100, 100))
        self.ability_1_image = pygame.transform.scale(pygame.image.load("images/lucq_icon.png").convert_alpha(),(100, 100))
        self.ability_1_image_grey = pygame.transform.scale(pygame.image.load("images/lucq_grey.png").convert_alpha(),(100, 100))
        self.ability_1_animation = pygame.image.load("images/lucq_1.png").convert_alpha()

        # Audio related assets.
        self.ability_1_sound = pygame.mixer.Sound("audio/lucqsound.mp3") 
        self.ability_1_sound.set_volume(2)

        self.ability_ult_sound = pygame.mixer.Sound("audio/lucultsound.mp3") 
        self.ability_ult_sound.set_volume(2)


        # Bullet/Basic firing related variables.
        self.bullet_speed = 50
        self.bullet_allowed_time = 200
        self.bullet_group = ally_bullet_group
        self.enemy_group = enemy_group

        # Ult Ability related variables.
        self.ability_ult_cd = 0
        self.ability_ult_duration = 0
        self.ability_ult_active = False
        self.gun_offset2 = pygame.math.Vector2(OFFSET_X + 10, OFFSET_Y - 10)
        self.to_rotate = True

        # Ability 1 related variables
        self.ability_1_cd = 0
        self.ability_1_active = True
        self.ability_1_duration = 0
        self.can_move = True
        self.ability_1_active = True
        self.ability_1_offset = pygame.math.Vector2(35, 0)

        # Player stats (should be overridden for each character)
        self.hp = 1200
        self.attack_damage = 70
        self.ability_power = 0
        self.armor = 30
        self.magic_resist = 30
        self.cooldown_reduction = 0
        self.crit_chance = 0

        super().__init__(screen, self.bullet_group, sprites_group, self.char_image, self.bullet_speed, self.bullet_allowed_time, self.enemy_group, 
                         self.hp, self.attack_damage, self.ability_power, self.armor, self.magic_resist, self.cooldown_reduction, self.crit_chance)


    def ability_1_cd_timer(self):
        if self.ability_1_cd >= (150*(1-(self.cooldown_reduction/100))):
            self.ability_1_cd = 0
        elif self.ability_1_cd > 0:
            self.ability_1_cd += 1

    def ability_1_active_timer(self):
        if self.ability_1_duration >= AB_1_ACTIVE:
            self.ability_1_active = False
            self.ability_1_duration = 0
            if self.ability_ult_active == False:
                self.to_rotate = True
            self.can_move = True
        elif self.ability_1_duration > 0:
            self.ability_1_duration += 1
            self.beam.beam_collision(self.beam)


    def ability_ult_cd_timer(self):
        if self.ability_ult_cd >= (500*(1-(self.cooldown_reduction/100))):
            self.ability_ult_cd = 0
        elif self.ability_ult_cd > 0:
            self.ability_ult_cd += 1

    def ability_ult_active_timer(self):
        if self.ability_ult_duration >= 125:
            self.ability_ult_active = False
            self.ability_ult_duration = 0
            self.to_rotate = True
        elif self.ability_ult_duration > 0:
            self.ability_ult_duration += 1

    def ability_inputs(self):
        self.ability_ult_cd_timer()
        self.ability_1_cd_timer()
        input = pygame.key.get_pressed()    # Retrieves the key presses.

        # If ult is not on cooldown and the r key is pressed, fire a large amount of bullets at a fast rate.
        if input[pygame.K_r] and self.ability_ult_cd == 0:
            pygame.mixer.Sound.play(self.ability_ult_sound)
            self.ability_ult_active = True
            self.to_rotate = False
            self.ability_ult_cd = 1
            self.ability_ult_duration = 1
        elif input[pygame.K_e] and self.ability_1_cd == 0:
            pygame.mixer.Sound.play(self.ability_1_sound)
            self.ability_1_active = True
            self.to_rotate = False
            self.can_move = False
            self.ability_1_cd = 1
            self.ability_1_duration = 1
            self.ability_1_fire()

    def ability_1_fire(self):
        self.beam = Beam(self.ability_1_animation, self.position, self.angle, 500, pygame.math.Vector2(190, 0), self.enemy_group)
        self.sprites_group.add(self.beam)
        

    def ability_ult_firing(self):
        if self.ability_ult_duration % 2 == 0 and self.ability_ult_active == True:
            start_point = self.position + self.gun_offset.rotate(self.angle)
            self.bullet = Bullet(start_point.x, start_point.y, self.angle, self.bullet_speed, self.bullet_allowed_time, self.attack_damage)
            self.bullet_group.add(self.bullet)
            self.sprites_group.add(self.bullet)

        elif self.ability_ult_duration % 2 == 1 and self.ability_ult_active == True:
            start_point2 = self.position + self.gun_offset2.rotate(self.angle)
            self.bullet2 = Bullet(start_point2.x, start_point2.y, self.angle, self.bullet_speed, self.bullet_allowed_time, self.attack_damage)
            self.bullet_group.add(self.bullet2)
            self.sprites_group.add(self.bullet2)

    def ability_ult_update(self):
        self.ability_inputs()
        self.ability_ult_active_timer()
        self.ability_ult_firing()
        self.ability_1_active_timer()

    def update(self):
        if self.can_move:
            self.register_player_inputs()
        self.ability_ult_update()
        self.hitbox.center = self.position
        self.rect.center = self.hitbox.center
        if self.to_rotate == True:
            self.player_rotation()
        if self.shoot_cd > 0:
            self.shoot_cd -= 1
        if self.hp <= 0:
            self.kill()