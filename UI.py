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

    def player_health_bar(self):
        pygame.draw.rect(self.screen, "black" , pygame.Rect(565, 390, 70, 10))
        health_bar_percent = 70*(self.player.currenthp / self.player.maxhp)
        pygame.draw.rect(self.screen, "green" , pygame.Rect(565, 390, health_bar_percent, 10))


    def stats_update(self):
        self.adtext = self.base_font.render(str(self.player.attack_damage), True, "yellow")
        self.armortext = self.base_font.render(str(self.player.armor), True, "yellow")
        self.crittext = self.base_font.render(str(self.player.crit_chance), True, "yellow")
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

    def enemy_health_bars(self):
        player_pos = self.player.rect
        self.offset.x = player_pos.centerx - WIDTH // 2
        self.offset.y = player_pos.centery - HEIGHT // 2

        for enemy in self.enemy_group:
            offset_pos = enemy.rect.center - self.offset
            pygame.draw.rect(self.screen, "black" , pygame.Rect(offset_pos.x - 35, offset_pos.y + 40, 70, 10))
            health_bar_percent = 70*(enemy.currenthp / enemy.maxhp)
            pygame.draw.rect(self.screen, "red" , pygame.Rect(offset_pos.x - 35, offset_pos.y + 40, health_bar_percent, 10))

    def display_items(self):
        items = self.player.itemList

    def update(self):
        self.stats_update()
        self.player_health_bar()
        self.enemy_health_bars()

    
