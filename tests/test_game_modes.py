"""
Test Game Modes System

This module tests the multiple game modes functionality:
- Game mode creation and configuration
- Mode switching and application
- Statistics tracking
- Mode-specific features
"""

import pytest
from src.game.game_modes import (
    GameMode, GameModeConfig, GameModeStats, GameModeManager
)
from src.game.game_logic import GameLogic, GameConfig


class TestGameModes:
    """Test the game modes system."""
    
    def test_game_mode_enum(self):
        """Test that all game modes are defined."""
        assert GameMode.CLASSIC == GameMode("classic")
        assert GameMode.TIME_ATTACK == GameMode("time_attack")
        assert GameMode.SURVIVAL == GameMode("survival")
        assert GameMode.SPEED == GameMode("speed")
    
    def test_game_mode_config_creation(self):
        """Test game mode configuration creation."""
        config = GameModeConfig(
            mode=GameMode.CLASSIC,
            name="Test Mode",
            description="Test description",
            speed_multiplier=1.5,
            score_multiplier=2.0
        )
        
        assert config.mode == GameMode.CLASSIC
        assert config.name == "Test Mode"
        assert config.speed_multiplier == 1.5
        assert config.score_multiplier == 2.0
    
    def test_game_mode_manager_initialization(self):
        """Test game mode manager initialization."""
        manager = GameModeManager()
        
        # Check that all modes are available
        all_modes = manager.get_all_modes()
        assert len(all_modes) == 4
        assert GameMode.CLASSIC in all_modes
        assert GameMode.TIME_ATTACK in all_modes
        assert GameMode.SURVIVAL in all_modes
        assert GameMode.SPEED in all_modes
        
        # Check default mode
        assert manager.get_current_mode() == GameMode.CLASSIC
    
    def test_mode_switching(self):
        """Test switching between game modes."""
        manager = GameModeManager()
        
        # Switch to Time Attack mode
        manager.set_game_mode(GameMode.TIME_ATTACK)
        assert manager.get_current_mode() == GameMode.TIME_ATTACK
        
        # Switch to Survival mode
        manager.set_game_mode(GameMode.SURVIVAL)
        assert manager.get_current_mode() == GameMode.SURVIVAL
        
        # Switch back to Classic
        manager.set_game_mode(GameMode.CLASSIC)
        assert manager.get_current_mode() == GameMode.CLASSIC
    
    def test_mode_configuration_retrieval(self):
        """Test retrieving mode configurations."""
        manager = GameModeManager()
        
        # Get Classic mode config
        classic_config = manager.get_mode_config(GameMode.CLASSIC)
        assert classic_config.name == "Classic Mode"
        assert classic_config.speed_multiplier == 1.0
        assert classic_config.score_multiplier == 1.0
        
        # Get Time Attack mode config
        time_attack_config = manager.get_mode_config(GameMode.TIME_ATTACK)
        assert time_attack_config.name == "Time Attack Mode"
        assert time_attack_config.speed_multiplier == 1.2
        assert time_attack_config.score_multiplier == 1.5
        assert time_attack_config.time_limit == 120.0
    
    def test_mode_info_retrieval(self):
        """Test retrieving comprehensive mode information."""
        manager = GameModeManager()
        
        classic_info = manager.get_mode_info(GameMode.CLASSIC)
        assert classic_info["name"] == "Classic Mode"
        assert classic_info["mode"] == "classic"
        assert "stats" in classic_info
        
        # Check that stats are initialized
        stats = classic_info["stats"]
        assert stats["games_played"] == 0
        assert stats["best_score"] == 0
    
    def test_mode_configuration_application(self):
        """Test applying mode configuration to game logic."""
        manager = GameModeManager()
        config = GameConfig()
        game_logic = GameLogic(config)
        
        # Switch to Speed mode (which has higher multipliers)
        manager.set_game_mode(GameMode.SPEED)
        
        # Apply the configuration
        manager.apply_mode_config(game_logic)
        
        # Check that the configuration was applied
        speed_config = manager.get_mode_config(GameMode.SPEED)
        assert game_logic.speed_system.get_speed_multiplier() == speed_config.speed_multiplier
        assert game_logic.scoring_system.score_multiplier.base_multiplier == speed_config.score_multiplier
    
    def test_mode_statistics_tracking(self):
        """Test tracking statistics for different modes."""
        manager = GameModeManager()
        
        # Switch to Time Attack mode
        manager.set_game_mode(GameMode.TIME_ATTACK)
        
        # Update stats for a game
        game_stats = {
            'score': 1500,
            'game_time': 95.5,
            'food_eaten': 15,
            'obstacles_destroyed': 3,
            'power_ups_collected': 2
        }
        
        manager.update_mode_stats(game_stats)
        
        # Check that stats were updated
        time_attack_info = manager.get_mode_info(GameMode.TIME_ATTACK)
        stats = time_attack_info["stats"]
        assert stats["games_played"] == 1
        assert stats["total_score"] == 1500
        assert stats["best_score"] == 1500
        assert stats["total_time"] == 95.5
        assert stats["food_eaten"] == 15
    
    def test_mode_difficulty_ratings(self):
        """Test mode difficulty ratings."""
        manager = GameModeManager()
        
        assert manager.get_mode_difficulty(GameMode.CLASSIC) == "Medium"
        assert manager.get_mode_difficulty(GameMode.TIME_ATTACK) == "Medium-Hard"
        assert manager.get_mode_difficulty(GameMode.SURVIVAL) == "Hard"
        assert manager.get_mode_difficulty(GameMode.SPEED) == "Very Hard"
    
    def test_mode_recommendations(self):
        """Test mode recommendations based on player skill."""
        manager = GameModeManager()
        
        assert manager.get_recommended_mode("beginner") == GameMode.CLASSIC
        assert manager.get_recommended_mode("intermediate") == GameMode.TIME_ATTACK
        assert manager.get_recommended_mode("advanced") == GameMode.SURVIVAL
        assert manager.get_recommended_mode("expert") == GameMode.SPEED
        assert manager.get_recommended_mode("unknown") == GameMode.CLASSIC
    
    def test_mode_summary(self):
        """Test getting summary of all modes."""
        manager = GameModeManager()
        
        summary = manager.get_mode_summary()
        
        # Check that all modes are included
        assert "classic" in summary
        assert "time_attack" in summary
        assert "survival" in summary
        assert "speed" in summary
        
        # Check that each mode has the required information
        for mode_key in summary:
            mode_info = summary[mode_key]
            assert "name" in mode_info
            assert "description" in mode_info
            assert "stats" in mode_info
    
    def test_mode_statistics_reset(self):
        """Test resetting mode statistics."""
        manager = GameModeManager()
        
        # Switch to Survival mode and update stats
        manager.set_game_mode(GameMode.SURVIVAL)
        game_stats = {'score': 2000, 'game_time': 120.0, 'food_eaten': 20}
        manager.update_mode_stats(game_stats)
        
        # Check that stats were updated
        survival_info = manager.get_mode_info(GameMode.SURVIVAL)
        assert survival_info["stats"]["best_score"] == 2000
        
        # Reset stats for Survival mode
        manager.reset_mode_stats(GameMode.SURVIVAL)
        
        # Check that stats were reset
        survival_info_after_reset = manager.get_mode_info(GameMode.SURVIVAL)
        assert survival_info_after_reset["stats"]["best_score"] == 0
        assert survival_info_after_reset["stats"]["games_played"] == 0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
