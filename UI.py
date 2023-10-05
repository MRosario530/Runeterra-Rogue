import pygame

class UI():
    pygame.font.init()
    base_font = pygame.font.SysFont("cambria", 22)

    def __init__(self, player):
        self.stats_image = pygame.image.load("images/stats.png")
        self.player = player
        self.statsrect = self.stats_image.get_rect(center=(90, 626))


        self.player_ad = player.attack_damage
        self.player_armor = player.armor
        self.player_crit = player.crit_chance
        self.player_ap = player.ability_power
        self.player_mr = player.magic_resist
        self.player_cdr = player.cooldown_reduction

        self.adtext = self.base_font.render(str(self.player_ad), True, "yellow")
        self.armortext = self.base_font.render(str(self.player_armor), True, "yellow")
        self.crittext = self.base_font.render(str(self.player_crit), True, "yellow")
        self.aptext = self.base_font.render(str(self.player_ap), True, "yellow")
        self.mrtext = self.base_font.render(str(self.player_mr), True, "yellow")
        self.cdrtext = self.base_font.render(str(self.player_cdr), True, "yellow")

        self.adtext_rect = self.adtext.get_rect(center=(70, 582))
        self.armortext_rect = self.armortext.get_rect(center=(70, 629))
        self.crittext_rect = self.crittext.get_rect(center=(70, 677))
        self.aptext_rect = self.aptext.get_rect(center=(150, 582))
        self.mrtext_rect = self.mrtext.get_rect(center=(150, 629))
        self.cdrtext_rect = self.cdrtext.get_rect(center=(150, 677))

        

    def update(self, screen):
        self.stats_update(screen)


    def stats_update(self, screen):
        screen.blit(self.stats_image, self.statsrect)
        screen.blit(self.adtext, self.adtext_rect)
        screen.blit(self.armortext, self.armortext_rect)
        screen.blit(self.crittext, self.crittext_rect)
        screen.blit(self.aptext, self.aptext_rect)
        screen.blit(self.mrtext, self.mrtext_rect)
        screen.blit(self.cdrtext, self.cdrtext_rect)

