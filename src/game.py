"""Game state, collision detection, and score management."""
import pygame
import math
from player import Player
from collectible import Collectible
from swipe import SwipeProcessor
from input import InputHandler
from audio import AudioManager
from ui import UI
from stars import Starfield
from asteroid import AsteroidField


class Game:
    """Main game state and logic."""
    
    def __init__(self, screen_width, screen_height, dev_mode=False):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.dev_mode = dev_mode
        self.round_duration = 10.0 if dev_mode else 60.0
        
        # Game objects
        self.player = Player(screen_width, screen_height)
        self.collectible = Collectible(screen_width, screen_height, self.player.radius)
        self.swipe_processor = SwipeProcessor()
        self.input_handler = InputHandler(self.swipe_processor)
        self.audio_manager = AudioManager()
        self.ui = UI(screen_width, screen_height)
        self.starfield = Starfield(screen_width, screen_height)
        self.asteroid_field = AsteroidField(screen_width, screen_height, count=3)
        
        # Score
        self.score = 0
        self.level = 0
        self.targets_per_level = 5
        self.level_targets_collected = 0
        
        # Timer (60 seconds per round, or 10 in dev mode)
        self.time_remaining = self.round_duration
        
        # Game state: 'title', 'playing', 'transition'
        self.game_state = 'title'
        self.title_start_time = None
        
        # Continuous thrust state
        self.is_thrusting = False
        self.current_thrust = (0, 0)  # Current frame's thrust vector
        self.thrust_history = []  # Recent thrust directions for smoothing
        
        # Mouse capture state (start visible for title screen)
        self.mouse_captured = False
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        
        # Spawn first collectible (avoiding asteroids)
        player_x, player_y = self.player.get_position()
        self.collectible.spawn(player_x, player_y, self.asteroid_field.get_asteroids())
    
    def handle_event(self, event):
        """Handle input events."""
        # Title screen - auto-advance after 1 second
        if self.game_state == 'title':
            return
        
        # Handle transition screen clicks
        if self.game_state == 'transition' and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                result = self.ui.check_transition_click(event.pos)
                if result:
                    param_name, delta = result
                    params = self.swipe_processor.get_parameters()
                    new_value = params[param_name] + delta
                    self.swipe_processor.set_parameter(param_name, new_value)
                    # Start new round
                    self.game_state = 'playing'
                    self.time_remaining = self.round_duration
                    self.level_targets_collected = 0
                    # Reset player velocity
                    self.player.vx = 0
                    self.player.vy = 0
                    # Hide mouse and capture
                    self.mouse_captured = True
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
            return
        
        # Escape key to toggle mouse capture
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.mouse_captured = not self.mouse_captured
                pygame.mouse.set_visible(not self.mouse_captured)
                pygame.event.set_grab(self.mouse_captured)
                return
        
        # Keyboard input for parameters
        self.input_handler.handle_event(event)
        
        # Continuous thrust from mouse motion
        if event.type == pygame.MOUSEMOTION:
            rel_x, rel_y = event.rel
            
            # Only thrust if there's actual movement
            if rel_x != 0 or rel_y != 0:
                self.is_thrusting = True
                
                # Add to history
                self.thrust_history.append((rel_x, rel_y))
                
                # Get smoothness parameter (1-10 maps to 10-100 samples to average)
                params = self.swipe_processor.get_parameters()
                smooth_samples = params['smoothness'] * 10
                smooth_count = max(1, min(smooth_samples, len(self.thrust_history)))
                
                # Average over the last 'smooth_count' samples
                recent = self.thrust_history[-smooth_count:]
                avg_dx = sum(t[0] for t in recent) / len(recent)
                avg_dy = sum(t[1] for t in recent) / len(recent)
                
                # Apply strength multiplier (0.1x to 1.0x)
                multiplier = 0.1 + (params['strength'] / 10) * 0.9
                
                # Scale down for continuous application
                continuous_scale = 0.5
                
                self.current_thrust = (avg_dx * multiplier * continuous_scale, 
                                       avg_dy * multiplier * continuous_scale)
                
                # Keep history reasonable size (up to 100 for max smoothness)
                if len(self.thrust_history) > 100:
                    self.thrust_history = self.thrust_history[-100:]
    
    def update(self, dt):
        """Update game state."""
        # Title screen - auto-advance after 1 second
        if self.game_state == 'title':
            if self.title_start_time is None:
                self.title_start_time = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.title_start_time > 1000:
                # Advance to playing
                self.game_state = 'playing'
                self.level = 1
                self.time_remaining = self.round_duration
                # Reset player velocity
                self.player.vx = 0
                self.player.vy = 0
                # Hide mouse and capture
                self.mouse_captured = True
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)
            return
        
        # Skip game updates during transition screen
        if self.game_state == 'transition':
            return
        
        # Update input handler for key holding
        self.input_handler.update()
        
        # Update timer
        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.time_remaining = 0
            # Round over - go to transition screen
            self.game_state = 'transition'
            self.level += 1
            # Show mouse for transition screen
            self.mouse_captured = False
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
            return
        
        # Apply continuous thrust
        if self.is_thrusting and (self.current_thrust[0] != 0 or self.current_thrust[1] != 0):
            self.player.apply_impulse(self.current_thrust[0], self.current_thrust[1])
        
        # Reset thrust state - will be set again on next mouse motion
        # Clear thrust so flame disappears when not actively thrusting
        if not self.is_thrusting:
            self.current_thrust = (0, 0)
            self.thrust_history = []
        self.is_thrusting = False
        
        # Update player
        self.player.update(dt)
        
        # Update asteroids
        self.asteroid_field.update(dt)
        
        # Update collectible animation
        self.collectible.update(dt)
        
        # Check collision with collectible
        player_x, player_y = self.player.get_position()
        if self.collectible.check_collision(player_x, player_y, self.player.radius):
            # Collected!
            self.score += 1
            self.level_targets_collected += 1
            self.audio_manager.play_collection_sound()
            self.collectible.spawn(player_x, player_y, self.asteroid_field.get_asteroids())
        
        # Check collision with asteroids
        if self.asteroid_field.check_collision(player_x, player_y, self.player.radius):
            # Hit asteroid - reset player and lose points
            self.player.reset()
            self.score = max(0, self.score - 1)
            # Respawn asteroids away from player
            new_x, new_y = self.player.get_position()
            self.asteroid_field.respawn_away_from(new_x, new_y, 150)
    
    def _get_flame_colors(self, magnitude):
        """Get flame colors based on magnitude (energy). Blue=weak, Yellow=medium, Red=strong."""
        # Normalize magnitude to 0-1 range (assuming max useful magnitude around 15)
        t = min(1.0, magnitude / 15.0)
        
        if t < 0.5:
            # Blue to Yellow (low to medium energy)
            # Blue: (100, 150, 255) -> Yellow: (255, 255, 0)
            inner_t = t * 2  # 0 to 1 within this range
            outer = (int(100 + 155 * inner_t), int(150 + 105 * inner_t), int(255 - 255 * inner_t))
            middle = (int(150 + 105 * inner_t), int(200 + 55 * inner_t), int(255 - 205 * inner_t))
            core = (int(200 + 55 * inner_t), int(250 + 5 * inner_t), int(255 - 155 * inner_t))
        else:
            # Yellow to Red (medium to high energy)
            # Yellow: (255, 255, 0) -> Red: (255, 50, 0)
            inner_t = (t - 0.5) * 2  # 0 to 1 within this range
            outer = (255, int(255 - 205 * inner_t), 0)
            middle = (255, int(255 - 105 * inner_t), int(50 - 50 * inner_t))
            core = (255, int(255 - 55 * inner_t), int(100 - 100 * inner_t))
        
        return outer, middle, core
    
    def _draw_thrust(self, screen, ball_x, ball_y, dx, dy, ball_radius):
        """Draw a rocket thrust flame behind the ball, pointing in thrust direction."""
        magnitude = math.sqrt(dx * dx + dy * dy)
        
        if magnitude < 0.1:
            return
        
        # Normalize direction (thrust points in direction of motion)
        norm_dx = dx / magnitude
        norm_dy = dy / magnitude
        
        # Thrust comes from behind the ball (opposite to motion direction)
        # Tip of flame is at ball edge, base extends backward
        tip_x = ball_x - norm_dx * ball_radius
        tip_y = ball_y - norm_dy * ball_radius
        
        # Thrust length based on magnitude
        thrust_length = min(100, max(15, magnitude * 8))
        
        # Base of flame (behind the ball)
        base_x = tip_x - norm_dx * thrust_length
        base_y = tip_y - norm_dy * thrust_length
        base_width = min(20, thrust_length * 0.5)
        
        # Perpendicular vector for width
        perp_x = -norm_dy
        perp_y = norm_dx
        
        # Get colors based on magnitude (energy level)
        outer_color, middle_color, core_color = self._get_flame_colors(magnitude)
        
        # Outer flame
        pygame.draw.polygon(screen, outer_color, [
            (base_x + perp_x * base_width / 2, base_y + perp_y * base_width / 2),
            (base_x - perp_x * base_width / 2, base_y - perp_y * base_width / 2),
            (tip_x, tip_y)
        ])
        
        # Middle flame
        inner_width = base_width * 0.6
        inner_base_x = base_x + norm_dx * thrust_length * 0.15
        inner_base_y = base_y + norm_dy * thrust_length * 0.15
        pygame.draw.polygon(screen, middle_color, [
            (inner_base_x + perp_x * inner_width / 2, inner_base_y + perp_y * inner_width / 2),
            (inner_base_x - perp_x * inner_width / 2, inner_base_y - perp_y * inner_width / 2),
            (tip_x, tip_y)
        ])
        
        # Hot core
        core_width = base_width * 0.25
        core_base_x = base_x + norm_dx * thrust_length * 0.3
        core_base_y = base_y + norm_dy * thrust_length * 0.3
        core_tip_x = base_x + norm_dx * thrust_length * 0.75
        core_tip_y = base_y + norm_dy * thrust_length * 0.75
        pygame.draw.polygon(screen, core_color, [
            (core_base_x + perp_x * core_width / 2, core_base_y + perp_y * core_width / 2),
            (core_base_x - perp_x * core_width / 2, core_base_y - perp_y * core_width / 2),
            (core_tip_x, core_tip_y)
        ])
    
    def draw(self, screen, time_ms):
        """Draw everything."""
        # Background
        screen.fill((0, 0, 0))  # Pure black
        
        # Title screen
        if self.game_state == 'title':
            self.ui.draw_title_screen(screen)
            return
        
        # If in transition, show transition screen
        if self.game_state == 'transition':
            params = self.swipe_processor.get_parameters()
            self.ui.draw_level_transition(screen, self.level - 1, params)
            return
        
        # Stars
        self.starfield.draw(screen, time_ms)
        
        # Asteroids
        self.asteroid_field.draw(screen)
        
        # Collectible
        self.collectible.draw(screen)
        
        # Get player position
        player_x, player_y = self.player.get_position()
        
        # Draw thrust flame (behind ball, while thrusting)
        if self.current_thrust[0] != 0 or self.current_thrust[1] != 0:
            self._draw_thrust(screen, player_x, player_y, 
                            self.current_thrust[0], self.current_thrust[1],
                            self.player.radius)
        
        # Player (draw after thrust so ball is on top)
        self.player.draw(screen)
        
        # UI
        params = self.swipe_processor.get_parameters()
        self.ui.draw(screen, self.score, self.time_remaining, params)
    
    def cleanup(self):
        """Clean up resources."""
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        self.audio_manager.cleanup()