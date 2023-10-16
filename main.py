import pygame
from keys import *
from Lucian import *
from Camera import *
from Enemy import *
from Level import *
from Item import *
from Menu import *

# Initialize window

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Runeterra Rogue')
clock = pygame.time.Clock()

pygame.mixer.music.load("audio/SoLTheme.mp3")
pygame.mixer.music.set_volume(0.01)
pygame.mixer.music.play(-1)

menu = Menu(screen, clock)

    
menu.start_screen()

pygame.quit()
