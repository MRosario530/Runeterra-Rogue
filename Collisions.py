import pygame

class Collisions():
    def __init__(self, ally_bullet_group, enemy_bullet_group, player_group, enemy_group, ally_ability_group):
        super().__init__()
        self.ally_bullet_group = ally_bullet_group  # All sprite groups with potential collisions.
        self.enemy_bullet_group = enemy_bullet_group
        self.player_group = player_group
        self.enemy_group = enemy_group
        self.ally_ability_group = ally_ability_group


    def check_enemy_shots(self):    # Function which determines collisions from enemy bullets upon the player/player entities.
        collisions = pygame.sprite.groupcollide(self.player_group, self.enemy_bullet_group, False, True)
        for collision in collisions:
            collision.currenthp -= collisions.get(collision)[0].damage

    def check_ally_shots(self):     # Function which determines collisions from ally bullets upon the enemy/enemy entities.
        collisions = pygame.sprite.groupcollide(self.enemy_group, self.ally_bullet_group, False, True)
        for collision in collisions:
            collision.currenthp -= collisions.get(collision)[0].damage

    def check_ally_abilities(self): # Function which determines collisions from ally abilities upon the enemy/enemy entities.
        collisions = pygame.sprite.groupcollide(self.enemy_group, self.ally_ability_group, False, False)
        for collision in collisions:
            collision.currenthp -= collisions.get(collision)[0].damage