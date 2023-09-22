import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_group, all_sprites_group, pos, player):
        super().__init__(enemy_group, all_sprites_group)
        self.image = pygame.image.load("images/cannon.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.enemy_direction = pygame.math.Vector2()
        self.enemy_velocity = pygame.math.Vector2()
        self.enemy_speed = 5

        self.position = pygame.math.Vector2(pos)
        self.player = player

        self.player_pos = pygame.math.Vector2(self.player.hitbox.center)

    def aggro(self):
        player_pos = pygame.math.Vector2(self.player.hitbox.center)
        print(player_pos)
        enemy_pos = self.rect.center
        distance = (player_pos - enemy_pos).magnitude()

        if distance > 0:
            self.enemy_direction = (player_pos - enemy_pos).normalize()
        else:
            self.enemy_direction = pygame.math.Vector2()

        self.enemy_velocity = self.enemy_direction * self.enemy_speed
        self.position += self.enemy_velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y



    def update(self):
        self.aggro()