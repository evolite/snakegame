"""
Food System

This module handles food spawning, types, and effects.
It includes different food types with varying point values and special effects.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import random
from .grid import Position, Grid


class FoodType(Enum):
    """Enumeration of food types with their properties."""
    NORMAL = "normal"
    BONUS = "bonus"
    SPEED_UP = "speed_up"
    SPEED_DOWN = "speed_down"
    DOUBLE_POINTS = "double_points"
    INVINCIBILITY = "invincibility"


@dataclass
class FoodProperties:
    """Properties of a food item."""
    points: int
    duration: float  # Duration of effect in seconds (0 for instant)
    color: str
    symbol: str
    probability: float  # Spawn probability (0.0 to 1.0)


class Food:
    """
    Represents a food item in the game.
    
    Food items can have different types, effects, and point values.
    """
    
    # Food type definitions with their properties
    FOOD_TYPES = {
        FoodType.NORMAL: FoodProperties(
            points=10,
            duration=0.0,
            color="red",
            symbol="●",
            probability=0.7
        ),
        FoodType.BONUS: FoodProperties(
            points=25,
            duration=0.0,
            color="gold",
            symbol="★",
            probability=0.15
        ),
        FoodType.SPEED_UP: FoodProperties(
            points=15,
            duration=5.0,
            color="blue",
            symbol="⚡",
            probability=0.05
        ),
        FoodType.SPEED_DOWN: FoodProperties(
            points=5,
            duration=3.0,
            color="purple",
            symbol="🐌",
            probability=0.05
        ),
        FoodType.DOUBLE_POINTS: FoodProperties(
            points=20,
            duration=8.0,
            color="green",
            symbol="2×",
            probability=0.03
        ),
        FoodType.INVINCIBILITY: FoodProperties(
            points=30,
            duration=4.0,
            color="white",
            symbol="🛡️",
            probability=0.02
        )
    }
    
    def __init__(self, position: Position, food_type: FoodType = FoodType.NORMAL):
        """Initialize a food item."""
        self.position = position
        self.food_type = food_type
        self.properties = self.FOOD_TYPES[food_type]
        self.collected = False
        self.spawn_time = 0.0  # Will be set by the food manager
        
    def get_position(self) -> Position:
        """Get the food's position."""
        return self.position
    
    def get_points(self) -> int:
        """Get the points this food provides."""
        return self.properties.points
    
    def get_duration(self) -> float:
        """Get the duration of this food's effect."""
        return self.properties.duration
    
    def get_color(self) -> str:
        """Get the color of this food."""
        return self.properties.color
    
    def get_symbol(self) -> str:
        """Get the symbol representing this food."""
        return self.properties.symbol
    
    def collect(self) -> None:
        """Mark the food as collected."""
        self.collected = True
    
    def is_collected(self) -> bool:
        """Check if the food has been collected."""
        return self.collected
    
    def get_effect_type(self) -> FoodType:
        """Get the type of effect this food provides."""
        return self.food_type
    
    def has_temporary_effect(self) -> bool:
        """Check if this food has a temporary effect."""
        return self.properties.duration > 0.0


class FoodManager:
    """
    Manages food spawning and collection in the game.
    
    Handles:
    - Food spawning at random positions
    - Food type selection based on probabilities
    - Food collection and respawning
    - Special food effects
    """
    
    def __init__(self, grid: Grid, max_food: int = 3):
        """Initialize the food manager."""
        self.grid = grid
        self.max_food = max_food
        self.active_food: List[Food] = []
        self.food_spawn_timer = 0.0
        self.spawn_interval = 2.0  # Seconds between spawns
        self.special_food_chance = 0.3  # Chance for special food
        
    def spawn_food(self, force_normal: bool = False) -> Optional[Food]:
        """
        Spawn a new food item at a random free position.
        
        Args:
            force_normal: If True, always spawn normal food
            
        Returns:
            The spawned food item, or None if no free positions
        """
        # Find a free position
        position = self.grid.get_random_free_position()
        if position is None:
            return None
        
        # Determine food type
        if force_normal:
            food_type = FoodType.NORMAL
        else:
            food_type = self._select_food_type()
        
        # Create and add food
        food = Food(position, food_type)
        self.active_food.append(food)
        
        # Mark position as occupied
        self.grid.occupy_position(position)
        
        return food
    
    def _select_food_type(self) -> FoodType:
        """Select a food type based on probabilities."""
        rand = random.random()
        cumulative_prob = 0.0
        
        for food_type, properties in self.FOOD_TYPES.items():
            cumulative_prob += properties.probability
            if rand <= cumulative_prob:
                return food_type
        
        # Fallback to normal food
        return FoodType.NORMAL
    
    def get_food_at_position(self, position: Position) -> Optional[Food]:
        """Get food at a specific position, if any."""
        for food in self.active_food:
            if food.get_position() == position and not food.is_collected():
                return food
        return None
    
    def collect_food_at_position(self, position: Position) -> Optional[Food]:
        """
        Collect food at a specific position.
        
        Returns:
            The collected food item, or None if no food at position
        """
        food = self.get_food_at_position(position)
        if food:
            food.collect()
            self.grid.free_position(position)
            return food
        return None
    
    def remove_collected_food(self) -> None:
        """Remove all collected food items from the active list."""
        self.active_food = [food for food in self.active_food if not food.is_collected()]
    
    def get_active_food_count(self) -> int:
        """Get the number of active food items."""
        return len([food for food in self.active_food if not food.is_collected()])
    
    def should_spawn_food(self) -> bool:
        """Check if more food should be spawned."""
        return self.get_active_food_count() < self.max_food
    
    def update(self, delta_time: float) -> None:
        """Update the food manager (called each frame)."""
        self.food_spawn_timer += delta_time
        
        # Remove collected food
        self.remove_collected_food()
        
        # Spawn new food if needed
        if self.should_spawn_food() and self.food_spawn_timer >= self.spawn_interval:
            if self.spawn_food():
                self.food_spawn_timer = 0.0
    
    def clear_all_food(self) -> None:
        """Clear all food from the grid."""
        for food in self.active_food:
            if not food.is_collected():
                self.grid.free_position(food.get_position())
        self.active_food.clear()
        self.food_spawn_timer = 0.0
    
    def get_food_positions(self) -> List[Position]:
        """Get positions of all active food items."""
        return [food.get_position() for food in self.active_food if not food.is_collected()]
    
    def set_max_food(self, max_food: int) -> None:
        """Set the maximum number of food items."""
        self.max_food = max_food
    
    def set_spawn_interval(self, interval: float) -> None:
        """Set the interval between food spawns."""
        self.spawn_interval = interval
    
    def get_food_stats(self) -> Dict[str, Any]:
        """Get statistics about food spawning and collection."""
        total_spawned = len(self.active_food)
        active_count = self.get_active_food_count()
        collected_count = total_spawned - active_count
        
        return {
            "total_spawned": total_spawned,
            "active_count": active_count,
            "collected_count": collected_count,
            "max_food": self.max_food,
            "spawn_interval": self.spawn_interval
        }
