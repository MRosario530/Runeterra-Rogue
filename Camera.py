import pygame
from keys import *


class Camera(pygame.sprite.Group):
    def __init__(self, player, all_sprites_group, screen, background):
        super().__init__()
        self.player = player
        self.player_pos = player.rect
        self.offset = pygame.math.Vector2()
        self.all_sprites_group = all_sprites_group
        self.screen = screen
        self.background = background
        self.bg_rect = background.get_rect(topleft = (0,0))

    def camera_draw(self):
        self.player_pos = self.player.rect
        self.offset.x = self.player_pos.centerx - WIDTH // 2
        self.offset.y = self.player_pos.centery - HEIGHT // 2
        bg_offset_pos = self.bg_rect.topleft - self.offset
        self.screen.blit(self.background, bg_offset_pos)
        for sprite in self.all_sprites_group:
            offset_pos = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_pos)