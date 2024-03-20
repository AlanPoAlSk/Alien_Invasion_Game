import pygame.font
import os
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information."""
    
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.text_color_hs = (230, 30, 30)
        self.score_font_size = 36  
        self.level_font_size = 24  
        self.font = pygame.font.SysFont(None, self.score_font_size)
        
        # Load the high score from a file
        self.high_score_file = 'high_score.txt'
        self.load_high_score()
        
        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        
    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 5 + ship_number * ship.rect.width
            ship.rect.y = 5
            self.ships.add(ship)
        
    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = f"Level: {self.stats.level}"
        self.level_image = pygame.font.SysFont(None, self.level_font_size).render(level_str, True, self.text_color, self.settings.bg_color)
        
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
        
    def prep_score(self):
        """Turn the score info a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"Score: {rounded_score}"
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def show_score(self):
        """Draw scores, level, and ships/lives to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        
    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"High Score: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color_hs, self.settings.bg_color)
        
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        
        # Save the high score to the file
        with open(self.high_score_file, 'w') as file:
            file.write(str(self.stats.high_score))
        
    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            
    def load_high_score(self):
        """Load the high score from a file."""
        if os.path.exists(self.high_score_file):
            with open(self.high_score_file, 'r') as file:
                try:
                    self.stats.high_score = int(file.read())
                except ValueError:
                    # Handle if the file doesn't contain a valid high score
                    self.stats.high_score = 0
        else:
            # Handle if the file doesn't exist
            self.stats.high_score = 0