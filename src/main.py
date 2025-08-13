"""
Main Snake Game Application

Integrates all game components and provides the main game loop.
This is the entry point for the Snake game.
"""

import sys
import pygame
from src.game.game_logic import GameLogic, GameConfig
from src.game.game_loop import FixedTimestepGameLoop
from src.ui.display import DisplayManager
from src.ui.game_renderer import GameRenderer
from src.ui.input_manager import InputManager, ControlScheme
from src.ui.game_controller import GameController


class SnakeGame:
    """
    Main Snake Game application class.
    
    Integrates all game systems:
    - Game logic and state
    - Input handling and controls
    - Rendering and display
    - Game loop and timing
    """
    
    def __init__(self, config: GameConfig = None):
        """Initialize the Snake Game."""
        if config is None:
            config = GameConfig()
        
        self.config = config
        self.running = False
        self.paused = False
        
        # Initialize Pygame
        pygame.init()
        
        # Initialize game components
        self.display_manager = DisplayManager(config)
        
        self.game_logic = GameLogic(config)
        self.input_manager = InputManager(self.display_manager)
        self.game_controller = GameController(self.game_logic, self.input_manager)
        
        # Initialize renderers
        self.game_renderer = GameRenderer(self.display_manager)
        
        # Initialize game loop
        self.game_loop = FixedTimestepGameLoop(
            game_logic=self.game_logic,
            target_fps=60,  # Default target FPS
            physics_fps=10   # Default physics FPS
        )
        
        # Set up game loop callbacks
        self.game_loop.set_update_callback(self.update)
        self.game_loop.set_render_callback(self.render)
        self.game_loop.set_physics_update_callback(self.physics_update)
        
        # Set up input callbacks
        self._setup_input_callbacks()
        
        # Game state
        self.current_screen = "game"  # game, menu, game_over, pause
        
    def _setup_input_callbacks(self):
        """Set up input callbacks for the main game."""
        # Game control callbacks
        self.input_manager.register_callback(
            "quit", 
            self._handle_quit
        )
        self.input_manager.register_callback(
            "menu", 
            self._handle_menu
        )
        
    def start(self):
        """Start the game."""
        print("Starting Snake Game...")
        self.running = True
        self.game_controller.start_game()
        self.game_loop.start()
        
        # Main game loop
        try:
            while self.running:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        break
                    
                    # Handle input events
                    self.game_controller.handle_event(event)
                
                # Update game loop
                self.game_loop.update()
                
                # Check if game should continue
                if not self.game_controller.game_running:
                    self.running = False
                    
        except KeyboardInterrupt:
            print("Game interrupted by user")
        finally:
            self.cleanup()
    
    def update(self, delta_time: float):
        """Update game state (called by game loop)."""
        if not self.running:
            return
        
        # Update game controller
        self.game_controller.update(delta_time)
        
        # Update game state
        game_status = self.game_controller.get_game_status()
        if game_status == "game_over":
            self.current_screen = "game_over"
        elif game_status == "paused":
            self.current_screen = "pause"
        elif game_status == "active":
            self.current_screen = "game"
    
    def physics_update(self, delta_time: float):
        """Update physics (called by game loop)."""
        if not self.running:
            return
        
        # Physics updates are handled by the game logic
        # This is called at a fixed timestep for consistent physics
        pass
    
    def render(self):
        """Render the game (called by game loop)."""
        if not self.running:
            return
        
        # Clear screen
        self.display_manager.clear_screen()
        
        # Render based on current screen
        if self.current_screen == "game":
            self._render_game()
        elif self.current_screen == "pause":
            self._render_pause_screen()
        elif self.current_screen == "game_over":
            self._render_game_over_screen()
        elif self.current_screen == "menu":
            self._render_menu_screen()
        
        # Update display
        self.display_manager.update_display()
    
    def _render_game(self):
        """Render the main game screen."""
        # Get game state
        game_stats = self.game_controller.get_game_stats()
        
        # Render game elements
        self.game_renderer.render_game(
            snake_body=self.game_logic.get_snake_body(),
            food_positions=self.game_logic.get_food_positions(),
            score=self.game_logic.get_score(),
            high_score=self.game_logic.get_high_score(),
            level=self.game_logic.get_level(),
            game_time=self.game_logic.get_game_time()
        )
    
    def _render_pause_screen(self):
        """Render the pause screen."""
        self.game_renderer.render_pause_screen(
            score=self.game_logic.get_score(),
            high_score=self.game_logic.get_high_score()
        )
    
    def _render_game_over_screen(self):
        """Render the game over screen."""
        self.game_renderer.render_game_over_screen(
            score=self.game_logic.get_score(),
            high_score=self.game_logic.get_high_score(),
            snake_length=self.game_logic.get_snake_length(),
            game_time=self.game_logic.get_game_time()
        )
    
    def _render_menu_screen(self):
        """Render the menu screen."""
        self.game_renderer.render_menu_screen()
    
    def _handle_quit(self, action, key):
        """Handle quit input."""
        self.running = False
    
    def _handle_menu(self, action, key):
        """Handle menu input."""
        if self.current_screen == "game":
            self.game_controller.pause_game()
        elif self.current_screen == "pause":
            self.game_controller.resume_game()
    
    def pause(self):
        """Pause the game."""
        self.paused = True
        self.game_controller.pause_game()
    
    def resume(self):
        """Resume the game."""
        self.paused = False
        self.game_controller.resume_game()
    
    def restart(self):
        """Restart the game."""
        self.game_controller.restart_game()
        self.current_screen = "game"
    
    def set_control_scheme(self, scheme: ControlScheme):
        """Change the control scheme."""
        self.game_controller.set_control_scheme(scheme)
    
    def get_control_scheme(self) -> ControlScheme:
        """Get the current control scheme."""
        return self.game_controller.get_control_scheme()
    
    def cleanup(self):
        """Clean up resources."""
        print("Cleaning up...")
        
        # Stop game loop
        if self.game_loop:
            self.game_loop.stop()
        
        # Clean up display
        if self.display_manager:
            self.display_manager.cleanup()
        
        # Quit Pygame
        pygame.quit()
        
        print("Game cleaned up successfully")
    
    def get_game_stats(self):
        """Get current game statistics."""
        return self.game_controller.get_game_stats()
    
    def get_input_stats(self):
        """Get input statistics for debugging."""
        return self.game_controller.get_input_stats()
    
    def is_running(self) -> bool:
        """Check if the game is running."""
        return self.running
    
    def is_paused(self) -> bool:
        """Check if the game is paused."""
        return self.paused


def main():
    """Main entry point for the Snake Game."""
    print("Snake Game - Starting up...")
    
    # Create game configuration
    config = GameConfig(
        window_width=800,
        window_height=600,
        grid_width=40,
        grid_height=30,
        target_fps=60,
        physics_fps=10
    )
    
    # Create and start the game
    game = SnakeGame(config)
    
    try:
        game.start()
    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()
    finally:
        game.cleanup()
    
    print("Snake Game - Shutdown complete")


if __name__ == "__main__":
    main()
