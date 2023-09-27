# Character select background photo by Mudassir Ali: https://www.pexels.com/photo/blue-wallpaper-2680270/

import pygame, sys
import math
from Button import *
from keys import *
from Lucian import *
from Camera import *
from Enemy import *
from Level import *
from Collisions import *

pygame.font.init()
base_font = pygame.font.SysFont("cambria", 50)
character_font = pygame.font.SysFont("times new roman", 70)
isAlive = False

class Menu():
    def __init__(self, screen, clock):
        super().__init__()
        self.menu_bg = pygame.transform.scale(pygame.image.load("images/demacia_splash.jpeg"),(WIDTH, HEIGHT))
        self.character_select_bg = pygame.transform.scale(pygame.image.load("images/character_select.jpg"),(WIDTH, HEIGHT))
        self.screen = screen
        self.clock = clock

        self.background = pygame.image.load('Images/ground.png').convert()
        self.flash_icon = pygame.image.load('Images/flash.png').convert()
        self.flash_icon_grey = pygame.image.load('Images/flash_grey.png').convert()

        self.enemy_bullet_group = pygame.sprite.Group()
        self.ally_bullet_group = pygame.sprite.Group()
        self.all_sprites_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()


    def start_screen(self):
        play_button = Button(image=pygame.image.load("images/button_bg.png"), pos=(600, 300), text_input="PLAY", font=base_font, button_color="blue", button_hover_color="white")
        quit_button = Button(image=pygame.image.load("images/button_bg.png"), pos=(600, 450), text_input="QUIT", font=base_font, button_color="blue", button_hover_color="white")

        while True:
            self.screen.blit(self.menu_bg, (0,0))
            mouse_pos = pygame.mouse.get_pos()
            title_text = base_font.render("RUNETERRA ROGUE", True, "#1F6080")
            text_rect = title_text.get_rect(center=(600,100))

            self.screen.blit(title_text, text_rect)

            for button in [play_button, quit_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(mouse_pos):
                        self.character_select()
                    if quit_button.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
        
    def character_select(self):

        play_button_display = False
        Lucian_button = Button(image=pygame.image.load("images/LucianSquare.png"), pos=(600, 600), text_input="", font=base_font, button_color="blue", button_hover_color="white")
        play_button = Button(image=pygame.image.load("images/button_bg.png"), pos=(1000, 600), text_input="PLAY", font=base_font, button_color="blue", button_hover_color="white")
        back_button = Button(image=pygame.image.load("images/button_bg.png"), pos=(200, 600), text_input="BACK", font=base_font, button_color="blue", button_hover_color="white")
        current_character_text = ""
        current_character = None
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.character_select_bg, (0,0))

            title_text = character_font.render(current_character_text, True, "white")
            text_rect = title_text.get_rect(center=(600,100))

            self.screen.blit(title_text, text_rect)

            for button in [back_button, Lucian_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            if play_button_display == True:
                play_button.changeColor(mouse_pos)
                play_button.update(self.screen)

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if Lucian_button.checkForInput(mouse_pos):
                            play_button_display = True
                            current_character_text = "Lucian"
                            current_character = Lucian(self.screen, self.ally_bullet_group, self.all_sprites_group, self.enemy_group)
                        if back_button.checkForInput(mouse_pos):
                            self.start_screen()
                        if play_button.checkForInput(mouse_pos):
                            self.play(current_character)
            pygame.display.update()

    def play(self, character):
        exit = False

        player = character
        camera = Camera(player, self.all_sprites_group, self.screen, self.background)
        self.all_sprites_group.add(player)
        self.player_group.add(player)

        timer_sec = 0
        timer = pygame.USEREVENT + 1                                     
        pygame.time.set_timer(timer, 1000)

        level = Level(self.enemy_group, self.all_sprites_group, player, self.player_group, self.enemy_bullet_group)
        check_collides = Collisions(self.ally_bullet_group, self.enemy_bullet_group, self.player_group, self.enemy_group)

        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                    pygame.quit()
                    sys.exit()
                if event.type == timer:
                    if timer_sec % 5 == 0 :
                        level.update(timer_sec)
                        timer_sec += 1
                    else:
                        timer_sec += 1

            self.screen.blit(self.background, (0,0))
            camera.camera_draw()

            if player.flash_cd == 0:
                self.screen.blit(self.flash_icon, (1100, 600))
            else:
                self.screen.blit(self.flash_icon_grey, (1100, 600))
            
            if player.ability_ult_cd == 0:
                self.screen.blit(player.ability_ult_image, (1000, 600))
            else:
                self.screen.blit(player.ability_ult_image_grey, (1000, 600))

            if player.ability_ult_cd == 0:
                self.screen.blit(player.ability_ult_image, (1000, 600))
            else:
                self.screen.blit(player.ability_ult_image_grey, (1000, 600))

            if player.ability_1_cd == 0:
                self.screen.blit(player.ability_1_image, (900, 600))
            else:
                self.screen.blit(player.ability_1_image_grey, (900, 600))

            check_collides.check_ally_shots()
            check_collides.check_enemy_shots()
            if (len(self.player_group.sprites()) == 0):
                self.game_over_screen()

            self.all_sprites_group.update()
            pygame.display.update()
            self.clock.tick(FRAME_RATE)

    def game_over_screen(self):
        restart_button = Button(image=pygame.image.load("images/button_bg.png"), pos=(600, 600), text_input="MENU", font=base_font, button_color="blue", button_hover_color="white")
        self.enemy_bullet_group.empty()
        self.ally_bullet_group.empty()
        self.all_sprites_group.empty()
        self.enemy_group.empty()
        self.player_group.empty()
        exit = False
        while not exit:
            self.screen.fill("black")
            mouse_pos = pygame.mouse.get_pos()    
            restart_button.changeColor(mouse_pos)
            restart_button.update(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.checkForInput(mouse_pos):
                        self.start_screen()
            pygame.display.update()



