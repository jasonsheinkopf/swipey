"""Keyboard handling for parameter adjustments."""
import pygame


class InputHandler:
    """Handles keyboard input for parameter adjustments."""
    
    def __init__(self, swipe_processor):
        self.swipe_processor = swipe_processor
        self.last_update_time = 0
        self.update_interval = 100  # milliseconds (0.1 seconds = 10 per second)
    
    def handle_event(self, event):
        """Process keyboard events."""
        # This is now just for compatibility, actual handling is in update()
        pass
    
    def update(self):
        """Update parameter values based on held keys."""
        current_time = pygame.time.get_ticks()
        
        # Check if enough time has passed since last update
        if current_time - self.last_update_time < self.update_interval:
            return
        
        keys = pygame.key.get_pressed()
        params = self.swipe_processor.get_parameters()
        changed = False
        
        # Strength controls: Q/A
        if keys[pygame.K_q]:
            self.swipe_processor.set_parameter('strength', params['strength'] + 1)
            changed = True
        elif keys[pygame.K_a]:
            self.swipe_processor.set_parameter('strength', params['strength'] - 1)
            changed = True
        
        # Focus controls: W/S
        if keys[pygame.K_w]:
            self.swipe_processor.set_parameter('focus', params['focus'] + 1)
            changed = True
        elif keys[pygame.K_s]:
            self.swipe_processor.set_parameter('focus', params['focus'] - 1)
            changed = True
        
        # Smoothness controls: E/D
        if keys[pygame.K_e]:
            self.swipe_processor.set_parameter('smoothness', params['smoothness'] + 1)
            changed = True
        elif keys[pygame.K_d]:
            self.swipe_processor.set_parameter('smoothness', params['smoothness'] - 1)
            changed = True
        
        # Update timer only if a key was pressed
        if changed:
            self.last_update_time = current_time
