"""
Game State Management System

This module handles the overall game state, including:
- Game status (menu, playing, paused, game over)
- Score tracking
- Level progression
- Game configuration
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class GameStatus(Enum):
    """Enumeration of possible game states."""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    SETTINGS = "settings"


class Difficulty(Enum):
    """Enumeration of difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass
class GameConfig:
    """Configuration settings for the game."""
    grid_width: int = 30
    grid_height: int = 20
    cell_size: int = 20
    initial_speed: float = 10.0  # cells per second
    speed_increase: float = 0.5   # speed increase per food eaten
    max_speed: float = 25.0       # maximum speed limit


class GameState:
    """
    Central game state manager.
    
    Manages the overall state of the game including status, score,
    configuration, and other global game variables.
    """
    
    def __init__(self, config: Optional[GameConfig] = None):
        """Initialize the game state with optional configuration."""
        self.config = config or GameConfig()
        self.status = GameStatus.MENU
        self.difficulty = Difficulty.MEDIUM
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.food_eaten = 0
        self.game_time = 0.0  # in seconds
        
    def reset_game(self) -> None:
        """Reset the game state for a new game."""
        self.status = GameStatus.PLAYING
        self.score = 0
        self.level = 1
        self.food_eaten = 0
        self.game_time = 0.0
        
    def pause_game(self) -> None:
        """Pause the current game."""
        if self.status == GameStatus.PLAYING:
            self.status = GameStatus.PAUSED
            
    def resume_game(self) -> None:
        """Resume a paused game."""
        if self.status == GameStatus.PAUSED:
            self.status = GameStatus.PLAYING
            
    def end_game(self) -> None:
        """End the current game."""
        self.status = GameStatus.GAME_OVER
        if self.score > self.high_score:
            self.high_score = self.score
            
    def add_score(self, points: int) -> None:
        """Add points to the current score."""
        self.score += points
        self.food_eaten += 1
        
        # Level up every 5 food items
        if self.food_eaten % 5 == 0:
            self.level += 1
            
    def update_game_time(self, delta_time: float) -> None:
        """Update the game time counter."""
        if self.status == GameStatus.PLAYING:
            self.game_time += delta_time
            
    def get_current_speed(self) -> float:
        """Calculate the current game speed based on level and food eaten."""
        speed = self.config.initial_speed + (self.food_eaten * self.config.speed_increase)
        return min(speed, self.config.max_speed)
        
    def is_game_active(self) -> bool:
        """Check if the game is currently active (playing or paused)."""
        return self.status in [GameStatus.PLAYING, GameStatus.PAUSED]
        
    def can_pause(self) -> bool:
        """Check if the game can be paused."""
        return self.status == GameStatus.PLAYING
        
    def can_resume(self) -> bool:
        """Check if the game can be resumed."""
        return self.status == GameStatus.PAUSED
