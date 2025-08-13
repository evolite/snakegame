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
from src.ui.menu_manager import MenuManager, MenuState
from src.ui.audio_manager import AudioManager, SoundEffect, BackgroundMusic
from src.game.game_modes import GameMode


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
        
        try:
            # Initialize Pygame
            print("Initializing Pygame...")
            pygame.init()
            print("✓ Pygame initialized successfully")
            
            # Initialize game components
            print("Initializing display manager...")
            self.display_manager = DisplayManager(config)
            print("✓ Display manager initialized")
            
            print("Initializing game logic...")
            self.game_logic = GameLogic(config)
            print("✓ Game logic initialized")
            
            print("Initializing input manager...")
            self.input_manager = InputManager(self.display_manager)
            print("✓ Input manager initialized")
            
            print("Initializing game controller...")
            self.game_controller = GameController(self.game_logic, self.input_manager)
            print("✓ Game controller initialized")
            
            print("Initializing menu manager...")
            self.menu_manager = MenuManager(self.input_manager)
            print("✓ Menu manager initialized")
            
            # Initialize renderers
            print("Initializing game renderer...")
            self.game_renderer = GameRenderer(self.display_manager)
            print("✓ Game renderer initialized")
            
            # Initialize audio manager (with error handling)
            print("Initializing audio manager...")
            try:
                self.audio_manager = AudioManager()
                print("✓ Audio manager initialized")
                
                # Register audio callbacks with game logic
                self.game_logic.register_audio_callback("food_collected", 
                    lambda: self.audio_manager.play_sound_effect(SoundEffect.FOOD_COLLECTION))
                self.game_logic.register_audio_callback("collision", 
                    lambda: self.audio_manager.play_sound_effect(SoundEffect.COLLISION))
            except Exception as e:
                print(f"⚠️ Audio manager failed to initialize: {e}")
                print("Game will continue without audio")
                self.audio_manager = None
            
            # Initialize game loop
            print("Initializing game loop...")
            self.game_loop = FixedTimestepGameLoop(
                game_logic=self.game_logic,
                target_fps=60,  # Default target FPS
                physics_fps=10   # Default physics FPS
            )
            print("✓ Game loop initialized")
            
            # Set up game loop callbacks
            self.game_loop.set_update_callback(self.update)
            self.game_loop.set_render_callback(self.render)
            self.game_loop.set_physics_update_callback(self.physics_update)
            
            # Set up input callbacks
            self._setup_input_callbacks()
            
            # Game state
            self.current_screen = "game"  # game, menu, game_over, pause
            
            # Setup menu callbacks
            self._setup_menu_callbacks()
            
            print("✓ Snake Game initialization completed successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize Snake Game: {e}")
            import traceback
            traceback.print_exc()
            raise
        
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
    
    def _setup_menu_callbacks(self):
        """Set up callbacks for menu actions."""
        self.menu_manager.register_callback("new_game", self._handle_new_game)
        self.menu_manager.register_callback("high_scores", self._handle_high_scores)
        self.menu_manager.register_callback("settings", self._handle_settings)
        self.menu_manager.register_callback("quit", self._handle_quit)
        self.menu_manager.register_callback("retry", self._handle_retry)
        self.menu_manager.register_callback("main_menu", self._handle_main_menu)
        self.menu_manager.register_callback("resume", self._handle_resume)
        self.menu_manager.register_callback("restart", self._handle_restart)
        self.menu_manager.register_callback("back", self._handle_back)
        self.menu_manager.register_callback("difficulty_level", self._handle_difficulty_level)
        self.menu_manager.register_callback("difficulty_easy", self._handle_difficulty_easy)
        self.menu_manager.register_callback("difficulty_medium", self._handle_difficulty_medium)
        self.menu_manager.register_callback("difficulty_hard", self._handle_difficulty_hard)
        self.menu_manager.register_callback("back_to_menu", self._handle_back_to_menu)
        
        # Game mode callbacks
        self.menu_manager.register_callback("game_mode", self._handle_game_mode_selection)
        self.menu_manager.register_callback("mode_classic", self._handle_mode_classic)
        self.menu_manager.register_callback("mode_time_attack", self._handle_mode_time_attack)
        self.menu_manager.register_callback("mode_survival", self._handle_mode_survival)
        self.menu_manager.register_callback("mode_speed", self._handle_mode_speed)
        
    def start(self):
        """Start the game."""
        print("Starting Snake Game...")
        self.running = True
        self.menu_manager.set_menu_state(MenuState.START_MENU)
        self.current_screen = "menu"
        
        # Play main menu music
        self.audio_manager.play_background_music(BackgroundMusic.MAIN_MENU)
        
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
        
        # Update menu manager
        self.menu_manager.update(delta_time)
        
        # Update game controller if in game
        if self.current_screen == "game":
            self.game_controller.update(delta_time)
            
            # Check game state changes
            game_status = self.game_controller.get_game_status()
            if game_status == "game_over":
                # Save high score if achieved
                self.game_logic.get_scoring_system().save_high_score()
                # Play game over audio
                self.audio_manager.play_sound_effect(SoundEffect.GAME_OVER)
                self.audio_manager.play_background_music(BackgroundMusic.GAME_OVER)
                self.current_screen = "game_over"
                self.menu_manager.set_menu_state(MenuState.GAME_OVER)
            elif game_status == "paused":
                self.current_screen = "pause"
                self.menu_manager.set_menu_state(MenuState.PAUSE_MENU)
    
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
        elif self.current_screen == "high_scores":
            self._render_high_scores_screen()
        
        # Update display
        self.display_manager.update_display()
    
    def _render_game(self):
        """Render the main game screen."""
        # Get game state
        game_stats = self.game_controller.get_game_stats()
        
        # Render game elements
        self.game_renderer.render_game(
            snake=self.game_logic.snake,
            food_list=self.game_logic.food_manager.get_food_list(),
            score=self.game_logic.get_score(),
            level=self.game_logic.get_level(),
            food_eaten=self.game_logic.get_food_eaten(),
            game_time=self.game_logic.get_game_time(),
            high_score=self.game_logic.get_high_score(),
            power_ups_manager=self.game_logic.power_ups_manager,
            obstacle_manager=self.game_logic.obstacle_manager,
            current_difficulty=self.game_logic.get_current_difficulty()
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
        current_state = self.menu_manager.get_current_state()
        title = self.menu_manager.get_menu_title()
        options = [opt.text for opt in self.menu_manager.get_current_options()]
        selected_index = self.menu_manager.get_selected_index()
        
        self.game_renderer.render_menu_screen(title, options, selected_index)
    
    def _render_high_scores_screen(self):
        """Render the high scores screen."""
        high_scores = self.game_logic.get_scoring_system().get_high_scores_list()
        self.game_renderer.render_high_scores_screen(high_scores)
    
    def _handle_quit(self, action, key):
        """Handle quit input."""
        self.running = False
    
    def _handle_menu(self, action, key):
        """Handle menu input."""
        if self.current_screen == "game":
            self.game_controller.pause_game()
        elif self.current_screen == "pause":
            self.game_controller.resume_game()
    
    def _handle_new_game(self):
        """Handle new game menu action."""
        self.audio_manager.play_sound_effect(SoundEffect.GAME_START)
        self.audio_manager.play_background_music(BackgroundMusic.GAMEPLAY)
        self.game_controller.start_game()
        self.current_screen = "game"
        self.menu_manager.disable_menu()
    
    def _handle_settings(self):
        """Handle settings menu action."""
        self.menu_manager.set_menu_state(MenuState.SETTINGS_MENU)
    
    def _handle_retry(self):
        """Handle retry menu action."""
        self.game_controller.restart_game()
        self.current_screen = "game"
        self.menu_manager.disable_menu()
    
    def _handle_main_menu(self):
        """Handle main menu action."""
        self.menu_manager.set_menu_state(MenuState.START_MENU)
        self.current_screen = "menu"
        self.menu_manager.enable_menu()
    
    def _handle_resume(self):
        """Handle resume menu action."""
        self.game_controller.resume_game()
        self.current_screen = "game"
        self.menu_manager.disable_menu()
    
    def _handle_restart(self):
        """Handle restart menu action."""
        self.game_controller.restart_game()
        self.current_screen = "game"
        self.menu_manager.disable_menu()
    
    def _handle_back(self):
        """Handle back menu action."""
        if self.menu_manager.get_current_state() == MenuState.SETTINGS_MENU:
            self.menu_manager.set_menu_state(MenuState.START_MENU)
        elif self.menu_manager.get_current_state() == MenuState.DIFFICULTY_SELECTION:
            self.menu_manager.set_menu_state(MenuState.SETTINGS_MENU)
    
    def _handle_difficulty_level(self):
        """Handle difficulty level menu action."""
        self.menu_manager.set_menu_state(MenuState.DIFFICULTY_SELECTION)
    
    def _handle_difficulty_easy(self):
        """Handle easy difficulty selection."""
        self.game_logic.set_difficulty("easy")
        self.menu_manager.set_menu_state(MenuState.SETTINGS_MENU)
    
    def _handle_difficulty_medium(self):
        """Handle medium difficulty selection."""
        self.game_logic.set_difficulty("medium")
        self.menu_manager.set_menu_state(MenuState.SETTINGS_MENU)
    
    def _handle_difficulty_hard(self):
        """Handle hard difficulty selection."""
        self.game_logic.set_difficulty("hard")
        self.menu_manager.set_menu_state(MenuState.SETTINGS_MENU)
    
    def pause(self):
        """Pause the game."""
        self.paused = True
        self.game_controller.pause_game()
        self.current_screen = "pause"
        self.menu_manager.set_menu_state(MenuState.PAUSE_MENU)
        self.menu_manager.enable_menu()
    
    def resume(self):
        """Resume the game."""
        self.paused = False
        self.game_controller.resume_game()
        self.current_screen = "game"
        self.menu_manager.disable_menu()
    
    def restart(self):
        """Restart the game."""
        self.game_controller.restart_game()
        self.current_screen = "game"
        self.menu_manager.disable_menu()
    
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
        
        # Clean up audio
        if hasattr(self, 'audio_manager'):
            self.audio_manager.cleanup()
        
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
    
    def _handle_high_scores(self):
        """Handle high scores menu action."""
        self.audio_manager.play_sound_effect(SoundEffect.MENU_SELECT)
        self.menu_manager.set_menu_state(MenuState.HIGH_SCORES)
        self.current_screen = "high_scores"
    
    def _handle_back_to_menu(self):
        """Handle back to menu action."""
        self.menu_manager.set_menu_state(MenuState.START_MENU)
        self.current_screen = "menu"
    
    def _handle_game_mode_selection(self):
        """Handle game mode selection menu action."""
        self.audio_manager.play_sound_effect(SoundEffect.MENU_SELECT)
        self.menu_manager.set_menu_state(MenuState.GAME_MODE_SELECTION)
        self.current_screen = "game_mode_selection"
    
    def _handle_mode_classic(self):
        """Handle classic mode selection."""
        self.audio_manager.play_sound_effect(SoundEffect.MENU_SELECT)
        self.game_logic.game_mode_manager.set_game_mode(GameMode.CLASSIC)
        self.game_logic.game_mode_manager.apply_mode_config(self.game_logic)
        self.menu_manager.set_menu_state(MenuState.START_MENU)
        self.current_screen = "menu"
        print("Selected Classic Mode")
    
    def _handle_mode_time_attack(self):
        """Handle time attack mode selection."""
        self.audio_manager.play_sound_effect(SoundEffect.MENU_SELECT)
        self.game_logic.game_mode_manager.set_game_mode(GameMode.TIME_ATTACK)
        self.game_logic.game_mode_manager.apply_mode_config(self.game_logic)
        self.menu_manager.set_menu_state(MenuState.START_MENU)
        self.current_screen = "menu"
        print("Selected Time Attack Mode")
    
    def _handle_mode_survival(self):
        """Handle survival mode selection."""
        self.audio_manager.play_sound_effect(SoundEffect.MENU_SELECT)
        self.game_logic.game_mode_manager.set_game_mode(GameMode.SURVIVAL)
        self.game_logic.game_mode_manager.apply_mode_config(self.game_logic)
        self.menu_manager.set_menu_state(MenuState.START_MENU)
        self.current_screen = "menu"
        print("Selected Survival Mode")
    
    def _handle_mode_speed(self):
        """Handle speed mode selection."""
        self.audio_manager.play_sound_effect(SoundEffect.MENU_SELECT)
        self.audio_manager.play_sound_effect(SoundEffect.MENU_SELECT)
        self.game_logic.game_mode_manager.set_game_mode(GameMode.SPEED)
        self.game_logic.game_mode_manager.apply_mode_config(self.game_logic)
        self.menu_manager.set_menu_state(MenuState.START_MENU)
        self.current_screen = "menu"
        print("Selected Speed Mode")


def main():
    """Main entry point for the Snake Game."""
    print("Snake Game - Starting up...")
    
    try:
        # Import check
        print("Checking imports...")
        import pygame
        print(f"✓ Pygame {pygame.version.ver} imported successfully")
        
        # Create game configuration
        print("Creating game configuration...")
        config = GameConfig(
            grid_width=40,
            grid_height=30,
            cell_size=20,
            initial_speed=8.0,
            speed_increase=0.5,
            max_speed=25.0
        )
        print("✓ Game configuration created")
        
        # Create and start the game
        print("Creating SnakeGame instance...")
        game = SnakeGame(config)
        print("✓ SnakeGame instance created successfully")
        
        try:
            print("Starting game...")
            game.start()
        except Exception as e:
            print(f"❌ Error running game: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("Cleaning up...")
            game.cleanup()
            
    except Exception as e:
        print(f"❌ Critical error during game initialization: {e}")
        import traceback
        traceback.print_exc()
        print("Game will exit due to initialization error")
        input("Press Enter to continue...")  # Keep console open
        return 1
    
    print("Snake Game - Shutdown complete")
    input("Press Enter to continue...")  # Keep console open
    return 0


if __name__ == "__main__":
    main()
