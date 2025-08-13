"""
Unit tests for Game State Management System.

Tests the core game state components including:
- GameStatus enum
- Difficulty enum  
- GameConfig dataclass
- GameState class
"""

import pytest
import time
from src.game.game_state import GameStatus, Difficulty, GameConfig, GameState


class TestGameStatus:
    """Test the GameStatus enum."""
    
    def test_game_status_values(self):
        """Test that all expected game status values exist."""
        assert GameStatus.MENU.value == "menu"
        assert GameStatus.PLAYING.value == "playing"
        assert GameStatus.PAUSED.value == "paused"
        assert GameStatus.GAME_OVER.value == "game_over"
        assert GameStatus.SETTINGS.value == "settings"
    
    def test_game_status_enumeration(self):
        """Test that all status values can be enumerated."""
        statuses = list(GameStatus)
        assert len(statuses) == 5
        assert GameStatus.MENU in statuses
        assert GameStatus.PLAYING in statuses
        assert GameStatus.PAUSED in statuses
        assert GameStatus.GAME_OVER in statuses
        assert GameStatus.SETTINGS in statuses


class TestDifficulty:
    """Test the Difficulty enum."""
    
    def test_difficulty_values(self):
        """Test that all expected difficulty values exist."""
        assert Difficulty.EASY.value == "easy"
        assert Difficulty.MEDIUM.value == "medium"
        assert Difficulty.HARD.value == "hard"
    
    def test_difficulty_enumeration(self):
        """Test that all difficulty values can be enumerated."""
        difficulties = list(Difficulty)
        assert len(difficulties) == 3
        assert Difficulty.EASY in difficulties
        assert Difficulty.MEDIUM in difficulties
        assert Difficulty.HARD in difficulties


class TestGameConfig:
    """Test the GameConfig dataclass."""
    
    def test_game_config_default_values(self):
        """Test that GameConfig has correct default values."""
        config = GameConfig()
        
        assert config.grid_width == 30
        assert config.grid_height == 20
        assert config.cell_size == 20
        assert config.initial_speed == 10.0
        assert config.speed_increase == 0.5
        assert config.max_speed == 25.0
    
    def test_game_config_custom_values(self):
        """Test that GameConfig can be created with custom values."""
        config = GameConfig(
            grid_width=40,
            grid_height=30,
            cell_size=25,
            initial_speed=15.0,
            speed_increase=1.0,
            max_speed=30.0
        )
        
        assert config.grid_width == 40
        assert config.grid_height == 30
        assert config.cell_size == 25
        assert config.initial_speed == 15.0
        assert config.speed_increase == 1.0
        assert config.max_speed == 30.0
    
    def test_game_config_immutability(self):
        """Test that GameConfig fields can be modified."""
        config = GameConfig()
        
        # Modify values
        config.grid_width = 50
        config.initial_speed = 20.0
        
        assert config.grid_width == 50
        assert config.initial_speed == 20.0


class TestGameState:
    """Test the GameState class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = GameConfig()
        self.game_state = GameState(self.config)
    
    def test_game_state_initialization_with_config(self):
        """Test GameState initialization with provided config."""
        assert self.game_state.config == self.config
        assert self.game_state.status == GameStatus.MENU
        assert self.game_state.difficulty == Difficulty.MEDIUM
        assert self.game_state.score == 0
        assert self.game_state.high_score == 0
        assert self.game_state.level == 1
        assert self.game_state.food_eaten == 0
        assert self.game_state.game_time == 0.0
    
    def test_game_state_initialization_without_config(self):
        """Test GameState initialization without config (uses default)."""
        game_state = GameState()
        
        assert game_state.config is not None
        assert isinstance(game_state.config, GameConfig)
        assert game_state.status == GameStatus.MENU
        assert game_state.difficulty == Difficulty.MEDIUM
    
    def test_reset_game(self):
        """Test resetting the game state."""
        # Modify some values
        self.game_state.score = 100
        self.game_state.level = 5
        self.game_state.food_eaten = 10
        self.game_state.game_time = 60.0
        
        # Reset game
        self.game_state.reset_game()
        
        assert self.game_state.status == GameStatus.PLAYING
        assert self.game_state.score == 0
        assert self.game_state.level == 1
        assert self.game_state.food_eaten == 0
        assert self.game_state.game_time == 0.0
        
        # High score should remain unchanged
        assert self.game_state.high_score == 0
    
    def test_pause_game(self):
        """Test pausing the game."""
        # Set to playing first
        self.game_state.status = GameStatus.PLAYING
        
        self.game_state.pause_game()
        assert self.game_state.status == GameStatus.PAUSED
    
    def test_pause_game_when_not_playing(self):
        """Test that pause_game only works when status is PLAYING."""
        # Set to menu
        self.game_state.status = GameStatus.MENU
        
        self.game_state.pause_game()
        assert self.game_state.status == GameStatus.MENU  # Should not change
    
    def test_resume_game(self):
        """Test resuming the game."""
        # Set to paused first
        self.game_state.status = GameStatus.PAUSED
        
        self.game_state.resume_game()
        assert self.game_state.status == GameStatus.PLAYING
    
    def test_resume_game_when_not_paused(self):
        """Test that resume_game only works when status is PAUSED."""
        # Set to playing
        self.game_state.status = GameStatus.PLAYING
        
        self.game_state.resume_game()
        assert self.game_state.status == GameStatus.PLAYING  # Should not change
    
    def test_end_game(self):
        """Test ending the game."""
        # Set score and status
        self.game_state.score = 100
        self.game_state.status = GameStatus.PLAYING
        
        self.game_state.end_game()
        
        assert self.game_state.status == GameStatus.GAME_OVER
        assert self.game_state.high_score == 100  # Should update high score
    
    def test_end_game_high_score_update(self):
        """Test that high score is only updated when current score is higher."""
        # Set initial high score
        self.game_state.high_score = 200
        
        # End game with lower score
        self.game_state.score = 100
        self.game_state.end_game()
        
        assert self.game_state.high_score == 200  # Should not change
    
    def test_add_score(self):
        """Test adding score and level progression."""
        initial_score = self.game_state.score
        initial_level = self.game_state.level
        initial_food_eaten = self.game_state.food_eaten
        
        # Add score
        self.game_state.add_score(50)
        
        assert self.game_state.score == initial_score + 50
        assert self.game_state.food_eaten == initial_food_eaten + 1
        
        # Level should not change yet (need 5 food items)
        assert self.game_state.level == initial_level
    
    def test_add_score_level_progression(self):
        """Test that level increases every 5 food items eaten."""
        # Eat 4 food items
        for _ in range(4):
            self.game_state.add_score(10)
        
        assert self.game_state.level == 1  # Still level 1
        
        # Eat 5th food item
        self.game_state.add_score(10)
        assert self.game_state.level == 2  # Should level up
        
        # Eat 4 more food items
        for _ in range(4):
            self.game_state.add_score(10)
        
        assert self.game_state.level == 2  # Still level 2
        
        # Eat 10th food item
        self.game_state.add_score(10)
        assert self.game_state.level == 3  # Should level up again
    
    def test_update_game_time(self):
        """Test updating game time."""
        # Set status to playing first
        self.game_state.status = GameStatus.PLAYING
        initial_time = self.game_state.game_time
        
        # Update time
        self.game_state.update_game_time(1.5)
        assert self.game_state.game_time == initial_time + 1.5
        
        # Update again
        self.game_state.update_game_time(0.5)
        assert self.game_state.game_time == initial_time + 2.0
    
    def test_update_game_time_only_when_playing(self):
        """Test that game time only updates when status is PLAYING."""
        # Set to paused
        self.game_state.status = GameStatus.PAUSED
        initial_time = self.game_state.game_time
        
        # Update time
        self.game_state.update_game_time(2.0)
        
        # Time should not change when paused
        assert self.game_state.game_time == initial_time
    
    def test_get_current_speed(self):
        """Test getting current speed based on food eaten."""
        # Test initial speed
        assert self.game_state.get_current_speed() == 10.0
        
        # Eat food and check speed increase
        self.game_state.add_score(10)  # This will increase food_eaten to 1
        expected_speed = 10.0 + 0.5  # initial_speed + speed_increase
        assert self.game_state.get_current_speed() == expected_speed
        
        # Eat more food
        self.game_state.add_score(10)  # This will increase food_eaten to 2
        expected_speed = 10.0 + (0.5 * 2)  # initial_speed + (speed_increase * 2)
        assert self.game_state.get_current_speed() == expected_speed
    
    def test_get_current_speed_max_limit(self):
        """Test that speed doesn't exceed max_speed limit."""
        # Set a very high speed_increase to test limit
        self.game_state.config.speed_increase = 100.0
        
        # Eat food multiple times
        for _ in range(10):
            self.game_state.add_score(50)
        
        # Speed should be capped at max_speed
        assert self.game_state.get_current_speed() == 25.0  # max_speed
    
    def test_is_game_active(self):
        """Test checking if game is active."""
        # Initially not active (menu)
        assert not self.game_state.is_game_active()
        
        # Set to playing
        self.game_state.status = GameStatus.PLAYING
        assert self.game_state.is_game_active()
        
        # Set to paused
        self.game_state.status = GameStatus.PAUSED
        assert self.game_state.is_game_active()  # Paused is still considered active
        
        # Set to game over
        self.game_state.status = GameStatus.GAME_OVER
        assert not self.game_state.is_game_active()
    
    def test_can_pause(self):
        """Test checking if game can be paused."""
        # Initially can't pause (menu)
        assert not self.game_state.can_pause()
        
        # Set to playing
        self.game_state.status = GameStatus.PLAYING
        assert self.game_state.can_pause()
        
        # Set to paused
        self.game_state.status = GameStatus.PAUSED
        assert not self.game_state.can_pause()
        
        # Set to game over
        self.game_state.status = GameStatus.GAME_OVER
        assert not self.game_state.can_pause()
    
    def test_can_resume(self):
        """Test checking if game can be resumed."""
        # Initially can't resume (menu)
        assert not self.game_state.can_resume()
        
        # Set to playing
        self.game_state.status = GameStatus.PLAYING
        assert not self.game_state.can_resume()
        
        # Set to paused
        self.game_state.status = GameStatus.PAUSED
        assert self.game_state.can_resume()
        
        # Set to game over
        self.game_state.status = GameStatus.GAME_OVER
        assert not self.game_state.can_resume()


if __name__ == "__main__":
    pytest.main([__file__])
