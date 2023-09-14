import pygame
from keys import *


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        # Import images for character and flash animation.
        self.image = pygame.transform.scale(pygame.image.load("images/lucian.jpg").convert_alpha(),(PLAYER_WIDTH, PLAYER_HEIGHT))
        self.flash_particles = pygame.transform.scale(pygame.image.load("images/flash_particles.png").convert_alpha(),(PLAYER_WIDTH, PLAYER_HEIGHT))

        self.position = pygame.math.Vector2(START_X, START_Y)   # Current player location.
        self.speed = PLAYER_SPEED                               # Player's current speed.
        self.flash_cd = 0                                       # Cooldown of the flash ability.
        self.display_flash = False                              # Variable for displaying the flash animation.
        self.display_timer = 0                                  # Timer for how long the flash animation stays on screen.
        self.screen = screen                                    # Game window.
        self.flash_x = 0                                        # Location of where the player is flashing from on the x-axis.
        self.flash_y = 0                                        # Location of where the player is flashing from on the y-axis.


    def player_input_wasd(self):    # Method responsible for handling wasd movement of the player.
        self.x_movement = 0
        self.y_movement = 0

        input = pygame.key.get_pressed()
        if input[pygame.K_w]:
            self.y_movement = -self.speed
        if input[pygame.K_a]:
            self.x_movement = -self.speed
        if input[pygame.K_s]:
            self.y_movement = self.speed
        if input[pygame.K_d]:
            self.x_movement = self.speed
        
        
    def flash_cooldown(self):       # Method for timing the cooldown of the flash ability.
        if self.flash_cd >= 500:
            self.flash_cd = 0
        elif self.flash_cd > 0:
            self.flash_cd += 1

    def draw_flash(self):           # Method which displays and fades away the flash ability.
        if self.display_flash:
            self.flash_particles.set_alpha(2.5 * self.display_timer)
            self.screen.blit(self.flash_particles, (self.flash_x, self.flash_y))
    
    def update_flash(self):         # Method which continuously updates the variables relating to flash.
        if self.display_flash:
            self.display_timer -= 1
            self.draw_flash()
            if self.display_timer <= 0:
                self.display_flash = False

    def show_flash(self):           # Method which initializes the flash animation and starts the timer upon button press.
        self.display_flash = True
        self.display_timer = 30
        self.draw_flash()

    
    def player_input_flash(self):   # Method which handles the user input for flash (f).
        self.flash_cooldown()
        flash_sound = pygame.mixer.Sound("audio/flash_sound.mp3") # Retrieves the flash audio.
        flash_sound.set_volume(0.1)

        input = pygame.key.get_pressed()    # Retrieves the key presses.
        x, y = pygame.mouse.get_pos()       # Retrieves the current position of the mouse.

        # If flash is not on cooldown and the f key is pressed, teleport the character either 300 units or to where the mouse is, whatever is closer.
        if input[pygame.K_f] and self.flash_cd == 0:    
            pygame.mixer.Sound.play(flash_sound)
            self.flash_x = self.position.x
            self.flash_y = self.position.y
            self.show_flash()
            if x - self.flash_x > FLASH_DISTANCE:
                x = self.flash_x + FLASH_DISTANCE
            elif x - self.flash_x < -FLASH_DISTANCE:
                x = self.flash_x - FLASH_DISTANCE 
            if y - self.flash_y > FLASH_DISTANCE:
                y = self.flash_y + FLASH_DISTANCE
            elif y - self.flash_y < -FLASH_DISTANCE:
                y = self.flash_y - FLASH_DISTANCE 
            self.position = pygame.math.Vector2(x, y)
            self.flash_cd = 1

    def update_position(self):  # Update all positions based off player input.
        self.player_input_wasd()
        self.update_flash()
        self.player_input_flash()
        self.position += pygame.math.Vector2(self.x_movement, self.y_movement)
