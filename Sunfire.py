import pygame


class Sunfire(pygame.sprite.Sprite):
    def __init__(self, active_timer, position):
        super().__init__()
        self.sunfire_count = 0
        self.sunfire_active = active_timer
        self.sunfire_radius = 25
        self.sunfire_size = 90
        self.image = pygame.image.load("images/sunfire_aura.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.damage = 1

    def sunfire_expand(self):
        self.sunfire_size = self.sunfire_size * 1.04
        self.image = pygame.transform.scale(self.image, (self.sunfire_size, self.sunfire_size))
        self.rect = self.image.get_rect()
        #self.rect.topleft = (600 - self.image.get_width() / 2, 350 - self.image.get_height() / 2)
        self.sunfire_active -= 1
        if self.sunfire_active <= 0:
            self.kill()

    def updatePlayerPos(self, position):
        self.rect.center = position

    def update(self):
        self.sunfire_expand()