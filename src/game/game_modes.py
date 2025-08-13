"""
Game Modes System

This module implements multiple game modes to increase replayability and variety:
- Classic Mode: Traditional snake gameplay
- Time Attack Mode: Score-based with time limits
- Survival Mode: Endless gameplay with increasing difficulty
- Speed Mode: Fast-paced with constant acceleration
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import json
import os
from datetime import datetime


class GameMode(Enum):
    """Available game modes."""
    CLASSIC = "classic"
    TIME_ATTACK = "time_attack"
    SURVIVAL = "survival"
    SPEED = "speed"


@dataclass
class GameModeConfig:
    """Configuration for a specific game mode."""
    mode: GameMode
    name: str
    description: str
    time_limit: Optional[float] = None  # None for unlimited time
    speed_multiplier: float = 1.0
    score_multiplier: float = 1.0
    food_spawn_rate: float = 1.0
    obstacle_density: float = 1.0
    power_up_frequency: float = 1.0
    snake_growth_rate: float = 1.0
    visual_theme: str = "default"
    special_rules: List[str] = field(default_factory=list)
    difficulty_curve: str = "normal"  # normal, aggressive, gentle


@dataclass
class GameModeStats:
    """Statistics for a specific game mode."""
    mode: GameMode
    games_played: int = 0
    total_score: int = 0
    best_score: int = 0
    total_time: float = 0.0
    best_time: float = 0.0
    food_eaten: int = 0
    obstacles_destroyed: int = 0
    power_ups_collected: int = 0
    last_played: Optional[str] = None


class GameModeManager:
    """
    Manages different game modes and their configurations.
    
    Features:
    - Multiple game mode support
    - Mode-specific configurations
    - Statistics tracking
    - Mode persistence
    - Seamless mode switching
    """
    
    def __init__(self, stats_file: str = "game_mode_stats.json"):
        """Initialize the game mode manager."""
        self.current_mode = GameMode.CLASSIC
        self.stats_file = stats_file
        self.mode_stats: Dict[GameMode, GameModeStats] = {}
        
        # Initialize mode configurations
        self.mode_configs = self._initialize_mode_configs()
        
        # Load existing statistics
        self._load_mode_stats()
        
        # Initialize statistics for all modes
        self._initialize_mode_stats()
    
    def _initialize_mode_configs(self) -> Dict[GameMode, GameModeConfig]:
        """Initialize configurations for all game modes."""
        return {
            GameMode.CLASSIC: GameModeConfig(
                mode=GameMode.CLASSIC,
                name="Classic Mode",
                description="Traditional snake gameplay with standard rules",
                speed_multiplier=1.0,
                score_multiplier=1.0,
                food_spawn_rate=1.0,
                obstacle_density=0.8,
                power_up_frequency=1.0,
                snake_growth_rate=1.0,
                visual_theme="classic",
                special_rules=["Standard snake growth", "Normal food spawning", "Balanced obstacles"]
            ),
            
            GameMode.TIME_ATTACK: GameModeConfig(
                mode=GameMode.TIME_ATTACK,
                name="Time Attack Mode",
                description="Score-based gameplay with time limits",
                time_limit=120.0,  # 2 minutes
                speed_multiplier=1.2,
                score_multiplier=1.5,
                food_spawn_rate=1.3,
                obstacle_density=0.6,
                power_up_frequency=1.2,
                snake_growth_rate=1.1,
                visual_theme="time_attack",
                special_rules=["Time limit", "Bonus points for speed", "Frequent power-ups"],
                difficulty_curve="aggressive"
            ),
            
            GameMode.SURVIVAL: GameModeConfig(
                mode=GameMode.SURVIVAL,
                name="Survival Mode",
                description="Endless gameplay with increasing difficulty",
                speed_multiplier=0.8,
                score_multiplier=1.3,
                food_spawn_rate=0.9,
                obstacle_density=1.2,
                power_up_frequency=0.8,
                snake_growth_rate=0.9,
                visual_theme="survival",
                special_rules=["Endless gameplay", "Increasing difficulty", "Survival bonus"],
                difficulty_curve="aggressive"
            ),
            
            GameMode.SPEED: GameModeConfig(
                mode=GameMode.SPEED,
                name="Speed Mode",
                description="Fast-paced gameplay with constant acceleration",
                speed_multiplier=1.5,
                score_multiplier=1.8,
                food_spawn_rate=1.5,
                obstacle_density=0.4,
                power_up_frequency=1.5,
                snake_growth_rate=1.3,
                visual_theme="speed",
                special_rules=["Constant acceleration", "Speed bonuses", "Quick reactions needed"],
                difficulty_curve="aggressive"
            )
        }
    
    def _initialize_mode_stats(self) -> None:
        """Initialize statistics for all game modes."""
        for mode in GameMode:
            if mode not in self.mode_stats:
                self.mode_stats[mode] = GameModeStats(mode=mode)
    
    def get_current_mode(self) -> GameMode:
        """Get the current game mode."""
        return self.current_mode
    
    def get_current_config(self) -> GameModeConfig:
        """Get the configuration for the current game mode."""
        return self.mode_configs[self.current_mode]
    
    def set_game_mode(self, mode: GameMode) -> None:
        """Set the current game mode."""
        if mode in GameMode:
            self.current_mode = mode
            print(f"Game mode changed to: {self.mode_configs[mode].name}")
    
    def get_mode_config(self, mode: GameMode) -> GameModeConfig:
        """Get configuration for a specific game mode."""
        return self.mode_configs.get(mode, self.mode_configs[GameMode.CLASSIC])
    
    def get_all_modes(self) -> List[GameMode]:
        """Get all available game modes."""
        return list(GameMode)
    
    def get_mode_info(self, mode: GameMode) -> Dict[str, Any]:
        """Get comprehensive information about a game mode."""
        config = self.get_mode_config(mode)
        stats = self.mode_stats.get(mode, GameModeStats(mode=mode))
        
        return {
            "mode": mode.value,
            "name": config.name,
            "description": config.description,
            "time_limit": config.time_limit,
            "speed_multiplier": config.speed_multiplier,
            "score_multiplier": config.score_multiplier,
            "food_spawn_rate": config.food_spawn_rate,
            "obstacle_density": config.obstacle_density,
            "power_up_frequency": config.power_up_frequency,
            "snake_growth_rate": config.snake_growth_rate,
            "visual_theme": config.visual_theme,
            "special_rules": config.special_rules,
            "difficulty_curve": config.difficulty_curve,
            "stats": {
                "games_played": stats.games_played,
                "best_score": stats.best_score,
                "best_time": stats.best_time,
                "total_score": stats.total_score,
                "total_time": stats.total_time,
                "food_eaten": stats.food_eaten,
                "obstacles_destroyed": stats.obstacles_destroyed,
                "power_ups_collected": stats.power_ups_collected,
                "last_played": stats.last_played
            }
        }
    
    def apply_mode_config(self, game_logic) -> None:
        """Apply the current mode configuration to the game logic."""
        config = self.get_current_config()
        
        # Apply speed multiplier
        if hasattr(game_logic, 'speed_system'):
            game_logic.speed_system.set_speed_multiplier(config.speed_multiplier)
        
        # Apply score multiplier
        if hasattr(game_logic, 'scoring_system'):
            game_logic.scoring_system.score_multiplier.base_multiplier = config.score_multiplier
        
        # Apply food spawn rate
        if hasattr(game_logic, 'food_manager'):
            game_logic.food_manager.set_spawn_rate_multiplier(config.food_spawn_rate)
        
        # Apply obstacle density
        if hasattr(game_logic, 'obstacle_manager'):
            game_logic.obstacle_manager.set_obstacle_density(config.obstacle_density)
        
        # Apply power-up frequency
        if hasattr(game_logic, 'power_ups_manager'):
            game_logic.power_ups_manager.set_spawn_frequency_multiplier(config.power_up_frequency)
        
        print(f"Applied {config.name} configuration")
    
    def update_mode_stats(self, game_stats: Dict[str, Any]) -> None:
        """Update statistics for the current game mode."""
        mode = self.current_mode
        if mode not in self.mode_stats:
            self.mode_stats[mode] = GameModeStats(mode=mode)
        
        stats = self.mode_stats[mode]
        
        # Update basic stats
        stats.games_played += 1
        stats.total_score += game_stats.get('score', 0)
        stats.total_time += game_stats.get('game_time', 0.0)
        stats.food_eaten += game_stats.get('food_eaten', 0)
        stats.obstacles_destroyed += game_stats.get('obstacles_destroyed', 0)
        stats.power_ups_collected += game_stats.get('power_ups_collected', 0)
        stats.last_played = datetime.now().isoformat()
        
        # Update best scores
        current_score = game_stats.get('score', 0)
        if current_score > stats.best_score:
            stats.best_score = current_score
        
        # Update best time (for time-based modes)
        current_time = game_stats.get('game_time', 0.0)
        if current_time > stats.best_time:
            stats.best_time = current_time
        
        # Save stats
        self._save_mode_stats()
    
    def get_mode_ranking(self, mode: GameMode) -> int:
        """Get the ranking of a score in a specific mode."""
        if mode not in self.mode_stats:
            return 1
        
        stats = self.mode_stats[mode]
        if stats.best_score == 0:
            return 1
        
        # This would be expanded to compare against other players
        # For now, just return 1 if it's a new best score
        return 1
    
    def get_mode_summary(self) -> Dict[str, Any]:
        """Get a summary of all game modes and their statistics."""
        summary = {}
        for mode in GameMode:
            summary[mode.value] = self.get_mode_info(mode)
        return summary
    
    def reset_mode_stats(self, mode: GameMode) -> None:
        """Reset statistics for a specific game mode."""
        if mode in self.mode_stats:
            self.mode_stats[mode] = GameModeStats(mode=mode)
            self._save_mode_stats()
    
    def reset_all_stats(self) -> None:
        """Reset statistics for all game modes."""
        self.mode_stats.clear()
        self._initialize_mode_stats()
        self._save_mode_stats()
    
    def _load_mode_stats(self) -> None:
        """Load mode statistics from file."""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    data = json.load(f)
                    for mode_str, stats_data in data.items():
                        try:
                            mode = GameMode(mode_str)
                            stats = GameModeStats(**stats_data)
                            stats.mode = mode  # Ensure mode is set correctly
                            self.mode_stats[mode] = stats
                        except (ValueError, KeyError) as e:
                            print(f"Error loading stats for mode {mode_str}: {e}")
        except Exception as e:
            print(f"Failed to load mode stats: {e}")
    
    def _save_mode_stats(self) -> None:
        """Save mode statistics to file."""
        try:
            # Convert stats to serializable format
            serializable_stats = {}
            for mode, stats in self.mode_stats.items():
                stats_dict = stats.__dict__.copy()
                stats_dict['mode'] = mode.value  # Convert enum to string
                serializable_stats[mode.value] = stats_dict
            
            with open(self.stats_file, 'w') as f:
                json.dump(serializable_stats, f, indent=2)
        except Exception as e:
            print(f"Failed to save mode stats: {e}")
    
    def get_recommended_mode(self, player_skill: str = "medium") -> GameMode:
        """Get a recommended game mode based on player skill."""
        if player_skill == "beginner":
            return GameMode.CLASSIC
        elif player_skill == "intermediate":
            return GameMode.TIME_ATTACK
        elif player_skill == "advanced":
            return GameMode.SURVIVAL
        elif player_skill == "expert":
            return GameMode.SPEED
        else:
            return GameMode.CLASSIC
    
    def get_mode_difficulty(self, mode: GameMode) -> str:
        """Get the difficulty level of a game mode."""
        difficulty_map = {
            GameMode.CLASSIC: "Medium",
            GameMode.TIME_ATTACK: "Medium-Hard",
            GameMode.SURVIVAL: "Hard",
            GameMode.SPEED: "Very Hard"
        }
        return difficulty_map.get(mode, "Medium")
