"""Entry point and game loop for Drift."""
import pygame
import sys
import argparse
from game import Game


def main():
    """Main entry point."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Swipey - The parameter optimization simulator')
    parser.add_argument('--dev', action='store_true', help='Development mode (10 second rounds)')
    args = parser.parse_args()
    
    # Initialize Pygame
    pygame.init()
    
    # Screen setup
    screen_width = 1024
    screen_height = 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Drift")
    
    # Clock for FPS control
    clock = pygame.time.Clock()
    fps = 60
    
    # Create game
    game = Game(screen_width, screen_height, dev_mode=args.dev)
    
    # Game loop
    running = True
    start_time = pygame.time.get_ticks()
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            game.handle_event(event)
        
        # Update
        dt = 1.0 / fps  # Fixed timestep
        game.update(dt)
        
        # Draw
        current_time = pygame.time.get_ticks() - start_time
        game.draw(screen, current_time)
        
        # Flip display
        pygame.display.flip()
        
        # Maintain FPS
        clock.tick(fps)
    
    # Cleanup
    game.cleanup()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
