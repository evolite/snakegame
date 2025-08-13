"""
Scoring System

This module handles all scoring-related functionality:
- Score calculation and tracking
- High score management
- Score persistence
- Multiplier effects
- Achievement tracking
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from .food import FoodType


@dataclass
class ScoreEntry:
    """Represents a single score entry."""
    score: int
    date: str
    level: int
    food_eaten: int
    game_time: float
    difficulty: str
    player_name: str = "Player"


@dataclass
class HighScore:
    """Represents a high score entry."""
    score: int
    date: str
    level: int
    food_eaten: int
    game_time: float
    difficulty: str
    player_name: str = "Player"
    
    def __lt__(self, other: 'HighScore') -> bool:
        """Compare high scores (higher scores are 'less than' for sorting)."""
        return self.score > other.score


class ScoreMultiplier:
    """Manages score multipliers and their effects."""
    
    def __init__(self):
        """Initialize the score multiplier system."""
        self.base_multiplier = 1.0
        self.temporary_multiplier = 1.0
        self.temporary_duration = 0.0
        self.combo_multiplier = 1.0
        self.combo_timer = 0.0
        self.combo_timeout = 2.0  # seconds to maintain combo
        
    def update(self, delta_time: float) -> None:
        """Update multiplier timers."""
        # Update temporary multiplier
        if self.temporary_duration > 0:
            self.temporary_duration -= delta_time
            if self.temporary_duration <= 0:
                self.temporary_multiplier = 1.0
        
        # Update combo multiplier
        if self.combo_timer > 0:
            self.combo_timer -= delta_time
            if self.combo_timer <= 0:
                self.combo_multiplier = 1.0
    
    def get_total_multiplier(self) -> float:
        """Get the total current multiplier."""
        return self.base_multiplier * self.temporary_multiplier * self.combo_multiplier
    
    def set_temporary_multiplier(self, multiplier: float, duration: float) -> None:
        """Set a temporary multiplier for a specific duration."""
        self.temporary_multiplier = multiplier
        self.temporary_duration = duration
    
    def add_combo(self) -> None:
        """Add to the combo multiplier."""
        self.combo_multiplier += 0.1
        self.combo_timer = self.combo_timeout
    
    def reset_combo(self) -> None:
        """Reset the combo multiplier."""
        self.combo_multiplier = 1.0
        self.combo_timer = 0.0
    
    def get_combo_level(self) -> int:
        """Get the current combo level."""
        return int((self.combo_multiplier - 1.0) * 10)


class ScoringSystem:
    """
    Central scoring system for the game.
    
    Handles:
    - Score calculation
    - High score tracking
    - Score persistence
    - Multiplier management
    - Achievement tracking
    """
    
    def __init__(self, high_scores_file: str = "high_scores.json"):
        """Initialize the scoring system."""
        self.current_score = 0
        self.high_scores_file = high_scores_file
        self.high_scores: List[HighScore] = []
        self.score_multiplier = ScoreMultiplier()
        self.food_eaten_count = 0
        self.level = 1
        self.game_time = 0.0
        self.difficulty = "medium"
        self.player_name = "Player"
        
        # Load existing high scores
        self.load_high_scores()
        
        # Score values for different food types
        self.food_scores = {
            FoodType.NORMAL: 10,
            FoodType.BONUS: 25,
            FoodType.SPEED_UP: 15,
            FoodType.SPEED_DOWN: 5,
            FoodType.DOUBLE_POINTS: 20,
            FoodType.INVINCIBILITY: 30
        }
        
        # Bonus points for achievements
        self.achievement_bonuses = {
            "first_food": 5,
            "five_food": 25,
            "ten_food": 50,
            "speed_bonus": 10,
            "combo_bonus": 15
        }
    
    def add_food_score(self, food_type: FoodType) -> int:
        """
        Add score for eating food.
        
        Args:
            food_type: The type of food eaten
            
        Returns:
            The points added
        """
        base_score = self.food_scores.get(food_type, 10)
        multiplier = self.score_multiplier.get_total_multiplier()
        final_score = int(base_score * multiplier)
        
        self.current_score += final_score
        self.food_eaten_count += 1
        
        # Update level
        self.level = (self.food_eaten_count // 5) + 1
        
        # Handle special food effects
        if food_type == FoodType.DOUBLE_POINTS:
            self.score_multiplier.set_temporary_multiplier(2.0, 8.0)
        elif food_type == FoodType.SPEED_UP:
            self.score_multiplier.set_temporary_multiplier(1.5, 5.0)
        elif food_type == FoodType.SPEED_DOWN:
            self.score_multiplier.set_temporary_multiplier(0.5, 3.0)
        
        # Add combo bonus
        self.score_multiplier.add_combo()
        
        return final_score
    
    def add_score(self, points: int) -> int:
        """
        Add points directly to the current score.
        
        Args:
            points: The points to add
            
        Returns:
            The points added
        """
        self.current_score += points
        return points
    
    def add_bonus_score(self, bonus_type: str) -> int:
        """
        Add bonus score for achievements.
        
        Args:
            bonus_type: The type of bonus
            
        Returns:
            The bonus points added
        """
        bonus = self.achievement_bonuses.get(bonus_type, 0)
        self.current_score += bonus
        return bonus
    
    def update_game_time(self, delta_time: float) -> None:
        """Update the game time counter."""
        self.game_time += delta_time
    
    def get_current_score(self) -> int:
        """Get the current score."""
        return self.current_score
    
    def get_high_score(self) -> int:
        """Get the highest score achieved."""
        if self.high_scores:
            return self.high_scores[0].score
        return 0
    
    def is_new_high_score(self) -> bool:
        """Check if the current score is a new high score."""
        return self.current_score > self.get_high_score()
    
    def get_score_rank(self) -> int:
        """Get the rank of the current score among high scores."""
        for i, high_score in enumerate(self.high_scores):
            if self.current_score >= high_score.score:
                return i + 1
        return len(self.high_scores) + 1
    
    def save_high_score(self) -> bool:
        """Save the current score as a high score if it qualifies."""
        if not self.is_new_high_score():
            return False
        
        # Create new high score entry
        new_high_score = HighScore(
            score=self.current_score,
            date=datetime.now().isoformat(),
            level=self.level,
            food_eaten=self.food_eaten_count,
            game_time=self.game_time,
            difficulty=self.difficulty,
            player_name=self.player_name
        )
        
        # Add to high scores list
        self.high_scores.append(new_high_score)
        
        # Sort by score (highest first)
        self.high_scores.sort()
        
        # Keep only top 10 scores
        self.high_scores = self.high_scores[:10]
        
        # Save to file
        self.save_high_scores()
        
        return True
    
    def load_high_scores(self) -> None:
        """Load high scores from file."""
        try:
            if os.path.exists(self.high_scores_file):
                with open(self.high_scores_file, 'r') as f:
                    data = json.load(f)
                    self.high_scores = [HighScore(**entry) for entry in data]
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            # If file is corrupted or doesn't exist, start with empty list
            self.high_scores = []
    
    def save_high_scores(self) -> None:
        """Save high scores to file."""
        try:
            with open(self.high_scores_file, 'w') as f:
                json.dump([asdict(score) for score in self.high_scores], f, indent=2)
        except IOError:
            # Handle file write errors gracefully
            pass
    
    def reset_score(self) -> None:
        """Reset the current score and related counters."""
        self.current_score = 0
        self.food_eaten_count = 0
        self.level = 1
        self.game_time = 0.0
        self.score_multiplier.reset_combo()
    
    def get_score_stats(self) -> Dict[str, any]:
        """Get comprehensive scoring statistics."""
        return {
            "current_score": self.current_score,
            "high_score": self.get_high_score(),
            "food_eaten": self.food_eaten_count,
            "level": self.level,
            "game_time": self.game_time,
            "difficulty": self.difficulty,
            "multiplier": self.score_multiplier.get_total_multiplier(),
            "combo_level": self.score_multiplier.get_combo_level(),
            "score_rank": self.get_score_rank()
        }
    
    def set_difficulty(self, difficulty: str) -> None:
        """Set the current difficulty level."""
        self.difficulty = difficulty
    
    def set_player_name(self, name: str) -> None:
        """Set the player name for high scores."""
        self.player_name = name
    
    def get_high_scores_list(self, limit: int = 10) -> List[HighScore]:
        """Get the list of high scores, limited to specified count."""
        return self.high_scores[:limit]
    
    def get_high_scores(self, limit: int = 10) -> List[HighScore]:
        """Get a list of high scores, limited to the specified number (alias for get_high_scores_list)."""
        return self.get_high_scores_list(limit)
    
    def clear_high_scores(self) -> None:
        """Clear all high scores."""
        self.high_scores.clear()
        self.save_high_scores()
    
    def export_scores(self, filename: str) -> bool:
        """Export high scores to a file."""
        try:
            with open(filename, 'w') as f:
                json.dump([asdict(score) for score in self.high_scores], f, indent=2)
            return True
        except IOError:
            return False
    
    def import_scores(self, filename: str) -> bool:
        """Import high scores from a file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                imported_scores = [HighScore(**entry) for entry in data]
                
                # Merge with existing scores
                self.high_scores.extend(imported_scores)
                
                # Sort and keep top scores
                self.high_scores.sort()
                self.high_scores = self.high_scores[:10]
                
                # Save updated scores
                self.save_high_scores()
                
                return True
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            return False
