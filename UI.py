import pygame

class UI():
    pygame.font.init()
    base_font = pygame.font.SysFont("cambria", 22)

    def __init__(self, player):
        self.stats_image = pygame.image.load("images/stats.png")
        self.player = player
        self.statsrect = self.stats_image.get_rect(center=(90, 626))

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

    def health_bar(self, screen):
        pygame.draw.rect(screen, "black" , pygame.Rect(565, 390, 70, 10))
        health_bar_percent = 70*(self.player.currenthp / self.player.maxhp)
        pygame.draw.rect(screen, "green" , pygame.Rect(565, 390, health_bar_percent, 10))


    def stats_update(self, screen):

        self.adtext = self.base_font.render(str(self.player.attack_damage), True, "yellow")
        self.armortext = self.base_font.render(str(self.player.armor), True, "yellow")
        self.crittext = self.base_font.render(str(self.player.crit_chance), True, "yellow")
        self.aptext = self.base_font.render(str(self.player.ability_power), True, "yellow")
        self.mrtext = self.base_font.render(str(self.player.magic_resist), True, "yellow")
        self.cdrtext = self.base_font.render(str(self.player.cooldown_reduction), True, "yellow")

        screen.blit(self.stats_image, self.statsrect)
        screen.blit(self.adtext, self.adtext_rect)
        screen.blit(self.armortext, self.armortext_rect)
        screen.blit(self.crittext, self.crittext_rect)
        screen.blit(self.aptext, self.aptext_rect)
        screen.blit(self.mrtext, self.mrtext_rect)
        screen.blit(self.cdrtext, self.cdrtext_rect)

    def update(self, screen):
        self.stats_update(screen)
        self.health_bar(screen)
