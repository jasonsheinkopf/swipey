"""Keyboard handling for parameter adjustments."""
import pygame
import time


class InputHandler:
    """Handles keyboard input for parameter adjustments."""
    
    def __init__(self, swipe_processor):
        self.swipe_processor = swipe_processor
        
        # Rate limiting: 0.5 seconds between changes
        self.last_change_time = 0
        self.change_cooldown = 0.5
    
    def handle_event(self, event):
        """Process keyboard events."""
        if event.type != pygame.KEYDOWN:
            return
        
        current_time = time.time()
        if current_time - self.last_change_time < self.change_cooldown:
            return  # Rate limited
        
        params = self.swipe_processor.get_parameters()
        
        # Strength controls: Q/A
        if event.key == pygame.K_q:
            self.swipe_processor.set_parameter('strength', params['strength'] + 1)
            self.last_change_time = current_time
        elif event.key == pygame.K_a:
            self.swipe_processor.set_parameter('strength', params['strength'] - 1)
            self.last_change_time = current_time
        
        # Focus controls: W/S
        elif event.key == pygame.K_w:
            self.swipe_processor.set_parameter('focus', params['focus'] + 1)
            self.last_change_time = current_time
        elif event.key == pygame.K_s:
            self.swipe_processor.set_parameter('focus', params['focus'] - 1)
            self.last_change_time = current_time
        
        # Smoothness controls: E/D
        elif event.key == pygame.K_e:
            self.swipe_processor.set_parameter('smoothness', params['smoothness'] + 1)
            self.last_change_time = current_time
        elif event.key == pygame.K_d:
            self.swipe_processor.set_parameter('smoothness', params['smoothness'] - 1)
            self.last_change_time = current_time
