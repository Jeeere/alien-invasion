class GameStats():
    """
    Track the statistics for alien invasion
    """
    def __init__(self, ai_settings):
        """Initialize the statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Start game as inactive
        self.game_active = False

        #Never reset high score
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1