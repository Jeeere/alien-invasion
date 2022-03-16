import pygame, sys
from pygame.locals import *
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """
    Responds to mouse and keyboard events
    """
    #Watch for exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score(stats)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, ai_settings, bullets, screen, stats)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_keydown_events(event, ship, ai_settings, bullets, screen, stats):
    """
    Responds to keypresses
    """
    if event.key == K_d:
        ship.moving_right = True
    elif event.key == K_a:
        ship.moving_left = True
    elif event.key == K_SPACE:
        fire_bullet(ship, ai_settings, bullets, screen)
    elif event.key == K_ESCAPE:
        save_high_score(stats)


def check_keyup_events(event, ship):
    """
    Responds to key releases
    """
    if event.key == K_d:
        ship.moving_right = False
    elif event.key == K_a:
        ship.moving_left = False

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start new game if play button is pressed"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset game settings
        ai_settings.init_dynamic_settings()
        # Hide cursor
        pygame.mouse.set_visible(False)
        #Reset game stats
        stats.reset_stats()
        stats.game_active = True

        #Reset scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #Empty aliens and bullets
        aliens.empty()
        bullets.empty()

        #Create new fleet and center player
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ship, ai_settings, screen, aliens, bullets, play_button, stats, sb):
    """
    Update images on screen and flip
    """
    #Clear screen after every loop
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    #Draw the score information
    sb.show_score()

    # Draw play button if game is inactive
    if not stats.game_active:
        play_button.draw_button()

    #Update screen
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Updates bullet position and removes old bullets
    """
    #Update bullet position
    bullets.update()

    #Remove bullets that have disappeared from screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Responds to bullet-alien collisions
    """
    #Check for bullets that have hit aliens
    collisions = pygame.sprite.groupcollide(bullets, aliens, ai_settings.disable_super_bullets, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        #Remove existing bullets and create new fleet and speed up game
        bullets.empty()
        ai_settings.increase_speed()

        #Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ship, ai_settings, bullets, screen):
    """
    Adds a new bullet to the bullets group if conditions are met
    """
    if len(bullets) < ai_settings.max_bullets:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
    """
    Create a full fleet of aliens
    """
    #Create alien and find number of aliens in a row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #Create fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #Create alien and place it in the row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
        

def get_number_aliens(ai_settings, alien_width):
    """
    Calculate number of aliens that can fit in a row
    """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """
    Determine the number of rows of aliens that can fit on screen
    """
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """
    Create an alien and place it in a row
    """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def check_fleet_edges(ai_settings, aliens):
    """
    Changes fleet direction if alien has hit the edge of the screen
    """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """
    Drop the fleet and change direction
    """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Check if the fleet is at an edge and update positions of all aliens
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        print("Ship hit!!!11!!")
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    #Look for aliens hitting bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Responds to ship being hit by alien
    """
    if stats.ships_left > 0:
        print("-1 ship")
        #Decrease ships left
        stats.ships_left -= 1

        #Update scoreboard
        sb.prep_ships()

        #Remove aliens and bullets
        aliens.empty()
        bullets.empty()

        #Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        print("Game Over!!11!!!")
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Check if aliens have hit bottom of screen
    """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Treat the same as ship got hit
            print("Aliens reached the bottom111!!!!!1")
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """Check if there is a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def get_high_score(stats):
    with open("high_score.txt") as file:
        hs = file.read()
        stats.high_score = int(hs)

def save_high_score(stats):
    with open("high_score.txt", "w") as file:
        file.write(str(stats.high_score))
    sys.exit()