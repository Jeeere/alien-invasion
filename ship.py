import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """
        Initialize ship and set starting position
        """
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Load ship sprite and create it's rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Spawn ship at bottom center of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #Store decimal value for ship's center
        self.center = float(self.rect.centerx)

        #Movement flags
        self.moving_right = False
        self.moving_left = False

    def move(self, ai_settings):
        """
        Update the ship's location based on movement flags
        """
        #Update ship center value
        if self.moving_right and self.rect.right < ai_settings.screen_width:
            self.center += self.ai_settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed

        #Update rect from self.center
        self.rect.centerx = self.center

    def blitme(self):
        """
        Draws the ship at its current location
        """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on screen"""
        self.center = self.screen_rect.centerx