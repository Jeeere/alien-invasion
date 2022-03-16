import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """
    A class to represent a single alien
    """
    def __init__(self, ai_settings, screen):
        """Initiliazile alien and its starting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Load the image and set rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #Start alien in top left corner of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw alien on screen"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move alien to the right"""
        self.x += self.ai_settings.alien_speed * self.ai_settings.fleet_direction
        self.rect.x = self.x
    
    def check_edges(self):
        """Return True if alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True