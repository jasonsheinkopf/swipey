"""Procedural sound generation using pygame.mixer."""
import pygame
import numpy as np


class AudioManager:
    """Generates and plays procedural audio."""
    
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        self.sample_rate = 22050
        
    def play_collection_sound(self):
        """Play the collection sound effect."""
        duration = 0.15  # 150ms
        frequency = 800  # Hz
        
        # Generate samples
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples, False)
        
        # Sine wave
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Envelope: quick attack, medium decay
        envelope = np.exp(-t * 8)  # Exponential decay
        
        # Apply envelope
        wave = wave * envelope
        
        # Add slight pitch bend up
        bend_factor = 1 + 0.2 * t / duration
        bent_wave = np.sin(2 * np.pi * frequency * t * bend_factor)
        wave = bent_wave * envelope
        
        # Convert to 16-bit integer
        wave = (wave * 32767).astype(np.int16)
        
        # Create sound
        sound = pygame.sndarray.make_sound(wave)
        sound.play()
    
    def cleanup(self):
        """Clean up audio resources."""
        pygame.mixer.quit()
