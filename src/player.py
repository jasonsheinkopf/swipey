"""Player sphere with frictionless physics and screen wrapping."""
import pygame


class Player:
    """The white sphere controlled by swipes."""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Size: ~3% of screen width
        self.radius = int(screen_width * 0.03)
        
        # Start in center
        self.x = screen_width / 2
        self.y = screen_height / 2
        
        # Frictionless movement (velocity persists)
        self.vx = 0.0
        self.vy = 0.0
        
        self.color = (255, 255, 255)  # Pure white
    
    def apply_impulse(self, dx, dy):
        """Add velocity from a swipe."""
        self.vx += dx
        self.vy += dy
    
    def update(self, dt):
        """Update position based on velocity."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Screen wrapping
        if self.x - self.radius > self.screen_width:
            self.x = -self.radius
        elif self.x + self.radius < 0:
            self.x = self.screen_width + self.radius
            
        if self.y - self.radius > self.screen_height:
            self.y = -self.radius
        elif self.y + self.radius < 0:
            self.y = self.screen_height + self.radius
    
    def draw(self, screen):
        """Draw the player sphere."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def get_position(self):
        """Return current position as tuple."""
        return (self.x, self.y)
