"""Game state, collision detection, and score management."""
from player import Player
from collectible import Collectible
from swipe import SwipeProcessor
from input import InputHandler
from audio import AudioManager
from ui import UI
from stars import Starfield


class Game:
    """Main game state and logic."""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Game objects
        self.player = Player(screen_width, screen_height)
        self.collectible = Collectible(screen_width, screen_height, self.player.radius)
        self.swipe_processor = SwipeProcessor()
        self.input_handler = InputHandler(self.swipe_processor)
        self.audio_manager = AudioManager()
        self.ui = UI(screen_width, screen_height)
        self.starfield = Starfield(screen_width, screen_height)
        
        # Score
        self.score = 0
        
        # Spawn first collectible
        player_x, player_y = self.player.get_position()
        self.collectible.spawn(player_x, player_y)
    
    def handle_event(self, event):
        """Handle input events."""
        import pygame
        
        # Keyboard input for parameters
        self.input_handler.handle_event(event)
        
        # Mouse swipe input
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                x, y = event.pos
                self.swipe_processor.start_swipe(x, y)
        
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # Left button is held
                x, y = event.pos
                self.swipe_processor.add_point(x, y)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                impulse = self.swipe_processor.end_swipe()
                self.player.apply_impulse(impulse[0], impulse[1])
    
    def update(self, dt):
        """Update game state."""
        # Update player
        self.player.update(dt)
        
        # Update collectible animation
        self.collectible.update(dt)
        
        # Check collision
        player_x, player_y = self.player.get_position()
        if self.collectible.check_collision(player_x, player_y, self.player.radius):
            # Collected!
            self.score += 1
            self.audio_manager.play_collection_sound()
            self.collectible.spawn(player_x, player_y)
    
    def draw(self, screen, time_ms):
        """Draw everything."""
        # Background
        screen.fill((0, 0, 0))  # Pure black
        
        # Stars
        self.starfield.draw(screen, time_ms)
        
        # Collectible
        self.collectible.draw(screen)
        
        # Player
        self.player.draw(screen)
        
        # UI
        params = self.swipe_processor.get_parameters()
        self.ui.draw(screen, self.score, params)
    
    def cleanup(self):
        """Clean up resources."""
        self.audio_manager.cleanup()
