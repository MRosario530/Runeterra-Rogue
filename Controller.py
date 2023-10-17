# Character select background photo by Mudassir Ali: https://www.pexels.com/photo/blue-wallpaper-2680270/

import pygame, sys, csv, random
from Button import *
from keys import *
from Lucian import *
from Camera import *
from Enemy import *
from Level import *
from Collisions import *
from UI import *
from Item import *

pygame.font.init()
base_font = pygame.font.SysFont("cambria", 50)
character_font = pygame.font.SysFont("times new roman", 70)
item_font = pygame.font.SysFont("cambria", 22)

isAlive = False

class Controller():
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


    def loadItems(self):
        with open('item.csv', 'r') as csv_file:
            self.items = []
            reader = csv.reader(csv_file)
            next(reader, None)
            for row in reader:
                item = Item(row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7]), pygame.image.load(row[8]), row[9])
                self.items.append(item)
            csv_file.close()


    def start_screen(self):
        play_button = Button(image=pygame.image.load("images/button_bg.png"), pos=(600, 300), text_input="PLAY", font=base_font, button_color="blue", button_hover_color="white")
        quit_button = Button(image=pygame.image.load("images/button_bg.png"), pos=(600, 450), text_input="QUIT", font=base_font, button_color="blue", button_hover_color="white")
        self.loadItems()
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
        center_image_display = False
        center_image = None
        play_button_display = False
        Lucian_button = Button(image=pygame.image.load("images/LucianSquare.png"), pos=(600, 600), text_input="", font=base_font, button_color="blue", button_hover_color="white")
        play_button = Button(image=pygame.image.load("images/button_bg.png"), pos=(1000, 600), text_input="PLAY", font=base_font, button_color="blue", button_hover_color="white")
        back_button = Button(image=pygame.image.load("images/button_bg.png"), pos=(200, 600), text_input="BACK", font=base_font, button_color="blue", button_hover_color="white")

        Lucian_image = pygame.image.load("images/Lucian_splash.png")
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

            if center_image_display == True:
                self.screen.blit(center_image, center_image.get_rect(center=(600,350)))

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if Lucian_button.checkForInput(mouse_pos):
                            play_button_display = True
                            center_image_display = True
                            current_character_text = "Lucian"
                            current_character = Lucian(self.screen, self.ally_bullet_group, self.all_sprites_group, self.enemy_group)
                            center_image = Lucian_image
                        if back_button.checkForInput(mouse_pos):
                            self.start_screen()
                        if play_button.checkForInput(mouse_pos):
                            self.play(current_character)
            pygame.display.update()

    def play(self, character):
        exit = False
        self.player = character
        userinterface = UI(self.screen, self.player, self.enemy_group)

        camera = Camera(self.player, self.all_sprites_group, self.screen, self.background)
        self.all_sprites_group.add(self.player)
        self.player_group.add(self.player)

        timer_sec = 0
        timer = pygame.USEREVENT + 1                                     
        pygame.time.set_timer(timer, 1000)

        level = Level(self.enemy_group, self.all_sprites_group, self.player, self.player_group, self.enemy_bullet_group)
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
                        if timer_sec % 10 == 0 and timer_sec != 0:
                            self.item_choice_screen()
                        timer_sec += 1
                    else:
                        timer_sec += 1

            self.screen.blit(self.background, (0,0))
            camera.camera_draw()
            userinterface.update()


            if self.player.flash_cd == 0:
                self.screen.blit(self.flash_icon, (1100, 600))
            else:
                self.screen.blit(self.flash_icon_grey, (1100, 600))
            
            if self.player.ability_ult_cd == 0:
                self.screen.blit(self.player.ability_ult_image, (1000, 600))
            else:
                self.screen.blit(self.player.ability_ult_image_grey, (1000, 600))

            if self.player.ability_ult_cd == 0:
                self.screen.blit(self.player.ability_ult_image, (1000, 600))
            else:
                self.screen.blit(self.player.ability_ult_image_grey, (1000, 600))

            if self.player.ability_1_cd == 0:
                self.screen.blit(self.player.ability_1_image, (900, 600))
            else:
                self.screen.blit(self.player.ability_1_image_grey, (900, 600))

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

    def item_choice_screen(self):
        current_item_choices = []
        current_item_choices.append(random.choice(self.items))
        current_item_choices.append(random.choice(self.items))
        current_item_choices.append(random.choice(self.items))

        item1_button = Button(image=pygame.image.load("images/item_button.png"), pos=(300, 350), text_input=current_item_choices[0].name, font=item_font, button_color="grey", button_hover_color="white")
        item2_button = Button(image=pygame.image.load("images/item_button.png"), pos=(600, 350), text_input=current_item_choices[1].name, font=item_font, button_color="grey", button_hover_color="white")
        item3_button = Button(image=pygame.image.load("images/item_button.png"), pos=(900, 350), text_input=current_item_choices[2].name, font=item_font, button_color="grey", button_hover_color="white")

        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill("#082430")
            title_text = character_font.render("Select your item!", True, "White")
            text_rect = title_text.get_rect(center=(600,100))

            self.screen.blit(title_text, text_rect)

            for button in [item1_button, item2_button, item3_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            self.screen.blit(current_item_choices[0].image, (286, 275))
            self.screen.blit(current_item_choices[1].image, (586, 275))
            self.screen.blit(current_item_choices[2].image, (886, 275))

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if item1_button.checkForInput(mouse_pos):
                            self.player.updateStats(current_item_choices[0])
                            self.player.item_list.append(current_item_choices[0])
                            return
                        if item2_button.checkForInput(mouse_pos):
                            self.player.updateStats(current_item_choices[1])
                            self.player.item_list.append(current_item_choices[1])
                            return
                        if item3_button.checkForInput(mouse_pos):
                            self.player.updateStats(current_item_choices[2])
                            self.player.item_list.append(current_item_choices[2])
                            return

            pygame.display.update()






