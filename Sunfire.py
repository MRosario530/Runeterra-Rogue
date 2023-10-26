import pygame


class Sunfire(pygame.sprite.Sprite):
    def __init__(self, active_timer, position):
        super().__init__()
        self.sunfire_count = 0
        self.sunfire_active = active_timer
        self.sunfire_multiple = 1.04
        self.original_image = pygame.image.load("images/sunfire_aura.png").convert_alpha()
        self.original_rect = self.original_image.get_rect()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.center = (position[0], position[1])
        self.damage = 20

    def sunfire_expand(self):   # Function which expands the sunfire image by a set amount on every call.
        self.sunfire_multiple = self.sunfire_multiple * 1.06
        self.image = pygame.transform.scale_by(self.original_image, self.sunfire_multiple)
        self.rect = self.original_rect.scale_by(self.sunfire_multiple)

        self.rect.center = (self.position[0], self.position[1])
        self.sunfire_active -= 1
        if self.sunfire_active <= 0:
            self.kill()

    def update(self):
        self.sunfire_expand()