"""Collectible target with pulsing glow and spawn logic."""
import random
import pygame
import math


class Collectible:
    """The pulsing collectible target."""
    
    def __init__(self, screen_width, screen_height, player_radius):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_radius = player_radius
        
        # Smaller than player
        self.radius = int(player_radius * 0.6)
        
        self.color = (255, 255, 255)  # White
        self.x = 0
        self.y = 0
        
        # Pulsing animation
        self.pulse_phase = 0
        
    def spawn(self, player_x, player_y):
        """Spawn at a random valid location."""
        # Safe zone: 10% margin from edges
        margin = 0.1
        min_x = self.screen_width * margin
        max_x = self.screen_width * (1 - margin)
        min_y = self.screen_height * margin
        max_y = self.screen_height * (1 - margin)
        
        # Minimum distance from player: 20% of screen
        min_distance = min(self.screen_width, self.screen_height) * 0.2
        
        attempts = 0
        while attempts < 100:
            self.x = random.uniform(min_x, max_x)
            self.y = random.uniform(min_y, max_y)
            
            # Check distance from player
            dx = self.x - player_x
            dy = self.y - player_y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance >= min_distance:
                break
                
            attempts += 1
    
    def update(self, dt):
        """Update pulsing animation."""
        self.pulse_phase += dt * 2  # 2 radians per second
    
    def draw(self, screen):
        """Draw the collectible with pulsing glow."""
        # Oscillate opacity between 0.5 and 1.0
        opacity = 0.75 + 0.25 * math.sin(self.pulse_phase)
        
        # Draw main circle with varying opacity
        color_value = int(255 * opacity)
        color = (color_value, color_value, color_value)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
    
    def check_collision(self, player_x, player_y, player_radius):
        """Check if player collects this target."""
        dx = self.x - player_x
        dy = self.y - player_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        return distance < (self.radius + player_radius)
    
    def get_position(self):
        """Return current position as tuple."""
        return (self.x, self.y)
