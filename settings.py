class Settings():
    def __init__(self):
        """Initialize static settings"""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        self.ship_limit = 3

        #Bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.max_bullets = 3
        self.disable_super_bullets = False

        #Alien settings
        self.fleet_drop_speed = 5

        # Difficulty (how fast game speeds up)
        self.speedup_scale = 1.1
        #Score scale
        self.score_scale = 1.5

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        """Initialize dynamic settings that change during game"""
        self.ship_speed = 0.7
        self.bullet_speed = 1
        self.alien_speed = 0.5
        self.alien_points = 50

        #fleet_direction 1 represents right ; -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values when next level starts"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print("New point value: " + str(self.alien_points))