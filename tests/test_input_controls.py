"""
Unit tests for Input Handling & Controls system.

Tests the input manager, game controller, and main game application.
"""

import pytest
import pygame
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.ui.input_manager import InputManager, InputAction, ControlScheme, KeyBinding
from src.ui.game_controller import GameController
from src.game.game_logic import GameLogic, GameConfig
from src.game.grid import Direction, Position


class TestInputManager:
    """Test the InputManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        pygame.init()
        self.input_manager = InputManager()
    
    def teardown_method(self):
        """Clean up after tests."""
        pygame.quit()
    
    def test_input_manager_creation(self):
        """Test InputManager creation and initialization."""
        assert self.input_manager is not None
        assert self.input_manager.control_scheme == ControlScheme.ARROW_KEYS
        assert self.input_manager.input_enabled is True
        assert self.input_manager.movement_enabled is True
        assert len(self.input_manager.key_bindings) > 0
    
    def test_key_bindings_setup(self):
        """Test that key bindings are properly set up."""
        bindings = self.input_manager.get_key_bindings()
        
        # Check movement keys
        assert InputAction.MOVE_UP in bindings
        assert InputAction.MOVE_DOWN in bindings
        assert InputAction.MOVE_LEFT in bindings
        assert InputAction.MOVE_RIGHT in bindings
        
        # Check game control keys
        assert InputAction.PAUSE in bindings
        assert InputAction.RESTART in bindings
        assert InputAction.QUIT in bindings
        
        # Check that primary keys are set
        up_binding = bindings[InputAction.MOVE_UP]
        assert up_binding.primary_key == pygame.K_UP
        assert up_binding.secondary_key == pygame.K_w
    
    def test_control_scheme_switching(self):
        """Test switching between control schemes."""
        # Test WASD scheme
        self.input_manager.set_control_scheme(ControlScheme.WASD)
        assert self.input_manager.control_scheme == ControlScheme.WASD
        
        bindings = self.input_manager.get_key_bindings()
        up_binding = bindings[InputAction.MOVE_UP]
        assert up_binding.primary_key == pygame.K_w
        assert up_binding.secondary_key == pygame.K_UP
        
        # Test arrow keys scheme
        self.input_manager.set_control_scheme(ControlScheme.ARROW_KEYS)
        assert self.input_manager.control_scheme == ControlScheme.ARROW_KEYS
        
        bindings = self.input_manager.get_key_bindings()
        up_binding = bindings[InputAction.MOVE_UP]
        assert up_binding.primary_key == pygame.K_UP
        assert up_binding.secondary_key == pygame.K_w
    
    def test_key_press_handling(self):
        """Test key press event handling."""
        # Simulate key press
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_UP
        
        self.input_manager.handle_event(event)
        
        assert pygame.K_UP in self.input_manager.keys_pressed
        assert pygame.K_UP in self.input_manager.keys_just_pressed
    
    def test_key_release_handling(self):
        """Test key release event handling."""
        # First press a key
        press_event = Mock()
        press_event.type = pygame.KEYDOWN
        press_event.key = pygame.K_UP
        self.input_manager.handle_event(press_event)
        
        # Then release it
        release_event = Mock()
        release_event.type = pygame.KEYUP
        release_event.key = pygame.K_UP
        self.input_manager.handle_event(release_event)
        
        assert pygame.K_UP not in self.input_manager.keys_pressed
        assert pygame.K_UP in self.input_manager.keys_just_released
    
    def test_movement_direction_prevention(self):
        """Test that 180° turns are prevented."""
        # Set initial movement direction
        self.input_manager.set_movement_direction(InputAction.MOVE_RIGHT)
        
        # Try to move left (opposite direction)
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_LEFT
        
        # Mock the callback to check if it's called
        callback_called = False
        def test_callback(action, key):
            nonlocal callback_called
            callback_called = True
        
        self.input_manager.register_callback(InputAction.MOVE_LEFT, test_callback)
        self.input_manager.handle_event(event)
        
        # Callback should not be called for prevented direction
        assert not callback_called
    
    def test_input_buffering(self):
        """Test input buffering functionality."""
        # Press multiple movement keys quickly
        keys = [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]
        
        for key in keys:
            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = key
            self.input_manager.handle_event(event)
        
        # Check buffer size
        assert len(self.input_manager.input_buffer) == 3
        
        # Get buffered input
        buffered = self.input_manager.get_buffered_input()
        assert buffered == InputAction.MOVE_UP
        
        # Buffer should have remaining inputs
        assert len(self.input_manager.input_buffer) == 2
    
    def test_callback_registration(self):
        """Test callback registration and execution."""
        callback_called = False
        callback_action = None
        callback_key = None
        
        def test_callback(action, key):
            nonlocal callback_called, callback_action, callback_key
            callback_called = True
            callback_action = action
            callback_key = key
        
        # Register callback
        self.input_manager.register_callback(InputAction.MOVE_UP, test_callback)
        
        # Trigger the action
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_UP
        self.input_manager.handle_event(event)
        
        # Check callback was called
        assert callback_called
        assert callback_action == InputAction.MOVE_UP
        assert callback_key == pygame.K_UP
    
    def test_input_enabling_disabling(self):
        """Test enabling and disabling input processing."""
        # Disable input
        self.input_manager.disable_input()
        assert not self.input_manager.input_enabled
        
        # Try to handle an event
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_UP
        
        # Event should not be processed
        initial_buffer_size = len(self.input_manager.input_buffer)
        self.input_manager.handle_event(event)
        assert len(self.input_manager.input_buffer) == initial_buffer_size
        
        # Re-enable input
        self.input_manager.enable_input()
        assert self.input_manager.input_enabled
    
    def test_movement_enabling_disabling(self):
        """Test enabling and disabling movement input."""
        # Disable movement
        self.input_manager.disable_movement()
        assert not self.input_manager.movement_enabled
        
        # Try to move
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_UP
        
        # Movement should not be processed
        initial_buffer_size = len(self.input_manager.input_buffer)
        self.input_manager.handle_event(event)
        assert len(self.input_manager.input_buffer) == initial_buffer_size
        
        # Re-enable movement
        self.input_manager.enable_movement()
        assert self.input_manager.movement_enabled
    
    def test_input_stats(self):
        """Test input statistics retrieval."""
        stats = self.input_manager.get_input_stats()
        
        assert "keys_pressed" in stats
        assert "input_buffer_size" in stats
        assert "control_scheme" in stats
        assert "input_enabled" in stats
        assert "movement_enabled" in stats
    
    def test_reset_input_state(self):
        """Test resetting input state."""
        # Press some keys
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_UP
        self.input_manager.handle_event(event)
        
        # Reset state
        self.input_manager.reset_input_state()
        
        # Check state is reset
        assert len(self.input_manager.keys_pressed) == 0
        assert len(self.input_manager.input_buffer) == 0
        assert self.input_manager.last_movement_direction is None


class TestGameController:
    """Test the GameController class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        pygame.init()
        self.config = GameConfig()
        self.game_logic = GameLogic(self.config)
        self.input_manager = InputManager()
        self.game_controller = GameController(self.game_logic, self.input_manager)
    
    def teardown_method(self):
        """Clean up after tests."""
        pygame.quit()
    
    def test_game_controller_creation(self):
        """Test GameController creation and initialization."""
        assert self.game_controller is not None
        assert self.game_controller.game_logic == self.game_logic
        assert self.game_controller.input_manager == self.input_manager
        assert not self.game_controller.game_running
        assert self.game_controller.input_processing_enabled
    
    def test_start_game(self):
        """Test starting the game."""
        self.game_controller.start_game()
        
        assert self.game_controller.game_running
        assert self.input_manager.input_enabled
        assert self.input_manager.movement_enabled
    
    def test_stop_game(self):
        """Test stopping the game."""
        self.game_controller.start_game()
        self.game_controller.stop_game()
        
        assert not self.game_controller.game_running
        assert not self.input_manager.input_enabled
        assert not self.input_manager.movement_enabled
    
    def test_pause_resume_game(self):
        """Test pausing and resuming the game."""
        self.game_controller.start_game()
        
        # Pause game
        self.game_controller.pause_game()
        assert self.game_logic.is_game_paused()
        assert not self.input_manager.movement_enabled
        
        # Resume game
        self.game_controller.resume_game()
        assert not self.game_logic.is_game_paused()
        assert self.input_manager.movement_enabled
    
    def test_restart_game(self):
        """Test restarting the game."""
        self.game_controller.start_game()
        
        # Make some changes to game state
        self.game_logic.game_state.add_score(100)
        
        # Restart game
        self.game_controller.restart_game()
        
        # Check game is reset
        assert self.game_logic.get_score() == 0
        assert self.input_manager.movement_enabled
    
    def test_movement_validation(self):
        """Test movement validation logic."""
        self.game_controller.start_game()
        
        # Test valid movement
        valid = self.game_controller._is_movement_valid(Direction.UP)
        assert valid is True
        
        # Test invalid movement (180° turn)
        # First set a direction
        self.game_logic.change_snake_direction("right")
        
        # Try to go left (opposite)
        valid = self.game_controller._is_movement_valid(Direction.LEFT)
        assert valid is False
    
    def test_input_action_to_direction_conversion(self):
        """Test converting input actions to grid directions."""
        direction = self.game_controller._input_action_to_direction(InputAction.MOVE_UP)
        assert direction == Direction.UP
        
        direction = self.game_controller._input_action_to_direction(InputAction.MOVE_DOWN)
        assert direction == Direction.DOWN
        
        direction = self.game_controller._input_action_to_direction(InputAction.MOVE_LEFT)
        assert direction == Direction.LEFT
        
        direction = self.game_controller._input_action_to_direction(InputAction.MOVE_RIGHT)
        assert direction == Direction.RIGHT
    
    def test_control_scheme_switching(self):
        """Test switching control schemes."""
        initial_scheme = self.game_controller.get_control_scheme()
        
        # Switch to WASD
        self.game_controller.set_control_scheme(ControlScheme.WASD)
        assert self.game_controller.get_control_scheme() == ControlScheme.WASD
        
        # Switch back
        self.game_controller.set_control_scheme(ControlScheme.ARROW_KEYS)
        assert self.game_controller.get_control_scheme() == ControlScheme.ARROW_KEYS
    
    def test_movement_delay_setting(self):
        """Test setting movement delay."""
        initial_delay = self.game_controller.get_movement_delay()
        
        # Set new delay
        self.game_controller.set_movement_delay(0.2)
        assert self.game_controller.get_movement_delay() == 0.2
        
        # Test minimum delay
        self.game_controller.set_movement_delay(0.01)
        assert self.game_controller.get_movement_delay() >= 0.05
    
    def test_input_processing_enabling_disabling(self):
        """Test enabling and disabling input processing."""
        # Disable input processing
        self.game_controller.disable_input_processing()
        assert not self.game_controller.is_input_processing_enabled()
        
        # Re-enable
        self.game_controller.enable_input_processing()
        assert self.game_controller.is_input_processing_enabled()
    
    def test_game_stats_retrieval(self):
        """Test retrieving game statistics."""
        stats = self.game_controller.get_game_stats()
        assert stats is not None
        
        input_stats = self.game_controller.get_input_stats()
        assert input_stats is not None
    
    def test_controller_reset(self):
        """Test resetting the controller."""
        self.game_controller.start_game()
        self.game_controller.reset_controller()
        
        assert not self.game_controller.game_running
        assert self.game_controller.input_processing_enabled
        assert self.game_controller.pending_movement is None


class TestMainGame:
    """Test the main SnakeGame class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        pygame.init()
        self.config = GameConfig(
            grid_width=20,
            grid_height=15,
            cell_size=20,
            initial_speed=10.0,
            speed_increase=0.5,
            max_speed=25.0
        )
    
    def teardown_method(self):
        """Clean up after tests."""
        pygame.quit()
    
    @patch('pygame.init')
    @patch('pygame.quit')
    def test_snake_game_creation(self, mock_quit, mock_init):
        """Test SnakeGame creation."""
        from main import SnakeGame
        
        game = SnakeGame(self.config)
        
        assert game is not None
        assert game.config == self.config
        assert not game.running
        assert not game.paused
        assert game.current_screen == "game"
    
    @patch('pygame.init')
    @patch('pygame.quit')
    def test_snake_game_components(self, mock_quit, mock_init):
        """Test that all game components are properly initialized."""
        from main import SnakeGame
        
        game = SnakeGame(self.config)
        
        # Check components exist
        assert game.display_manager is not None
        assert game.game_logic is not None
        assert game.input_manager is not None
        assert game.game_controller is not None
        assert game.game_renderer is not None
        assert game.game_loop is not None
    
    @patch('pygame.init')
    @patch('pygame.quit')
    def test_snake_game_control_methods(self, mock_quit, mock_init):
        """Test game control methods."""
        from main import SnakeGame
        
        game = SnakeGame(self.config)
        
        # Test pause/resume
        game.pause()
        assert game.paused
        
        game.resume()
        assert not game.paused
        
        # Test restart
        game.restart()
        assert game.current_screen == "game"
        
        # Test control scheme
        game.set_control_scheme(ControlScheme.WASD)
        assert game.get_control_scheme() == ControlScheme.WASD
    
    @patch('pygame.init')
    @patch('pygame.quit')
    def test_snake_game_state_methods(self, mock_quit, mock_init):
        """Test game state query methods."""
        from main import SnakeGame
        
        game = SnakeGame(self.config)
        
        # Test initial state
        assert not game.is_running()
        assert not game.is_paused()
        
        # Test stats methods
        game_stats = game.get_game_stats()
        assert game_stats is not None
        
        input_stats = game.get_input_stats()
        assert input_stats is not None


if __name__ == "__main__":
    pytest.main([__file__])
