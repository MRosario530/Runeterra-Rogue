import pygame
import math
from keys import *
from Lucian import *

# Initialize window
pygame.init()

gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Top-down project')
clock = pygame.time.Clock()

exit = False

background = pygame.image.load('Images/grass.jpg').convert()
background = pygame.transform.scale(background,(WIDTH, HEIGHT))
flash_icon = pygame.image.load('Images/flash.png').convert()
flash_icon_grey = pygame.image.load('Images/flash_grey.png').convert()


bullet_sprite_group = pygame.sprite.Group()
sprites_group = pygame.sprite.Group()

player = Lucian(gameDisplay, bullet_sprite_group, sprites_group)

sprites_group.add(player)

while not exit:
    input = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

    gameDisplay.blit(background, (0,0))
    if player.flash_cd == 0:
        gameDisplay.blit(flash_icon, (1100, 600))
    else:
        gameDisplay.blit(flash_icon_grey, (1100, 600))
    
    if player.ability_1_cd == 0:
        gameDisplay.blit(player.ability_1_image, (1000, 600))
    else:
        gameDisplay.blit(player.ability_1_image_grey, (1000, 600))
        
    sprites_group.draw(gameDisplay)
    sprites_group.update()
    pygame.display.update()
    clock.tick(FRAME_RATE)

pygame.quit()
