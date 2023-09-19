import pygame
import math
from keys import *
from Lucian import *
from Camera import *

# Initialize window

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Top-down project')
clock = pygame.time.Clock()

exit = False

background = pygame.image.load('Images/ground.png').convert()
# background = pygame.transform.scale(background,(WIDTH, HEIGHT))
flash_icon = pygame.image.load('Images/flash.png').convert()
flash_icon_grey = pygame.image.load('Images/flash_grey.png').convert()

pygame.mixer.music.load("audio/SoLTheme.mp3")
pygame.mixer.music.set_volume(0.01)
pygame.mixer.music.play(-1)

bullet_sprite_group = pygame.sprite.Group()
sprites_group = pygame.sprite.Group()

player = Lucian(screen, bullet_sprite_group, sprites_group)
camera = Camera(player, sprites_group, screen, background)
sprites_group.add(player)

while not exit:
    input = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

    screen.blit(background, (0,0))
    camera.camera_draw()

    if player.flash_cd == 0:
        screen.blit(flash_icon, (1100, 600))
    else:
        screen.blit(flash_icon_grey, (1100, 600))
    
    if player.ability_ult_cd == 0:
        screen.blit(player.ability_ult_image, (1000, 600))
    else:
        screen.blit(player.ability_ult_image_grey, (1000, 600))

    if player.ability_ult_cd == 0:
        screen.blit(player.ability_ult_image, (1000, 600))
    else:
        screen.blit(player.ability_ult_image_grey, (1000, 600))

    if player.ability_1_cd == 0:
        screen.blit(player.ability_1_image, (900, 600))
    else:
        screen.blit(player.ability_1_image_grey, (900, 600))
        
    # sprites_group.draw(screen)
    sprites_group.update()
    pygame.display.update()
    clock.tick(FRAME_RATE)

pygame.quit()
