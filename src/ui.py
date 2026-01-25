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
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # UI color: white with slight transparency
        self.color = (255, 255, 255)
        self.alpha = 204  # 0.8 * 255
        
        # Level transition clickable buttons
        self.transition_buttons = []
    
    def draw(self, screen, score, time_remaining, params):
        """Draw the UI elements."""
        # Score in top-left
        score_text = f"Score: {score}"
        score_surface = self.font_large.render(score_text, True, self.color)
        score_surface.set_alpha(self.alpha)
        screen.blit(score_surface, (20, 20))
        
        # Timer in top-right
        timer_text = f"{int(time_remaining)}s"
        timer_color = (255, 100, 100) if time_remaining < 10 else self.color
        timer_surface = self.font_large.render(timer_text, True, timer_color)
        timer_surface.set_alpha(self.alpha)
        timer_width = timer_surface.get_width()
        screen.blit(timer_surface, (self.screen_width - timer_width - 20, 20))
    
    def draw_title_screen(self, screen):
        """Draw the title screen."""
        # Background
        screen.fill((0, 0, 0))
        
        # Title: SWIPEY
        title = "SWIPEY"
        title_surface = pygame.font.Font(None, 96).render(title, True, (100, 150, 255))
        title_width = title_surface.get_width()
        screen.blit(title_surface, ((self.screen_width - title_width) // 2, 200))
        
        # Tagline
        tagline = "The parameter optimization simulator"
        tagline_surface = self.font_medium.render(tagline, True, (180, 180, 180))
        tagline_width = tagline_surface.get_width()
        screen.blit(tagline_surface, ((self.screen_width - tagline_width) // 2, 300))
        
        # Swipe visual
        swipe_center_x = self.screen_width // 2
        swipe_center_y = 420
        swipe_points = [
            (swipe_center_x - 100, swipe_center_y + 40),
            (swipe_center_x - 50, swipe_center_y - 20),
            (swipe_center_x, swipe_center_y - 40),
            (swipe_center_x + 50, swipe_center_y - 30),
            (swipe_center_x + 100, swipe_center_y + 10)
        ]
        pygame.draw.lines(screen, (100, 200, 255), False, swipe_points, 5)
        # Arrow at end
        pygame.draw.polygon(screen, (100, 200, 255), [
            (swipe_center_x + 100, swipe_center_y + 10),
            (swipe_center_x + 90, swipe_center_y),
            (swipe_center_x + 85, swipe_center_y + 15)
        ])
    
    def draw_level_transition(self, screen, level, params):
        """Draw the level transition screen with parameter adjustment options."""
        # Semi-transparent dark background
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(240)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Title
        if level == 0:
            title = "ROUND 1 STARTING"
        else:
            title = f"ROUND {level} COMPLETE!"
        title_surface = self.font_large.render(title, True, (100, 150, 255))
        title_width = title_surface.get_width()
        screen.blit(title_surface, ((self.screen_width - title_width) // 2, 40))
        
        # Store buttons for click detection
        self.transition_buttons = []
        
        # Draw each parameter with -1 and +1 buttons (only strength and smoothness)
        param_names = ['strength', 'smoothness']
        
        # Center the parameters vertically and horizontally
        param_row_height = 120
        total_height = len(param_names) * param_row_height
        y_start_centered = (self.screen_height - total_height) // 2
        
        # Subtitle positioned just above choices
        subtitle = "Choose one parameter adjustment"
        subtitle_surface = self.font_medium.render(subtitle, True, (200, 200, 200))
        subtitle_width = subtitle_surface.get_width()
        screen.blit(subtitle_surface, ((self.screen_width - subtitle_width) // 2, y_start_centered - 50))
        
        # All buttons same width
        button_width = 100
        button_spacing = 60  # Gap between left and right buttons
        
        for i, param_name in enumerate(param_names):
            y = y_start_centered + i * param_row_height
            current_value = params[param_name]
            
            # Center X position
            center_x = self.screen_width // 2
            
            # Set labels
            if i == 0:  # Strength
                minus_text_label = "WEAK"
                plus_text_label = "STRONG"
            else:  # Smoothness
                minus_text_label = "ROUGH"
                plus_text_label = "SMOOTH"
            
            # LEFT: -1 button
            minus_button = pygame.Rect(center_x - button_spacing // 2 - button_width, y + 15, button_width, 30)
            minus_color = (150, 50, 50) if current_value > 0 else (80, 30, 30)
            pygame.draw.rect(screen, minus_color, minus_button)
            pygame.draw.rect(screen, (255, 255, 255), minus_button, 2)
            minus_text = self.font_small.render(minus_text_label, True, (255, 255, 255))
            minus_text_rect = minus_text.get_rect(center=minus_button.center)
            screen.blit(minus_text, minus_text_rect)
            if current_value > 0:
                self.transition_buttons.append((minus_button, param_name, -1))
            
            # LEFT visual (further left from button)
            minus_visual_x = minus_button.left - 80
            if i == 0:  # Strength
                self._draw_strength_visual(screen, minus_visual_x, y, less=True)
            else:  # Smoothness
                self._draw_smoothness_visual(screen, minus_visual_x, y, less=True)
            
            # CENTER: Don't show the number (but still track it)
            # (removed the display code)
            
            # RIGHT: +1 button
            plus_button = pygame.Rect(center_x + button_spacing // 2, y + 15, button_width, 30)
            plus_color = (50, 150, 50) if current_value < 10 else (30, 80, 30)
            pygame.draw.rect(screen, plus_color, plus_button)
            pygame.draw.rect(screen, (255, 255, 255), plus_button, 2)
            plus_text = self.font_small.render(plus_text_label, True, (255, 255, 255))
            plus_text_rect = plus_text.get_rect(center=plus_button.center)
            screen.blit(plus_text, plus_text_rect)
            if current_value < 10:
                self.transition_buttons.append((plus_button, param_name, +1))
            
            # RIGHT visual (further right from button)
            plus_visual_x = plus_button.right + 20
            if i == 0:  # Strength
                self._draw_strength_visual(screen, plus_visual_x, y, less=False)
            else:  # Smoothness
                self._draw_smoothness_visual(screen, plus_visual_x, y, less=False)
        
        # Instructions at bottom
        instr_text = "Click a button to adjust and continue"
        instr_surface = self.font_small.render(instr_text, True, (200, 200, 200))
        instr_width = instr_surface.get_width()
        screen.blit(instr_surface, ((self.screen_width - instr_width) // 2, self.screen_height - 60))
    
    def check_transition_click(self, pos):
        """Check if a click hit any transition button. Returns (param_name, delta) or None."""
        for button_rect, param_name, delta in self.transition_buttons:
            if button_rect.collidepoint(pos):
                return (param_name, delta)
        return None
    
    def _draw_strength_visual(self, screen, x, y, less):
        """Draw strength parameter visual."""
        # Player circle (blue like in game) - use actual game radius (3% of screen width)
        player_radius = int(self.screen_width * 0.03)
        player_x = x + player_radius + 5
        player_y = y + 30
        pygame.draw.circle(screen, (100, 150, 255), (player_x, player_y), player_radius)
        
        # Triangular thruster flame
        if less:
            # Small thruster (weak) - points left
            thrust_length = 15
            base_width = 8
            direction = -1  # Left
            
            # Tip at ball edge pointing left
            tip_x = player_x - player_radius
            tip_y = player_y
            
            # Base extends backward (to the left)
            base_x = tip_x - thrust_length
        else:
            # Large thruster (strong) - points right, much bigger
            thrust_length = 70  # Double the original 35
            base_width = 36  # Double the original 18
            direction = 1  # Right
            
            # Tip at ball edge pointing right
            tip_x = player_x + player_radius
            tip_y = player_y
            
            # Base extends backward (to the right)
            base_x = tip_x + thrust_length
        
        # Get color based on magnitude using game's color map
        outer_color, middle_color, core_color = self._get_flame_colors(thrust_length)
        
        # Triangular flame
        pygame.draw.polygon(screen, outer_color, [
            (base_x, tip_y + base_width / 2),
            (base_x, tip_y - base_width / 2),
            (tip_x, tip_y)
        ])
    
    def _get_flame_colors(self, magnitude):
        """Get flame colors based on magnitude (energy). Blue=weak, Yellow=medium, Red=strong."""
        # Normalize magnitude to 0-1 range (assuming max useful magnitude around 15)
        t = min(1.0, magnitude / 15.0)
        
        if t < 0.5:
            # Blue to Yellow (low to medium energy)
            inner_t = t * 2
            outer = (int(100 + 155 * inner_t), int(150 + 105 * inner_t), int(255 - 255 * inner_t))
            middle = (int(150 + 105 * inner_t), int(200 + 55 * inner_t), int(255 - 205 * inner_t))
            core = (int(200 + 55 * inner_t), int(250 + 5 * inner_t), int(255 - 155 * inner_t))
        else:
            # Yellow to Red (medium to high energy)
            inner_t = (t - 0.5) * 2
            outer = (255, int(255 - 205 * inner_t), 0)
            middle = (255, int(255 - 105 * inner_t), int(50 - 50 * inner_t))
            core = (255, int(255 - 55 * inner_t), int(100 - 100 * inner_t))
        
        return outer, middle, core
    
    def _draw_smoothness_visual(self, screen, x, y, less):
        """Draw smoothness parameter visual."""
        # Player circle (blue like in game) - use actual game radius (3% of screen width)
        player_radius = int(self.screen_width * 0.03)
        player_x = x + player_radius + 5
        player_y = y + 30
        pygame.draw.circle(screen, (100, 150, 255), (player_x, player_y), player_radius)
        
        import math
        if less:
            # Several medium flames spread around 9 o'clock (rough) - pointing left
            angles = [math.pi * 0.9, math.pi, math.pi * 1.1]  # Top, middle, bottom around left
            thrust_length = 20
            base_width = 10
            # Alpha values: top (most reduced), middle (some reduction), bottom (full)
            alphas = [80, 180, 255]  # Top faded most, middle less, bottom full
            
            for i, (angle, alpha) in enumerate(zip(angles, alphas)):
                # Tip at ball edge
                tip_x = player_x + int(player_radius * math.cos(angle))
                tip_y = player_y + int(player_radius * math.sin(angle))
                
                # Base extends backward
                base_x = tip_x + int(thrust_length * math.cos(angle))
                base_y = tip_y + int(thrust_length * math.sin(angle))
                
                # Perpendicular for width
                perp_x = -math.sin(angle)
                perp_y = math.cos(angle)
                
                # Get color and apply alpha
                outer_color, _, _ = self._get_flame_colors(thrust_length)
                
                # Create surface with alpha for this thruster
                temp_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                flame_color_with_alpha = outer_color + (alpha,)
                pygame.draw.polygon(temp_surface, flame_color_with_alpha, [
                    (base_x + perp_x * base_width / 2, base_y + perp_y * base_width / 2),
                    (base_x - perp_x * base_width / 2, base_y - perp_y * base_width / 2),
                    (tip_x, tip_y)
                ])
                screen.blit(temp_surface, (0, 0))
        else:
            # Single unified flame exactly to the right (smooth) - pointing right
            thrust_length = 30
            base_width = 15
            
            # Tip at ball edge pointing right
            tip_x = player_x + player_radius
            tip_y = player_y
            
            # Base extends backward (to the right)
            base_x = tip_x + thrust_length
            
            # Get color based on magnitude
            outer_color, _, _ = self._get_flame_colors(thrust_length)
            
            # Triangular flame
            pygame.draw.polygon(screen, outer_color, [
                (base_x, tip_y + base_width / 2),
                (base_x, tip_y - base_width / 2),
                (tip_x, tip_y)
            ])
    
    def _draw_tutorial(self, screen):
        """Draw the tutorial overlay with parameter explanations."""
        # Semi-transparent dark background
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(230)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Title
        title = "SWIPE PARAMETERS GUIDE"
        title_surface = self.font_large.render(title, True, (100, 150, 255))
        title_width = title_surface.get_width()
        screen.blit(title_surface, ((self.screen_width - title_width) // 2, 40))
        
        # Starting Y position for content
        y_start = 120
        x_margin = 80
        section_spacing = 180
        
        # 1. STRENGTH (Q/A)
        self._draw_parameter_demo(screen, x_margin, y_start, 
                                  "STRENGTH (Q/A)", 
                                  "Controls force multiplier",
                                  ["Low: gentle nudge", "High: powerful thrust"],
                                  self._draw_strength_visual)
        
        # 2. FOCUS (W/S)
        self._draw_parameter_demo(screen, x_margin, y_start + section_spacing,
                                  "FOCUS (W/S)",
                                  "Which part of swipe to use",
                                  ["Low: last 10% of swipe", "High: entire swipe path"],
                                  self._draw_focus_visual)
        
        # 3. SMOOTHNESS (E/D)
        self._draw_parameter_demo(screen, x_margin, y_start + section_spacing * 2,
                                  "SMOOTHNESS (E/D)",
                                  "Direction averaging",
                                  ["Low: final flick only", "High: average all motion"],
                                  self._draw_smoothness_visual)
        
        # Bottom instructions
        dismiss_text = "Press SPACE to start playing"
        dismiss_surface = self.font_medium.render(dismiss_text, True, (255, 255, 100))
        dismiss_width = dismiss_surface.get_width()
        screen.blit(dismiss_surface, ((self.screen_width - dismiss_width) // 2, self.screen_height - 60))
    
    def _draw_parameter_demo(self, screen, x, y, title, description, details, visual_func):
        """Draw a parameter explanation section."""
        # Title
        title_surface = self.font_medium.render(title, True, (255, 200, 100))
        screen.blit(title_surface, (x, y))
        
        # Description
        desc_surface = self.font_small.render(description, True, (200, 200, 200))
        screen.blit(desc_surface, (x, y + 35))
        
        # Details
        detail_y = y + 65
        for detail in details:
            detail_surface = self.font_small.render(detail, True, (180, 180, 180))
            screen.blit(detail_surface, (x, detail_y))
            detail_y += 25
        
        # Visual demonstration
        visual_x = x + 450
        visual_func(screen, visual_x, y + 20)
    
    def dismiss_tutorial(self):
        """Hide the tutorial overlay."""
        self.show_tutorial = False

