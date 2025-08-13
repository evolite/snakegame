"""
Speed Progression System

This module implements a comprehensive speed progression system that provides:
- Dynamic speed progression based on multiple factors
- Smooth speed transitions and animations
- Speed indicators and visual feedback
- Configurable progression algorithms
- Speed-based scoring adjustments
"""

from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import math
import time


class SpeedProgressionType(Enum):
    """Enumeration of speed progression algorithms."""
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"
    STEPPED = "stepped"
    CUSTOM = "custom"


class SpeedTransitionType(Enum):
    """Enumeration of speed transition types."""
    INSTANT = "instant"
    SMOOTH = "smooth"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"


@dataclass
class SpeedConfig:
    """Configuration for the speed progression system."""
    initial_speed: float = 8.0  # Initial speed in cells per second
    max_speed: float = 30.0     # Maximum speed limit
    min_speed: float = 5.0      # Minimum speed limit
    
    # Progression settings
    progression_type: SpeedProgressionType = SpeedProgressionType.EXPONENTIAL
    base_increase: float = 0.3   # Base speed increase per food
    level_multiplier: float = 1.1  # Speed multiplier per level
    food_eaten_multiplier: float = 0.05  # Additional increase per food eaten
    
    # Transition settings
    transition_type: SpeedTransitionType = SpeedTransitionType.SMOOTH
    transition_duration: float = 0.5  # Duration of speed transitions in seconds
    
    # Difficulty multipliers
    difficulty_multipliers: Dict[str, float] = field(default_factory=lambda: {
        "easy": 0.8,
        "medium": 1.0,
        "hard": 1.3
    })
    
    # Custom progression function
    custom_progression_func: Optional[Callable[[int, int, float], float]] = None


@dataclass
class SpeedState:
    """Current state of the speed system."""
    current_speed: float
    target_speed: float
    previous_speed: float
    transition_start_time: float
    transition_progress: float
    is_transitioning: bool
    
    # Speed history for analysis
    speed_history: List[Tuple[float, float]] = field(default_factory=list)  # (time, speed)
    
    # Performance metrics
    average_speed: float = 0.0
    max_speed_reached: float = 0.0
    speed_change_count: int = 0


class SpeedProgressionSystem:
    """
    Comprehensive speed progression system.
    
    Handles:
    - Dynamic speed calculation based on multiple factors
    - Smooth speed transitions and animations
    - Speed progression algorithms
    - Speed-based scoring adjustments
    - Performance tracking and analysis
    """
    
    def __init__(self, config: Optional[SpeedConfig] = None):
        """Initialize the speed progression system."""
        self.config = config or SpeedConfig()
        self.speed_state = SpeedState(
            current_speed=self.config.initial_speed,
            target_speed=self.config.initial_speed,
            previous_speed=self.config.initial_speed,
            transition_start_time=0.0,
            transition_progress=0.0,
            is_transitioning=False
        )
        
        # Speed progression tracking
        self.last_food_eaten = 0
        self.last_level = 1
        self.last_score = 0
        
        # Speed control settings
        self.speed_enabled = True
        self.speed_multiplier = 1.0
        self.speed_override = None
        
        # Speed milestones and achievements
        self.speed_milestones = []
        self.speed_achievements = []
        
        # Performance tracking
        self.performance_timer = 0.0
        self.performance_interval = 1.0  # Update performance metrics every second
    
    def update(self, delta_time: float, current_food_eaten: int, current_level: int, 
               current_score: int, difficulty: str = "medium") -> None:
        """
        Update the speed progression system.
        
        Args:
            delta_time: Time elapsed since last update
            current_food_eaten: Current number of food items eaten
            current_level: Current game level
            current_score: Current game score
            difficulty: Current difficulty level
        """
        # Check if speed should be updated
        if self._should_update_speed(current_food_eaten, current_level, current_score):
            self._update_target_speed(current_food_eaten, current_level, current_score, difficulty)
        
        # Update speed transitions
        self._update_speed_transitions(delta_time)
        
        # Update performance tracking
        self._update_performance_tracking(delta_time)
        
        # Update speed history
        self._update_speed_history(delta_time)
    
    def _should_update_speed(self, current_food_eaten: int, current_level: int, 
                           current_score: int) -> bool:
        """Check if speed should be updated based on game state changes."""
        return (current_food_eaten != self.last_food_eaten or
                current_level != self.last_level or
                current_score != self.last_score)
    
    def _update_target_speed(self, current_food_eaten: int, current_level: int, 
                           current_score: int, difficulty: str) -> None:
        """Update the target speed based on current game state."""
        # Calculate base speed using progression algorithm
        base_speed = self._calculate_base_speed(current_food_eaten, current_level)
        
        # Apply difficulty multiplier
        difficulty_mult = self.config.difficulty_multipliers.get(difficulty.lower(), 1.0)
        adjusted_speed = base_speed * difficulty_mult
        
        # Apply speed multiplier and overrides
        final_speed = adjusted_speed * self.speed_multiplier
        if self.speed_override is not None:
            final_speed = self.speed_override
        
        # Clamp speed to limits
        final_speed = max(self.config.min_speed, min(final_speed, self.config.max_speed))
        
        # Start transition if speed changed
        if abs(final_speed - self.speed_state.current_speed) > 0.1:
            self._start_speed_transition(final_speed)
        
        # Update tracking variables
        self.last_food_eaten = current_food_eaten
        self.last_level = current_level
        self.last_score = current_score
    
    def _calculate_base_speed(self, food_eaten: int, level: int) -> float:
        """Calculate base speed using the selected progression algorithm."""
        if self.config.progression_type == SpeedProgressionType.LINEAR:
            return self._calculate_linear_speed(food_eaten, level)
        elif self.config.progression_type == SpeedProgressionType.EXPONENTIAL:
            return self._calculate_exponential_speed(food_eaten, level)
        elif self.config.progression_type == SpeedProgressionType.LOGARITHMIC:
            return self._calculate_logarithmic_speed(food_eaten, level)
        elif self.config.progression_type == SpeedProgressionType.STEPPED:
            return self._calculate_stepped_speed(food_eaten, level)
        elif self.config.progression_type == SpeedProgressionType.CUSTOM:
            return self._calculate_custom_speed(food_eaten, level)
        else:
            return self.config.initial_speed
    
    def _calculate_linear_speed(self, food_eaten: int, level: int) -> float:
        """Calculate speed using linear progression."""
        food_increase = food_eaten * self.config.base_increase
        level_increase = (level - 1) * self.config.level_multiplier
        return self.config.initial_speed + food_increase + level_increase
    
    def _calculate_exponential_speed(self, food_eaten: int, level: int) -> float:
        """Calculate speed using exponential progression."""
        food_factor = math.pow(1 + self.config.food_eaten_multiplier, food_eaten)
        level_factor = math.pow(self.config.level_multiplier, level - 1)
        return self.config.initial_speed * food_factor * level_factor
    
    def _calculate_logarithmic_speed(self, food_eaten: int, level: int) -> float:
        """Calculate speed using logarithmic progression."""
        food_factor = math.log(1 + food_eaten * self.config.base_increase, 2)
        level_factor = math.log(1 + (level - 1) * self.config.level_multiplier, 2)
        return self.config.initial_speed + food_factor + level_factor
    
    def _calculate_stepped_speed(self, food_eaten: int, level: int) -> float:
        """Calculate speed using stepped progression."""
        food_steps = food_eaten // 5  # Speed increase every 5 food items
        level_steps = level - 1
        total_steps = food_steps + level_steps
        return self.config.initial_speed + (total_steps * self.config.base_increase)
    
    def _calculate_custom_speed(self, food_eaten: int, level: int) -> float:
        """Calculate speed using custom progression function."""
        if self.config.custom_progression_func:
            return self.config.custom_progression_func(food_eaten, level, self.config.initial_speed)
        else:
            return self._calculate_exponential_speed(food_eaten, level)
    
    def _start_speed_transition(self, target_speed: float) -> None:
        """Start a speed transition to the target speed."""
        self.speed_state.previous_speed = self.speed_state.current_speed
        self.speed_state.target_speed = target_speed
        self.speed_state.transition_start_time = time.time()
        self.speed_state.transition_progress = 0.0
        self.speed_state.is_transitioning = True
        self.speed_state.speed_change_count += 1
    
    def _update_speed_transitions(self, delta_time: float) -> None:
        """Update speed transitions and animations."""
        if not self.speed_state.is_transitioning:
            return
        
        # Calculate transition progress
        elapsed_time = time.time() - self.speed_state.transition_start_time
        progress = elapsed_time / self.config.transition_duration
        
        if progress >= 1.0:
            # Transition complete
            self.speed_state.current_speed = self.speed_state.target_speed
            self.speed_state.is_transitioning = False
            self.speed_state.transition_progress = 1.0
        else:
            # Update transition progress
            self.speed_state.transition_progress = progress
            
            # Calculate current speed based on transition type
            transition_factor = self._calculate_transition_factor(progress)
            speed_diff = self.speed_state.target_speed - self.speed_state.previous_speed
            self.speed_state.current_speed = (
                self.speed_state.previous_speed + (speed_diff * transition_factor)
            )
    
    def _calculate_transition_factor(self, progress: float) -> float:
        """Calculate transition factor based on transition type."""
        if self.config.transition_type == SpeedTransitionType.INSTANT:
            return 1.0
        elif self.config.transition_type == SpeedTransitionType.SMOOTH:
            return progress
        elif self.config.transition_type == SpeedTransitionType.EASE_IN:
            return progress * progress
        elif self.config.transition_type == SpeedTransitionType.EASE_OUT:
            return 1.0 - (1.0 - progress) * (1.0 - progress)
        elif self.config.transition_type == SpeedTransitionType.EASE_IN_OUT:
            if progress < 0.5:
                return 2.0 * progress * progress
            else:
                return 1.0 - 2.0 * (1.0 - progress) * (1.0 - progress)
        else:
            return progress
    
    def _update_performance_tracking(self, delta_time: float) -> None:
        """Update performance tracking metrics."""
        self.performance_timer += delta_time
        
        if self.performance_timer >= self.performance_interval:
            # Update average speed
            if self.speed_state.speed_history:
                total_speed = sum(speed for _, speed in self.speed_state.speed_history)
                self.speed_state.average_speed = total_speed / len(self.speed_state.speed_history)
            
            # Update max speed reached
            if self.speed_state.current_speed > self.speed_state.max_speed_reached:
                self.speed_state.max_speed_reached = self.speed_state.current_speed
            
            self.performance_timer = 0.0
    
    def _update_speed_history(self, delta_time: float) -> None:
        """Update speed history for analysis."""
        current_time = time.time()
        self.speed_state.speed_history.append((current_time, self.speed_state.current_speed))
        
        # Keep only last 1000 entries to prevent memory issues
        if len(self.speed_state.speed_history) > 1000:
            self.speed_state.speed_history = self.speed_state.speed_history[-1000:]
    
    def get_current_speed(self) -> float:
        """Get the current game speed."""
        return self.speed_state.current_speed
    
    def get_target_speed(self) -> float:
        """Get the target speed for the current transition."""
        return self.speed_state.target_speed
    
    def get_speed_progress(self) -> float:
        """Get the progress of the current speed transition (0.0 to 1.0)."""
        return self.speed_state.transition_progress
    
    def is_transitioning(self) -> bool:
        """Check if a speed transition is currently in progress."""
        return self.speed_state.is_transitioning
    
    def get_speed_multiplier(self) -> float:
        """Get the current speed multiplier."""
        return self.speed_multiplier
    
    def set_speed_multiplier(self, multiplier: float) -> None:
        """Set the speed multiplier."""
        self.speed_multiplier = max(0.1, min(multiplier, 5.0))  # Clamp between 0.1x and 5x
    
    def set_speed_override(self, speed: Optional[float]) -> None:
        """Set a speed override (None to disable)."""
        self.speed_override = speed
    
    def enable_speed_progression(self, enabled: bool) -> None:
        """Enable or disable speed progression."""
        self.speed_enabled = enabled
    
    def get_speed_statistics(self) -> Dict[str, Any]:
        """Get comprehensive speed statistics."""
        return {
            "current_speed": self.speed_state.current_speed,
            "target_speed": self.speed_state.target_speed,
            "previous_speed": self.speed_state.previous_speed,
            "is_transitioning": self.speed_state.is_transitioning,
            "transition_progress": self.speed_state.transition_progress,
            "average_speed": self.speed_state.average_speed,
            "max_speed_reached": self.speed_state.max_speed_reached,
            "speed_change_count": self.speed_state.speed_change_count,
            "speed_enabled": self.speed_enabled,
            "speed_multiplier": self.speed_multiplier,
            "speed_override": self.speed_override,
            "progression_type": self.config.progression_type.value,
            "transition_type": self.config.transition_type.value,
            "speed_history_count": len(self.speed_state.speed_history)
        }
    
    def get_speed_progression_info(self) -> Dict[str, Any]:
        """Get information about the current speed progression."""
        return {
            "initial_speed": self.config.initial_speed,
            "current_speed": self.speed_state.current_speed,
            "target_speed": self.speed_state.target_speed,
            "max_speed": self.config.max_speed,
            "min_speed": self.config.min_speed,
            "progression_type": self.config.progression_type.value,
            "transition_type": self.config.transition_type.value,
            "is_transitioning": self.speed_state.is_transitioning,
            "transition_progress": self.speed_state.transition_progress
        }
    
    def reset_speed(self) -> None:
        """Reset speed to initial values."""
        self.speed_state.current_speed = self.config.initial_speed
        self.speed_state.target_speed = self.config.initial_speed
        self.speed_state.previous_speed = self.config.initial_speed
        self.speed_state.is_transitioning = False
        self.speed_state.transition_progress = 0.0
        
        self.last_food_eaten = 0
        self.last_level = 1
        self.last_score = 0
        
        self.speed_multiplier = 1.0
        self.speed_override = None
    
    def set_progression_type(self, progression_type: SpeedProgressionType) -> None:
        """Set the speed progression algorithm."""
        self.config.progression_type = progression_type
    
    def set_transition_type(self, transition_type: SpeedTransitionType) -> None:
        """Set the speed transition type."""
        self.config.transition_type = transition_type
    
    def set_transition_duration(self, duration: float) -> None:
        """Set the duration of speed transitions."""
        self.config.transition_duration = max(0.1, duration)
    
    def get_speed_based_score_multiplier(self) -> float:
        """Get a score multiplier based on current speed."""
        # Higher speeds could provide score bonuses
        speed_factor = self.speed_state.current_speed / self.config.initial_speed
        return min(2.0, 1.0 + (speed_factor - 1.0) * 0.1)  # Max 2x multiplier
    
    def get_speed_difficulty_rating(self) -> str:
        """Get a human-readable difficulty rating based on current speed."""
        speed_ratio = self.speed_state.current_speed / self.config.max_speed
        
        if speed_ratio < 0.3:
            return "Easy"
        elif speed_ratio < 0.6:
            return "Medium"
        elif speed_ratio < 0.8:
            return "Hard"
        else:
            return "Extreme"
