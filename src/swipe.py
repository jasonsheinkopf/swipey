"""Swipe capture and processing with configurable parameters."""
import math


class SwipeProcessor:
    """Processes swipe input through Focus, Smoothness, and Strength filters."""
    
    def __init__(self):
        # Parameters range from 1-10
        self.strength = 5
        self.focus = 5
        self.smoothness = 5
        
        # Swipe data
        self.points = []
        self.is_swiping = False
        
    def start_swipe(self, x, y):
        """Begin capturing a swipe."""
        self.is_swiping = True
        self.points = [(x, y)]
    
    def add_point(self, x, y):
        """Add a point to the current swipe."""
        if self.is_swiping:
            self.points.append((x, y))
    
    def end_swipe(self):
        """Complete the swipe and calculate impulse."""
        if not self.is_swiping or len(self.points) < 2:
            self.is_swiping = False
            return (0, 0)
        
        self.is_swiping = False
        
        # Step 1: Focus Filter - select portion of swipe
        focused_points = self._apply_focus()
        
        if len(focused_points) < 2:
            return (0, 0)
        
        # Step 2: Smoothness - average direction vectors
        direction = self._apply_smoothness(focused_points)
        
        # Step 3: Strength - scale the magnitude
        impulse = self._apply_strength(direction)
        
        return impulse
    
    def _apply_focus(self):
        """Select which portion of the swipe to use based on focus parameter."""
        if len(self.points) < 2:
            return self.points
        
        # Focus 1 = last 10% of swipe
        # Focus 10 = entire swipe (100%)
        portion = 0.1 + (self.focus - 1) * 0.1  # 0.1 to 1.0
        
        count = max(2, int(len(self.points) * portion))
        return self.points[-count:]
    
    def _apply_smoothness(self, points):
        """Average direction vectors based on smoothness parameter."""
        if len(points) < 2:
            return (0, 0)
        
        # Smoothness 1 = only last segment
        # Smoothness 10 = average all segments
        segments_to_use = max(1, int((len(points) - 1) * (self.smoothness / 10)))
        
        # Calculate direction vectors for the last N segments
        dx_sum = 0
        dy_sum = 0
        count = 0
        
        start_idx = len(points) - 1 - segments_to_use
        start_idx = max(0, start_idx)
        
        for i in range(start_idx, len(points) - 1):
            dx = points[i + 1][0] - points[i][0]
            dy = points[i + 1][1] - points[i][1]
            dx_sum += dx
            dy_sum += dy
            count += 1
        
        if count == 0:
            # Fallback to first and last point
            dx_sum = points[-1][0] - points[0][0]
            dy_sum = points[-1][1] - points[0][1]
            count = 1
        
        # Average
        avg_dx = dx_sum / count
        avg_dy = dy_sum / count
        
        return (avg_dx, avg_dy)
    
    def _apply_strength(self, direction):
        """Scale the magnitude based on strength parameter."""
        dx, dy = direction
        
        # Strength 1 = 0.1x multiplier (gentle nudge)
        # Strength 10 = 1.0x multiplier (powerful thrust)
        multiplier = 0.1 + (self.strength - 1) * 0.1
        
        # Scale for 60 FPS and pixel/second velocity
        scale = 0.01 * multiplier
        
        return (dx * scale, dy * scale)
    
    def set_parameter(self, param_name, value):
        """Set a parameter value (1-10)."""
        value = max(1, min(10, value))
        
        if param_name == 'strength':
            self.strength = value
        elif param_name == 'focus':
            self.focus = value
        elif param_name == 'smoothness':
            self.smoothness = value
    
    def get_parameters(self):
        """Return current parameter values."""
        return {
            'strength': self.strength,
            'focus': self.focus,
            'smoothness': self.smoothness
        }
