import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    """
    Initialize game and screen.
    """
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    # Create the play button
    play_button = Button(ai_settings, screen, "Play")

    #Create an instance to store game stats and create scoreboard
    stats = GameStats(ai_settings)
    #Get high score
    gf.get_high_score(stats)
    sb = Scoreboard(ai_settings, screen, stats)

    #Spawn a ship, group of bullets and a group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    #Create an alien fleet
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #Start main game loop
    while True:
        #Checks mouse and keyboard events
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.move(ai_settings)
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        #Updates screen
        gf.update_screen(ship, ai_settings, screen, aliens, bullets, play_button, stats, sb)

run_game()