import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """
    A class to manage bullets shot from the ship
    """
    def __init__(self, ai_settings, screen, ship):
        """
        Create bullet at ship location
        """
        super().__init__()
        self.screen = screen

        #Create bullet and correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, 
            ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #Store bullet position as decimal
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed = ai_settings.bullet_speed

    def update(self):
        """
        Move bullet up the screen
        """
        #Update decimal position of bullet
        self.y -= self.speed
        #Update position
        self.rect.y = self.y

    def draw_bullet(self):
        """
        Draws bullet to screen
        """
        pygame.draw.rect(self.screen, self.color, self.rect)