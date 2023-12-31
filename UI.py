import pygame
from keys import *

class UI():
    pygame.font.init()
    base_font = pygame.font.SysFont("cambria", 22)

    def __init__(self, screen, player, enemy_group):
        self.stats_image = pygame.image.load("images/stats.png")
        self.screen = screen
        self.player = player
        self.statsrect = self.stats_image.get_rect(center=(90, 626))
        self.enemy_group = enemy_group
        self.offset = pygame.math.Vector2()

        # Variables related to displaying character stats.
        self.adtext = self.base_font.render(str(self.player.attack_damage), True, "yellow")
        self.armortext = self.base_font.render(str(self.player.armor), True, "yellow")
        self.crittext = self.base_font.render(str(self.player.crit_chance), True, "yellow")
        self.aptext = self.base_font.render(str(self.player.ability_power), True, "yellow")
        self.mrtext = self.base_font.render(str(self.player.magic_resist), True, "yellow")
        self.cdrtext = self.base_font.render(str(self.player.cooldown_reduction), True, "yellow")

        self.adtext_rect = self.adtext.get_rect(topleft=(50, 570))
        self.armortext_rect = self.armortext.get_rect(topleft=(50, 618))
        self.crittext_rect = self.crittext.get_rect(topleft=(50, 670))
        self.aptext_rect = self.aptext.get_rect(topleft=(140, 570))
        self.mrtext_rect = self.mrtext.get_rect(topleft=(140, 618))
        self.cdrtext_rect = self.cdrtext.get_rect(topleft=(140, 670))

    def player_health_bar(self):    # Function which draws and updates the player health bar.
        pygame.draw.rect(self.screen, "black" , pygame.Rect(565, 390, 70, 10))
        health_bar_percent = 70*(self.player.currenthp / self.player.maxhp)
        pygame.draw.rect(self.screen, "green" , pygame.Rect(565, 390, health_bar_percent, 10))

    def stats_update(self):         # Function which draws and updates the character stats in the bottom-right of the screen.
        self.adtext = self.base_font.render(str(self.player.attack_damage), True, "yellow")
        self.armortext = self.base_font.render(str(self.player.armor), True, "yellow")
        if self.player.crit_chance <= 100:
            self.crittext = self.base_font.render(str(self.player.crit_chance) + "%", True, "yellow")
        else:
            self.crittext = self.base_font.render("100%", True, "yellow")
        
        self.aptext = self.base_font.render(str(self.player.ability_power), True, "yellow")
        self.mrtext = self.base_font.render(str(self.player.magic_resist), True, "yellow")
        self.cdrtext = self.base_font.render(str(self.player.cooldown_reduction), True, "yellow")

        self.screen.blit(self.stats_image, self.statsrect)
        self.screen.blit(self.adtext, self.adtext_rect)
        self.screen.blit(self.armortext, self.armortext_rect)
        self.screen.blit(self.crittext, self.crittext_rect)
        self.screen.blit(self.aptext, self.aptext_rect)
        self.screen.blit(self.mrtext, self.mrtext_rect)
        self.screen.blit(self.cdrtext, self.cdrtext_rect)

    def enemy_health_bars(self):    # Function which draws and updates all enemy health bars.
        player_pos = self.player.rect
        self.offset.x = player_pos.centerx - WIDTH // 2
        self.offset.y = player_pos.centery - HEIGHT // 2

        for enemy in self.enemy_group:
            offset_pos = enemy.rect.center - self.offset
            pygame.draw.rect(self.screen, "black" , pygame.Rect(offset_pos.x - 35, offset_pos.y + 40, 70, 10))
            health_bar_percent = 70*(enemy.currenthp / enemy.maxhp)
            pygame.draw.rect(self.screen, "red" , pygame.Rect(offset_pos.x - 35, offset_pos.y + 40, health_bar_percent, 10))

    def display_items(self):    # Function which draws and updates the player items in the top-right of the screen.
        item_image_x = 1200
        item_image_y = 0
        items = self.player.item_list
        for item in items:
            self.screen.blit(item.image, item.image.get_rect(topright=(item_image_x, item_image_y)))
            item_image_x -= 38
            if item_image_x < 800:
                item_image_y += 38
                item_image_x = 1200

    def update(self):
        self.enemy_health_bars()
        self.stats_update()
        self.player_health_bar()
        self.display_items()

    
