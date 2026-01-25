"""Asteroids that move across the screen as obstacles."""
import random
import pygame
import math


class Asteroid:
    """A rough-shaped grey asteroid obstacle."""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Random size
        self.radius = random.randint(25, 45)
        
        # Mass proportional to area (radius squared)
        self.mass = self.radius * self.radius
        
        # Generate rough shape (vertices around a circle with random offsets)
        self.num_vertices = random.randint(7, 10)
        self.vertex_offsets = []
        for i in range(self.num_vertices):
            # Random offset from base radius (0.7 to 1.3)
            offset = random.uniform(0.7, 1.3)
            self.vertex_offsets.append(offset)
        
        # Random position
        self.x = random.uniform(0, screen_width)
        self.y = random.uniform(0, screen_height)
        
        # Random constant velocity (slow drift)
        speed = random.uniform(30, 80)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        
        # Slight rotation
        self.rotation = random.uniform(0, 2 * math.pi)
        self.rotation_speed = random.uniform(-0.5, 0.5)
        
        # Grey color with slight variation
        grey = random.randint(80, 120)
        self.color = (grey, grey - 10, grey - 20)
        self.highlight_color = (grey + 30, grey + 20, grey + 10)
    
    def update(self, dt):
        """Update asteroid position and rotation."""
        # Move
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Rotate
        self.rotation += self.rotation_speed * dt
        
        # Screen wrapping (like player)
        if self.x - self.radius > self.screen_width:
            self.x = -self.radius
        elif self.x + self.radius < 0:
            self.x = self.screen_width + self.radius
            
        if self.y - self.radius > self.screen_height:
            self.y = -self.radius
        elif self.y + self.radius < 0:
            self.y = self.screen_height + self.radius
    
    def get_vertices(self):
        """Get the current vertex positions."""
        vertices = []
        for i in range(self.num_vertices):
            angle = self.rotation + (2 * math.pi * i / self.num_vertices)
            r = self.radius * self.vertex_offsets[i]
            x = self.x + r * math.cos(angle)
            y = self.y + r * math.sin(angle)
            vertices.append((x, y))
        return vertices
    
    def draw(self, screen):
        """Draw the asteroid."""
        vertices = self.get_vertices()
        
        # Draw main body
        pygame.draw.polygon(screen, self.color, vertices)
        
        # Draw outline for definition
        pygame.draw.polygon(screen, self.highlight_color, vertices, 2)
        
        # Add some crater-like details
        crater_x = self.x + self.radius * 0.2 * math.cos(self.rotation)
        crater_y = self.y + self.radius * 0.2 * math.sin(self.rotation)
        crater_r = self.radius * 0.2
        darker = (self.color[0] - 20, self.color[1] - 20, self.color[2] - 20)
        pygame.draw.circle(screen, darker, (int(crater_x), int(crater_y)), int(crater_r))
    
    def check_collision(self, player_x, player_y, player_radius):
        """Check if player collides with asteroid."""
        dx = self.x - player_x
        dy = self.y - player_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Use slightly smaller collision radius for fairness
        return distance < (self.radius * 0.8 + player_radius)
    
    def get_position(self):
        """Return current position as tuple."""
        return (self.x, self.y)


class AsteroidField:
    """Manages multiple asteroids."""
    
    def __init__(self, screen_width, screen_height, count=3):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.asteroids = []
        
        for _ in range(count):
            self.asteroids.append(Asteroid(screen_width, screen_height))
    
    def update(self, dt):
        """Update all asteroids and handle collisions between them."""
        # Update positions
        for asteroid in self.asteroids:
            asteroid.update(dt)
        
        # Check and resolve collisions between asteroids
        self._resolve_asteroid_collisions()
    
    def _resolve_asteroid_collisions(self):
        """Check for and resolve collisions between asteroids using elastic collision."""
        for i in range(len(self.asteroids)):
            for j in range(i + 1, len(self.asteroids)):
                a1 = self.asteroids[i]
                a2 = self.asteroids[j]
                
                # Calculate distance between centers
                dx = a2.x - a1.x
                dy = a2.y - a1.y
                distance = math.sqrt(dx * dx + dy * dy)
                
                # Check if colliding
                min_dist = a1.radius + a2.radius
                if distance < min_dist and distance > 0:
                    # Normalize collision vector
                    nx = dx / distance
                    ny = dy / distance
                    
                    # Relative velocity
                    dvx = a1.vx - a2.vx
                    dvy = a1.vy - a2.vy
                    
                    # Relative velocity along collision normal
                    dvn = dvx * nx + dvy * ny
                    
                    # Only resolve if asteroids are moving toward each other
                    if dvn > 0:
                        # Calculate impulse (elastic collision)
                        # Using conservation of momentum and kinetic energy
                        # impulse = 2 * m1 * m2 / (m1 + m2) * dvn
                        total_mass = a1.mass + a2.mass
                        impulse = 2 * dvn / total_mass
                        
                        # Apply impulse to velocities (weighted by mass)
                        a1.vx -= impulse * a2.mass * nx
                        a1.vy -= impulse * a2.mass * ny
                        a2.vx += impulse * a1.mass * nx
                        a2.vy += impulse * a1.mass * ny
                        
                        # Add some spin on collision
                        a1.rotation_speed += random.uniform(-0.3, 0.3)
                        a2.rotation_speed += random.uniform(-0.3, 0.3)
                    
                    # Separate overlapping asteroids
                    overlap = min_dist - distance
                    separation = overlap / 2 + 1
                    a1.x -= nx * separation
                    a1.y -= ny * separation
                    a2.x += nx * separation
                    a2.y += ny * separation
    
    def draw(self, screen):
        """Draw all asteroids."""
        for asteroid in self.asteroids:
            asteroid.draw(screen)
    
    def check_collision(self, player_x, player_y, player_radius):
        """Check if player collides with any asteroid."""
        for asteroid in self.asteroids:
            if asteroid.check_collision(player_x, player_y, player_radius):
                return True
        return False
    
    def get_asteroids(self):
        """Return list of asteroids for spawn avoidance."""
        return self.asteroids
    
    def respawn_away_from(self, x, y, min_distance):
        """Respawn all asteroids away from a point (e.g., after player death)."""
        for asteroid in self.asteroids:
            attempts = 0
            while attempts < 50:
                asteroid.x = random.uniform(0, self.screen_width)
                asteroid.y = random.uniform(0, self.screen_height)
                
                dx = asteroid.x - x
                dy = asteroid.y - y
                dist = math.sqrt(dx * dx + dy * dy)
                
                if dist > min_distance:
                    break
                attempts += 1