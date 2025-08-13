"""
Difficulty Management System

This module handles all difficulty-related functionality:
- Difficulty level definitions and settings
- Difficulty-specific game mechanics
- Difficulty selection and persistence
- Visual indicators for current difficulty
- Difficulty-based scoring adjustments
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from .game_state import Difficulty
from datetime import datetime


@dataclass
class DifficultySettings:
    """Configuration settings for a specific difficulty level."""
    name: str
    speed_multiplier: float
    scoring_multiplier: float
    food_spawn_rate: float
    power_up_frequency: float
    obstacle_density: float
    initial_speed: float
    max_speed: float
    speed_increase_rate: float
    description: str
    color: str
    icon: str


class DifficultyManager:
    """
    Manages difficulty levels and their effects on gameplay.
    
    Features:
    - Multiple difficulty levels (Easy, Medium, Hard)
    - Difficulty-specific settings and multipliers
    - Difficulty persistence between games
    - Visual indicators and feedback
    - Difficulty-based game balance
    """
    
    def __init__(self):
        """Initialize the difficulty manager."""
        self.current_difficulty = Difficulty.MEDIUM
        self.difficulty_settings = self._setup_difficulty_settings()
        self.difficulty_history: List[Tuple[str, float]] = []  # (difficulty, timestamp)
        
        # Load saved difficulty preference
        self._load_difficulty_preference()
    
    def _setup_difficulty_settings(self) -> Dict[Difficulty, DifficultySettings]:
        """Set up default difficulty settings."""
        return {
            Difficulty.EASY: DifficultySettings(
                name="Easy",
                speed_multiplier=0.7,
                scoring_multiplier=0.8,
                food_spawn_rate=1.2,
                power_up_frequency=1.3,
                obstacle_density=0.5,
                initial_speed=6.0,
                max_speed=18.0,
                speed_increase_rate=0.3,
                description="Relaxed gameplay with slower speed and more food",
                color="green",
                icon="🌱"
            ),
            Difficulty.MEDIUM: DifficultySettings(
                name="Medium",
                speed_multiplier=1.0,
                scoring_multiplier=1.0,
                food_spawn_rate=1.0,
                power_up_frequency=1.0,
                obstacle_density=1.0,
                initial_speed=8.0,
                max_speed=25.0,
                speed_increase_rate=0.5,
                description="Balanced gameplay with moderate challenge",
                color="yellow",
                icon="⚡"
            ),
            Difficulty.HARD: DifficultySettings(
                name="Hard",
                speed_multiplier=1.4,
                scoring_multiplier=1.3,
                food_spawn_rate=0.8,
                power_up_frequency=0.7,
                obstacle_density=1.5,
                initial_speed=12.0,
                max_speed=35.0,
                speed_increase_rate=0.7,
                description="Challenging gameplay with high speed and fewer resources",
                color="red",
                icon="🔥"
            )
        }
    
    def set_difficulty(self, difficulty: Difficulty) -> None:
        """Change the current difficulty level."""
        if difficulty != self.current_difficulty:
            self.current_difficulty = difficulty
            self._save_difficulty_preference()
            self._add_to_history(difficulty)
    
    def get_current_difficulty(self) -> Difficulty:
        """Get the current difficulty level."""
        return self.current_difficulty
    
    def get_current_settings(self) -> DifficultySettings:
        """Get the settings for the current difficulty level."""
        return self.difficulty_settings[self.current_difficulty]
    
    def get_difficulty_settings(self, difficulty: Difficulty) -> DifficultySettings:
        """Get the settings for a specific difficulty level."""
        return self.difficulty_settings[difficulty]
    
    def get_all_difficulties(self) -> List[Difficulty]:
        """Get all available difficulty levels."""
        return list(Difficulty)
    
    def get_difficulty_display_name(self, difficulty: Difficulty) -> str:
        """Get the display name for a difficulty level."""
        return self.difficulty_settings[difficulty].name
    
    def get_difficulty_description(self, difficulty: Difficulty) -> str:
        """Get the description for a difficulty level."""
        return self.difficulty_settings[difficulty].description
    
    def get_difficulty_color(self, difficulty: Difficulty) -> str:
        """Get the color associated with a difficulty level."""
        return self.difficulty_settings[difficulty].color
    
    def get_difficulty_icon(self, difficulty: Difficulty) -> str:
        """Get the icon associated with a difficulty level."""
        return self.difficulty_settings[difficulty].icon
    
    def get_speed_multiplier(self, difficulty: Optional[Difficulty] = None) -> float:
        """Get the speed multiplier for a difficulty level."""
        if difficulty is None:
            difficulty = self.current_difficulty
        return self.difficulty_settings[difficulty].speed_multiplier
    
    def get_scoring_multiplier(self, difficulty: Optional[Difficulty] = None) -> float:
        """Get the scoring multiplier for a difficulty level."""
        if difficulty is None:
            difficulty = self.current_difficulty
        return self.difficulty_settings[difficulty].scoring_multiplier
    
    def get_food_spawn_rate(self, difficulty: Optional[Difficulty] = None) -> float:
        """Get the food spawn rate for a difficulty level."""
        if difficulty is None:
            difficulty = self.current_difficulty
        return self.difficulty_settings[difficulty].food_spawn_rate
    
    def get_power_up_frequency(self, difficulty: Optional[Difficulty] = None) -> float:
        """Get the power-up frequency for a difficulty level."""
        if difficulty is None:
            difficulty = self.current_difficulty
        return self.difficulty_settings[difficulty].power_up_frequency
    
    def get_obstacle_density(self, difficulty: Optional[Difficulty] = None) -> float:
        """Get the obstacle density for a difficulty level."""
        if difficulty is None:
            difficulty = self.current_difficulty
        return self.difficulty_settings[difficulty].obstacle_density
    
    def get_initial_speed(self, difficulty: Optional[Difficulty] = None) -> float:
        """Get the initial speed for a difficulty level."""
        if difficulty is None:
            difficulty = self.current_difficulty
        return self.difficulty_settings[difficulty].initial_speed
    
    def get_max_speed(self, difficulty: Optional[Difficulty] = None) -> float:
        """Get the maximum speed for a difficulty level."""
        if difficulty is None:
            difficulty = self.current_difficulty
        return self.difficulty_settings[difficulty].max_speed
    
    def get_speed_increase_rate(self, difficulty: Optional[Difficulty] = None) -> float:
        """Get the speed increase rate for a difficulty level."""
        if difficulty is None:
            difficulty = self.current_difficulty
        return self.difficulty_settings[difficulty].speed_increase_rate
    
    def calculate_difficulty_score(self, base_score: int, difficulty: Optional[Difficulty] = None) -> int:
        """Calculate the final score based on difficulty multiplier."""
        if difficulty is None:
            difficulty = self.current_difficulty
        multiplier = self.get_scoring_multiplier(difficulty)
        return int(base_score * multiplier)
    
    def get_difficulty_stats(self) -> Dict:
        """Get statistics about difficulty usage."""
        stats = {}
        for difficulty in Difficulty:
            difficulty_name = difficulty.value
            count = sum(1 for _, diff in self.difficulty_history if diff == difficulty_name)
            stats[difficulty_name] = {
                'usage_count': count,
                'display_name': self.get_difficulty_display_name(difficulty),
                'description': self.get_difficulty_description(difficulty),
                'color': self.get_difficulty_color(difficulty),
                'icon': self.get_difficulty_icon(difficulty),
                'settings': asdict(self.get_difficulty_settings(difficulty))
            }
        return stats
    
    def _add_to_history(self, difficulty: Difficulty) -> None:
        """Add a difficulty change to the history."""
        import time
        self.difficulty_history.append((difficulty.value, time.time()))
        
        # Keep only last 100 entries
        if len(self.difficulty_history) > 100:
            self.difficulty_history = self.difficulty_history[-100:]
    
    def _save_difficulty_preference(self) -> None:
        """Save the current difficulty preference to a file."""
        try:
            config_dir = os.path.expanduser("~/.snake_game")
            os.makedirs(config_dir, exist_ok=True)
            
            config_file = os.path.join(config_dir, "difficulty_config.json")
            config_data = {
                'current_difficulty': self.current_difficulty.value,
                'last_updated': str(datetime.now())
            }
            
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
        except Exception as e:
            print(f"Failed to save difficulty preference: {e}")
    
    def _load_difficulty_preference(self) -> None:
        """Load the saved difficulty preference from file."""
        try:
            config_file = os.path.expanduser("~/.snake_game/difficulty_config.json")
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                
                saved_difficulty = config_data.get('current_difficulty', 'medium')
                for difficulty in Difficulty:
                    if difficulty.value == saved_difficulty:
                        self.current_difficulty = difficulty
                        break
        except Exception as e:
            print(f"Failed to load difficulty preference: {e}")
    
    def reset_difficulty(self) -> None:
        """Reset difficulty to default (Medium)."""
        self.set_difficulty(Difficulty.MEDIUM)
    
    def is_difficulty_easy(self) -> bool:
        """Check if current difficulty is Easy."""
        return self.current_difficulty == Difficulty.EASY
    
    def is_difficulty_medium(self) -> bool:
        """Check if current difficulty is Medium."""
        return self.current_difficulty == Difficulty.MEDIUM
    
    def is_difficulty_hard(self) -> bool:
        """Check if current difficulty is Hard."""
        return self.current_difficulty == Difficulty.HARD
    
    def get_difficulty_comparison(self) -> Dict[str, Dict]:
        """Get a comparison of all difficulty levels."""
        comparison = {}
        for difficulty in Difficulty:
            settings = self.difficulty_settings[difficulty]
            comparison[difficulty.value] = {
                'name': settings.name,
                'description': settings.description,
                'color': settings.color,
                'icon': settings.icon,
                'speed_multiplier': settings.speed_multiplier,
                'scoring_multiplier': settings.scoring_multiplier,
                'food_spawn_rate': settings.food_spawn_rate,
                'power_up_frequency': settings.power_up_frequency,
                'obstacle_density': settings.obstacle_density,
                'initial_speed': settings.initial_speed,
                'max_speed': settings.max_speed,
                'speed_increase_rate': settings.speed_increase_rate
            }
        return comparison
