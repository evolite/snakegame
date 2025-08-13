"""
Enhanced Food System

This module handles food spawning, types, and effects with:
- Multiple food types with unique effects
- Dynamic spawning and rarity systems
- Visual differentiation and animations
- Strategic gameplay enhancement
"""

from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import random
import math
from .grid import Position, Grid


class FoodType(Enum):
    """Enumeration of food types with their properties."""
    NORMAL = "normal"
    BONUS = "bonus"
    SPEED_UP = "speed_up"
    SPEED_DOWN = "speed_down"
    DOUBLE_POINTS = "double_points"
    INVINCIBILITY = "invincibility"
    GROWTH_BOOST = "growth_boost"
    MAGNET_FOOD = "magnet_food"
    SHIELD_FOOD = "shield_food"
    TIME_FREEZE = "time_freeze"
    GHOST_MODE = "ghost_mode"
    EXPLOSIVE_FOOD = "explosive_food"
    TELEPORT_FOOD = "teleport_food"
    RAINBOW_FOOD = "rainbow_food"


class FoodRarity(Enum):
    """Enumeration of food rarity levels."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


@dataclass
class FoodProperties:
    """Enhanced properties of a food item."""
    points: int
    duration: float  # Duration of effect in seconds (0 for instant)
    color: str
    symbol: str
    probability: float  # Spawn probability (0.0 to 1.0)
    rarity: FoodRarity
    description: str
    effect_strength: float  # Multiplier or effect intensity
    spawn_conditions: Dict[str, Any]  # Conditions for spawning
    visual_effects: List[str]  # List of visual effects to apply


class Food:
    """
    Represents an enhanced food item in the game.
    
    Food items can have different types, effects, point values, and visual properties.
    """
    
    # Enhanced food type definitions with their properties
    FOOD_TYPES = {
        FoodType.NORMAL: FoodProperties(
            points=10,
            duration=0.0,
            color="red",
            symbol="●",
            probability=0.6,
            rarity=FoodRarity.COMMON,
            description="Basic food - provides points and growth",
            effect_strength=1.0,
            spawn_conditions={},
            visual_effects=["pulse"]
        ),
        FoodType.BONUS: FoodProperties(
            points=25,
            duration=0.0,
            color="gold",
            symbol="★",
            probability=0.12,
            rarity=FoodRarity.UNCOMMON,
            description="Bonus food - extra points and growth",
            effect_strength=2.0,
            spawn_conditions={"min_score": 50},
            visual_effects=["pulse", "glow", "sparkle"]
        ),
        FoodType.SPEED_UP: FoodProperties(
            points=15,
            duration=6.0,
            color="blue",
            symbol="⚡",
            probability=0.06,
            rarity=FoodRarity.UNCOMMON,
            description="Speed boost - temporary speed increase",
            effect_strength=1.5,
            spawn_conditions={"min_level": 2},
            visual_effects=["flash", "lightning"]
        ),
        FoodType.SPEED_DOWN: FoodProperties(
            points=8,
            duration=4.0,
            color="purple",
            symbol="🐌",
            probability=0.04,
            rarity=FoodRarity.UNCOMMON,
            description="Slow motion - temporary speed decrease",
            effect_strength=0.5,
            spawn_conditions={"min_level": 3},
            visual_effects=["slow_pulse", "spiral"]
        ),
        FoodType.DOUBLE_POINTS: FoodProperties(
            points=20,
            duration=10.0,
            color="green",
            symbol="2×",
            probability=0.04,
            rarity=FoodRarity.RARE,
            description="Double points - score multiplier",
            effect_strength=2.0,
            spawn_conditions={"min_score": 100, "min_level": 3},
            visual_effects=["bounce", "glow", "multiplier"]
        ),
        FoodType.INVINCIBILITY: FoodProperties(
            points=35,
            duration=5.0,
            color="white",
            symbol="🛡️",
            probability=0.03,
            rarity=FoodRarity.RARE,
            description="Invincibility - temporary collision immunity",
            effect_strength=1.0,
            spawn_conditions={"min_level": 5, "min_score": 150},
            visual_effects=["sparkle", "shield", "glow"]
        ),
        FoodType.GROWTH_BOOST: FoodProperties(
            points=30,
            duration=0.0,
            color="lime",
            symbol="🌱",
            probability=0.03,
            rarity=FoodRarity.RARE,
            description="Growth boost - instant snake growth",
            effect_strength=3.0,
            spawn_conditions={"min_level": 4},
            visual_effects=["growth", "expand", "glow"]
        ),
        FoodType.MAGNET_FOOD: FoodProperties(
            points=25,
            duration=8.0,
            color="orange",
            symbol="🧲",
            probability=0.025,
            rarity=FoodRarity.EPIC,
            description="Magnet effect - attracts nearby food",
            effect_strength=1.0,
            spawn_conditions={"min_level": 6, "min_score": 200},
            visual_effects=["magnetic", "attract", "pulse"]
        ),
        FoodType.SHIELD_FOOD: FoodProperties(
            points=40,
            duration=0.0,
            color="cyan",
            symbol="🛡️",
            probability=0.02,
            rarity=FoodRarity.EPIC,
            description="Shield - protects from one collision",
            effect_strength=1.0,
            spawn_conditions={"min_level": 7, "min_score": 300},
            visual_effects=["shield", "protect", "glow"]
        ),
        FoodType.TIME_FREEZE: FoodProperties(
            points=50,
            duration=3.0,
            color="light_blue",
            symbol="⏰",
            probability=0.015,
            rarity=FoodRarity.EPIC,
            description="Time freeze - slows down game time",
            effect_strength=0.3,
            spawn_conditions={"min_level": 8, "min_score": 400},
            visual_effects=["freeze", "ice", "crystal"]
        ),
        FoodType.GHOST_MODE: FoodProperties(
            points=45,
            duration=4.0,
            color="transparent",
            symbol="👻",
            probability=0.015,
            rarity=FoodRarity.EPIC,
            description="Ghost mode - pass through walls",
            effect_strength=1.0,
            spawn_conditions={"min_level": 9, "min_score": 500},
            visual_effects=["ghost", "transparent", "fade"]
        ),
        FoodType.EXPLOSIVE_FOOD: FoodProperties(
            points=60,
            duration=0.0,
            color="yellow",
            symbol="💥",
            probability=0.01,
            rarity=FoodRarity.LEGENDARY,
            description="Explosive - clears nearby obstacles",
            effect_strength=1.0,
            spawn_conditions={"min_level": 10, "min_score": 600},
            visual_effects=["explosion", "blast", "fire"]
        ),
        FoodType.TELEPORT_FOOD: FoodProperties(
            points=55,
            duration=0.0,
            color="magenta",
            symbol="🌀",
            probability=0.01,
            rarity=FoodRarity.LEGENDARY,
            description="Teleport - moves snake to random location",
            effect_strength=1.0,
            spawn_conditions={"min_level": 12, "min_score": 800},
            visual_effects=["teleport", "portal", "swirl"]
        ),
        FoodType.RAINBOW_FOOD: FoodProperties(
            points=100,
            duration=15.0,
            color="rainbow",
            symbol="🌈",
            probability=0.005,
            rarity=FoodRarity.LEGENDARY,
            description="Rainbow - all power-ups active",
            effect_strength=2.0,
            spawn_conditions={"min_level": 15, "min_score": 1000},
            visual_effects=["rainbow", "prism", "spectrum"]
        )
    }
    
    def __init__(self, position: Position, food_type: FoodType = FoodType.NORMAL):
        """Initialize a food item."""
        self.position = position
        self.food_type = food_type
        self.properties = self.FOOD_TYPES[food_type]
        self.collected = False
        self.spawn_time = 0.0  # Will be set by the food manager
        self.animation_timer = 0.0
        self.visual_effects = self.properties.visual_effects.copy()
        
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
    
    def get_rarity(self) -> FoodRarity:
        """Get the rarity of this food."""
        return self.properties.rarity
    
    def get_description(self) -> str:
        """Get the description of this food."""
        return self.properties.description
    
    def get_effect_strength(self) -> float:
        """Get the effect strength of this food."""
        return self.properties.effect_strength
    
    def get_visual_effects(self) -> List[str]:
        """Get the visual effects for this food."""
        return self.visual_effects.copy()
    
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
    
    def update_animation(self, delta_time: float) -> None:
        """Update food animation timer."""
        self.animation_timer += delta_time
    
    def get_animation_progress(self) -> float:
        """Get the current animation progress (0.0 to 1.0)."""
        return (self.animation_timer % 2.0) / 2.0  # 2 second cycle
    
    def can_spawn(self, current_score: int, current_level: int) -> bool:
        """Check if this food can spawn based on current game state."""
        conditions = self.properties.spawn_conditions
        
        if "min_score" in conditions and current_score < conditions["min_score"]:
            return False
        
        if "min_level" in conditions and current_level < conditions["min_level"]:
            return False
        
        return True


class EnhancedFoodManager:
    """
    Enhanced food manager with advanced spawning and management.
    
    Handles:
    - Dynamic food spawning based on game state
    - Rarity-based spawning system
    - Food type balancing and progression
    - Special event food spawning
    - Food combination effects
    """
    
    def __init__(self, grid: Grid, max_food: int = 4):
        """Initialize the enhanced food manager."""
        self.grid = grid
        self.max_food = max_food
        self.active_food: List[Food] = []
        self.food_spawn_timer = 0.0
        self.spawn_interval = 2.0  # Seconds between spawns
        
        # Enhanced spawning settings
        self.dynamic_spawning = True
        self.rarity_boosts = {
            FoodRarity.COMMON: 1.0,
            FoodRarity.UNCOMMON: 1.2,
            FoodRarity.RARE: 1.5,
            FoodRarity.EPIC: 2.0,
            FoodRarity.LEGENDARY: 3.0
        }
        
        # Special event settings
        self.special_event_active = False
        self.special_event_timer = 0.0
        self.special_event_duration = 30.0  # 30 seconds
        
        # Food combination tracking
        self.food_combinations = []
        self.combo_timer = 0.0
        self.combo_threshold = 3  # Collect 3 special foods for combo
        
        # Game mode configuration support
        self.spawn_rate_multiplier = 1.0
        
    def _can_food_type_spawn(self, food_type: FoodType, current_score: int, current_level: int) -> bool:
        """Check if a food type can spawn based on current game state."""
        properties = Food.FOOD_TYPES[food_type]
        conditions = properties.spawn_conditions
        
        if "min_score" in conditions and current_score < conditions["min_score"]:
            return False
        
        if "min_level" in conditions and current_level < conditions["min_level"]:
            return False
        
        return True
        
    def spawn_food(self, current_score: int = 0, current_level: int = 1, 
                   force_normal: bool = False) -> Optional[Food]:
        """
        Spawn a new food item with enhanced logic.
        
        Args:
            current_score: Current game score
            current_level: Current game level
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
            food_type = self._select_enhanced_food_type(current_score, current_level)
        
        # Create and add food
        food = Food(position, food_type)
        food.spawn_time = 0.0  # Will be updated by update method
        self.active_food.append(food)
        
        # Mark position as occupied
        self.grid.occupy_position(position)
        
        return food
    
    def _select_enhanced_food_type(self, current_score: int, current_level: int) -> FoodType:
        """Select a food type based on enhanced probabilities and conditions."""
        # Get available food types based on current game state
        available_types = []
        total_probability = 0.0
        
        for food_type, properties in Food.FOOD_TYPES.items():
            if self._can_food_type_spawn(food_type, current_score, current_level):
                # Apply rarity boost
                rarity_boost = self.rarity_boosts.get(properties.rarity, 1.0)
                adjusted_probability = properties.probability * rarity_boost
                
                available_types.append((food_type, adjusted_probability))
                total_probability += adjusted_probability
        
        # Normalize probabilities
        if total_probability > 0:
            normalized_types = []
            for food_type, probability in available_types:
                normalized_prob = probability / total_probability
                normalized_types.append((food_type, normalized_prob))
        else:
            # Fallback to normal food
            return FoodType.NORMAL
        
        # Select food type based on probabilities
        rand = random.random()
        cumulative_prob = 0.0
        
        for food_type, probability in normalized_types:
            cumulative_prob += probability
            if rand <= cumulative_prob:
                return food_type
        
        # Fallback to normal food
        return FoodType.NORMAL
    
    def spawn_special_event_food(self) -> None:
        """Spawn special event food for limited time."""
        if self.special_event_active:
            return
        
        self.special_event_active = True
        self.special_event_timer = 0.0
        
        # Spawn multiple special food items
        for _ in range(3):
            if self.get_active_food_count() < self.max_food:
                self.spawn_food(force_normal=False)
    
    def update(self, delta_time: float, current_score: int = 0, current_level: int = 1) -> None:
        """Update the enhanced food manager."""
        self.food_spawn_timer += delta_time
        
        # Update special event timer
        if self.special_event_active:
            self.special_event_timer += delta_time
            if self.special_event_timer >= self.special_event_duration:
                self.special_event_active = False
        
        # Update food animations
        for food in self.active_food:
            food.update_animation(delta_time)
        
        # Remove collected food
        self.remove_collected_food()
        
        # Spawn new food if needed
        if self.should_spawn_food() and self.food_spawn_timer >= self.spawn_interval:
            if self.spawn_food(current_score, current_level):
                self.food_spawn_timer = 0.0
        
        # Update combo timer
        self.combo_timer += delta_time
        if self.combo_timer > 10.0:  # Reset combo after 10 seconds
            self.food_combinations.clear()
            self.combo_timer = 0.0
    
    def set_spawn_rate_multiplier(self, multiplier: float) -> None:
        """Set the spawn rate multiplier for game mode configuration."""
        self.spawn_rate_multiplier = max(0.1, min(multiplier, 5.0))  # Clamp between 0.1x and 5x
        # Adjust spawn interval based on multiplier
        self.spawn_interval = 2.0 / self.spawn_rate_multiplier
    
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
            
            # Track food combination
            self._track_food_combination(food)
            
            return food
        return None
    
    def _track_food_combination(self, food: Food) -> None:
        """Track food combinations for combo effects."""
        if food.get_rarity() != FoodRarity.COMMON:
            self.food_combinations.append(food.get_food_type())
            self.combo_timer = 0.0
            
            # Check for combo effects
            if len(self.food_combinations) >= self.combo_threshold:
                self._trigger_combo_effect()
    
    def _trigger_combo_effect(self) -> None:
        """Trigger a combo effect based on collected food."""
        # Reset combo
        self.food_combinations.clear()
        
        # Spawn bonus food as combo reward
        if self.get_active_food_count() < self.max_food:
            bonus_position = self.grid.get_random_free_position()
            if bonus_position:
                bonus_food = Food(bonus_position, FoodType.BONUS)
                bonus_food.spawn_time = 0.0
                self.active_food.append(bonus_food)
                self.grid.occupy_position(bonus_position)
    
    def remove_collected_food(self) -> None:
        """Remove all collected food items from the active list."""
        self.active_food = [food for food in self.active_food if not food.is_collected()]
    
    def get_active_food_count(self) -> int:
        """Get the number of active food items."""
        return len([food for food in self.active_food if not food.is_collected()])
    
    def should_spawn_food(self) -> bool:
        """Check if more food should be spawned."""
        return self.get_active_food_count() < self.max_food
    
    def clear_all_food(self) -> None:
        """Clear all food from the grid."""
        for food in self.active_food:
            if not food.is_collected():
                self.grid.free_position(food.get_position())
        self.active_food.clear()
        self.food_spawn_timer = 0.0
        self.special_event_active = False
        self.special_event_timer = 0.0
        self.food_combinations.clear()
        self.combo_timer = 0.0
    
    def get_food_positions(self) -> List[Position]:
        """Get positions of all active food items."""
        return [food.get_position() for food in self.active_food if not food.is_collected()]
    
    def get_food_by_rarity(self, rarity: FoodRarity) -> List[Food]:
        """Get all active food items of a specific rarity."""
        return [food for food in self.active_food 
                if not food.is_collected() and food.get_rarity() == rarity]
    
    def get_food_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about food spawning and collection."""
        total_spawned = len(self.active_food)
        active_count = self.get_active_food_count()
        collected_count = total_spawned - active_count
        
        # Count by rarity
        rarity_counts = {}
        for rarity in FoodRarity:
            rarity_counts[rarity.value] = len(self.get_food_by_rarity(rarity))
        
        # Count by type
        type_counts = {}
        for food in self.active_food:
            food_type = food.get_food_type().value
            type_counts[food_type] = type_counts.get(food_type, 0) + 1
        
        return {
            "total_spawned": total_spawned,
            "active_count": active_count,
            "collected_count": collected_count,
            "max_food": self.max_food,
            "spawn_interval": self.spawn_interval,
            "rarity_counts": rarity_counts,
            "type_counts": type_counts,
            "special_event_active": self.special_event_active,
            "combo_count": len(self.food_combinations),
            "dynamic_spawning": self.dynamic_spawning
        }
    
    def set_max_food(self, max_food: int) -> None:
        """Set the maximum number of food items."""
        self.max_food = max_food
    
    def set_spawn_interval(self, interval: float) -> None:
        """Set the interval between food spawns."""
        self.spawn_interval = interval
    
    def set_dynamic_spawning(self, enabled: bool) -> None:
        """Enable or disable dynamic food spawning."""
        self.dynamic_spawning = enabled
    
    def get_special_event_status(self) -> Dict[str, Any]:
        """Get the current special event status."""
        if self.special_event_active:
            remaining_time = self.special_event_duration - self.special_event_timer
            return {
                "active": True,
                "remaining_time": max(0.0, remaining_time),
                "total_duration": self.special_event_duration
            }
        else:
            return {
                "active": False,
                "remaining_time": 0.0,
                "total_duration": self.special_event_duration
            }
