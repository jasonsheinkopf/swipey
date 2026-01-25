"""Procedurally generated starfield background with twinkling animation."""
import random
import pygame


class Star:
    """A single twinkling star."""
    
    def __init__(self, x, y, size, period):
        self.x = x
        self.y = y
        self.size = size
        self.period = period  # milliseconds for one complete twinkle cycle
        self.phase = random.uniform(0, 2 * 3.14159)  # random starting phase
        
    def get_opacity(self, time_ms):
        """Calculate opacity based on time (20% to 100%)."""
        import math
        # Sine wave oscillation
        cycle = (time_ms / self.period + self.phase) % (2 * math.pi)
        # Map sine wave (-1 to 1) to opacity range (0.2 to 1.0)
        opacity = 0.6 + 0.4 * math.sin(cycle)
        return max(0.2, min(1.0, opacity))


class Starfield:
    """Manages the background starfield."""
    
    def __init__(self, screen_width, screen_height, star_count=100):
        self.stars = []
        
        for _ in range(star_count):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            size = random.randint(1, 3)
            period = random.uniform(2000, 6000)  # 2-6 seconds
            self.stars.append(Star(x, y, size, period))
    
    def draw(self, screen, time_ms):
        """Draw all stars with current opacity."""
        for star in self.stars:
            opacity = star.get_opacity(time_ms)
            color_value = int(255 * opacity)
            color = (color_value, color_value, color_value)
            
            if star.size == 1:
                screen.set_at((int(star.x), int(star.y)), color)
            else:
                pygame.draw.circle(screen, color, (int(star.x), int(star.y)), star.size)
