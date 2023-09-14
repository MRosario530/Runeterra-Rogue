import pygame
import math
from keys import *
from Player import *

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


player = Player(gameDisplay)

while not exit:
    input = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

    gameDisplay.blit(background, (0,0))
    gameDisplay.blit(player.image, player.position)
    if player.flash_cd == 0:
        gameDisplay.blit(flash_icon, (1100, 600))
    else:
        gameDisplay.blit(flash_icon_grey, (1100, 600))

    player.update_position()
    pygame.display.update()
    clock.tick(FRAME_RATE)

pygame.quit()
