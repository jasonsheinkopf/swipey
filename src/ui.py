"""UI display for score and parameters."""
import pygame


class UI:
    """Renders the game UI."""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Font
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 24)
        
        # UI color: white with slight transparency
        self.color = (255, 255, 255)
        self.alpha = 204  # 0.8 * 255
    
    def draw(self, screen, score, params):
        """Draw the UI elements."""
        # Score in top-left
        score_text = f"Score: {score}"
        score_surface = self.font_large.render(score_text, True, self.color)
        score_surface.set_alpha(self.alpha)
        screen.blit(score_surface, (20, 20))
        
        # Parameters in top-right
        param_y = 20
        
        strength_text = f"Strength: {params['strength']}/10 (Q/A)"
        strength_surface = self.font_small.render(strength_text, True, self.color)
        strength_surface.set_alpha(self.alpha)
        text_width = strength_surface.get_width()
        screen.blit(strength_surface, (self.screen_width - text_width - 20, param_y))
        param_y += 30
        
        focus_text = f"Focus: {params['focus']}/10 (W/S)"
        focus_surface = self.font_small.render(focus_text, True, self.color)
        focus_surface.set_alpha(self.alpha)
        text_width = focus_surface.get_width()
        screen.blit(focus_surface, (self.screen_width - text_width - 20, param_y))
        param_y += 30
        
        smoothness_text = f"Smoothness: {params['smoothness']}/10 (E/D)"
        smoothness_surface = self.font_small.render(smoothness_text, True, self.color)
        smoothness_surface.set_alpha(self.alpha)
        text_width = smoothness_surface.get_width()
        screen.blit(smoothness_surface, (self.screen_width - text_width - 20, param_y))
        
        # Instructions at bottom
        instructions = "Swipe with mouse to move | Collect the pulsing target"
        instr_surface = self.font_small.render(instructions, True, self.color)
        instr_surface.set_alpha(self.alpha)
        text_width = instr_surface.get_width()
        screen.blit(instr_surface, ((self.screen_width - text_width) // 2, self.screen_height - 40))
