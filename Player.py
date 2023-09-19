import pygame
import math
from Bullet import *
from keys import *


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, bullet_sprite_group, sprites_group, char_image, bullet_speed, bullet_allowed_time):
        super().__init__()
        # Character Image
        self.image = char_image     

        # Flash ability related variables
        self.flash_particles = pygame.transform.scale(pygame.image.load("images/flash_particles.png").convert_alpha(),(PLAYER_WIDTH, PLAYER_HEIGHT))
        self.flash_sound = pygame.mixer.Sound("audio/flash_sound.mp3") 
        self.flash_sound.set_volume(0.01)
        self.flash_cd = 0
        self.display_flash = False
        self.display_timer = 0
        self.flash_x = 0                                        # Location of where the player is flashing from on the x-axis.
        self.flash_y = 0                                        # Location of where the player is flashing from on the y-axis.

        # Sprite/image/Screen related variables
        self.bullet_sprite_group = bullet_sprite_group
        self.sprites_group = sprites_group
        self.position = pygame.math.Vector2(START_X, START_Y)   # Current player location.
        self.base_image = self.image    # Base image saved for rotation purposes.
        self.hitbox = self.base_image.get_rect(center = self.position)  # Both rects exist for hitbox information purposes.
        self.rect = self.hitbox.copy()
        self.speed = PLAYER_SPEED                               # Player's current speed.
        self.screen = screen                                    # Game window.

        # Shooting related variables
        self.fire = False
        self.shoot_cd = 0
        self.gun_offset = pygame.math.Vector2(OFFSET_X, OFFSET_Y)
        self.bullet_speed = bullet_speed
        self.bullet_allowed_time = bullet_allowed_time


    def player_rotation(self):  # Method responsible for rotating player icon in relation to the mouse
        mouse_pos = pygame.mouse.get_pos()       
        x_rotation = (mouse_pos[0] - self.hitbox.centerx)
        y_rotation = (mouse_pos[1] - self.hitbox.centery)
        self.angle = math.degrees(math.atan2(y_rotation, x_rotation))
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def player_character_inputs(self):    # Method responsible for player movement and shooting.
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
        
        if self.x_movement != 0 and self.y_movement != 0: 
            self.x_movement /= math.sqrt(2)
            self.y_movement /= math.sqrt(2)

        if pygame.mouse.get_pressed() == (1, 0, 0):
            self.fire = True
            self.firing()
        else:
            self.fire = False
        
    def firing(self):
        if self.shoot_cd == 0:
            self.shoot_cd = SHOOT_CD
            start_point = self.position + self.gun_offset.rotate(self.angle)
            self.bullet = Bullet(start_point.x, start_point.y, self.angle, self.bullet_speed, self.bullet_allowed_time)
            self.bullet_sprite_group.add(self.bullet)
            self.sprites_group.add(self.bullet)


    def flash_timer(self):       # Method for timing the cooldown of the flash ability.
        if self.flash_cd >= 500:
            self.flash_cd = 0
        elif self.flash_cd > 0:
            self.flash_cd += 1

    def draw_flash(self):           # Method which displays and fades away the flash ability.
        if self.display_flash:
            self.flash_particles.set_alpha(2.5 * self.display_timer)
            self.screen.blit(self.flash_particles, (self.flash_x - 0.5*PLAYER_WIDTH, self.flash_y - 0.5*PLAYER_HEIGHT))
    
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
        self.flash_timer()

        input = pygame.key.get_pressed()    # Retrieves the key presses.
        x, y = pygame.mouse.get_pos()       # Retrieves the current position of the mouse.

        # If flash is not on cooldown and the f key is pressed, teleport the character either 300 units or to where the mouse is, whatever is closer.
        if input[pygame.K_f] and self.flash_cd == 0:    
            pygame.mixer.Sound.play(self.flash_sound)
            self.flash_x = self.hitbox.centerx
            self.flash_y = self.hitbox.centery
            self.show_flash()
            if x - self.flash_x > FLASH_DISTANCE:
                x = self.flash_x + FLASH_DISTANCE
            elif x - self.flash_x < -FLASH_DISTANCE:
                x = self.flash_x - FLASH_DISTANCE 
            if y - self.flash_y > FLASH_DISTANCE:
                y = self.flash_y + FLASH_DISTANCE
            elif y - self.flash_y < -FLASH_DISTANCE:
                y = self.flash_y - FLASH_DISTANCE 
            self.position = pygame.math.Vector2(x, y) # Note - This ability has not been updated to have a circular range - rather, it is more like a square.
            self.flash_cd = 1

    def register_player_inputs(self):
        self.player_character_inputs()
        self.update_flash()
        self.player_input_flash()
        self.position += pygame.math.Vector2(self.x_movement, self.y_movement)


    def update(self):  # Update all positions based off player input.
        self.register_player_inputs()
        self.hitbox.center = self.position
        self.rect.center = self.hitbox.center
        self.player_rotation()
        if self.shoot_cd > 0:
            self.shoot_cd -= 1
