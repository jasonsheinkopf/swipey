"""Collectible target with pulsing glow and spawn logic."""
import random
import pygame
import math


class Collectible:
    """The pulsing collectible target - green diamond."""
    
    def __init__(self, screen_width, screen_height, player_radius):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_radius = player_radius
        
        # Size (half-width of diamond)
        self.size = int(player_radius * 0.8)
        
        self.color = (0, 255, 100)  # Green
        self.x = 0
        self.y = 0
        
        # Pulsing animation
        self.pulse_phase = 0
        
    def spawn(self, player_x, player_y, obstacles=None):
        """Spawn at a random valid location, avoiding player and obstacles."""
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
            
            if distance < min_distance:
                attempts += 1
                continue
            
            # Check distance from obstacles
            if obstacles:
                too_close = False
                for obs in obstacles:
                    ox, oy = obs.get_position()
                    dx = self.x - ox
                    dy = self.y - oy
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist < obs.radius + self.size + 20:
                        too_close = True
                        break
                if too_close:
                    attempts += 1
                    continue
            
            break
    
    def update(self, dt):
        """Update pulsing animation."""
        self.pulse_phase += dt * 3  # 3 radians per second
    
    def draw(self, screen):
        """Draw the collectible as a pulsing green diamond."""
        # Oscillate size between 0.8 and 1.2
        scale = 1.0 + 0.2 * math.sin(self.pulse_phase)
        size = int(self.size * scale)
        
        # Diamond points (rotated square)
        points = [
            (self.x, self.y - size),      # Top
            (self.x + size, self.y),       # Right
            (self.x, self.y + size),       # Bottom
            (self.x - size, self.y)        # Left
        ]
        
        # Draw glow (larger, semi-transparent)
        glow_size = int(size * 1.3)
        glow_points = [
            (self.x, self.y - glow_size),
            (self.x + glow_size, self.y),
            (self.x, self.y + glow_size),
            (self.x - glow_size, self.y)
        ]
        glow_surface = pygame.Surface((glow_size * 3, glow_size * 3), pygame.SRCALPHA)
        glow_color = (0, 255, 100, 80)
        adjusted_points = [(p[0] - self.x + glow_size * 1.5, p[1] - self.y + glow_size * 1.5) for p in glow_points]
        pygame.draw.polygon(glow_surface, glow_color, adjusted_points)
        screen.blit(glow_surface, (self.x - glow_size * 1.5, self.y - glow_size * 1.5))
        
        # Draw main diamond
        pygame.draw.polygon(screen, self.color, points)
        
        # Draw bright center
        inner_size = int(size * 0.5)
        inner_points = [
            (self.x, self.y - inner_size),
            (self.x + inner_size, self.y),
            (self.x, self.y + inner_size),
            (self.x - inner_size, self.y)
        ]
        pygame.draw.polygon(screen, (150, 255, 200), inner_points)
    
    def check_collision(self, player_x, player_y, player_radius):
        """Check if player collects this target."""
        dx = self.x - player_x
        dy = self.y - player_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        return distance < (self.size + player_radius)
    
    def get_position(self):
        """Return current position as tuple."""
        return (self.x, self.y)