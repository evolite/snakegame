"""
Obstacles and Walls System

This module implements a comprehensive obstacles and walls system that provides:
- Multiple obstacle types with unique behaviors
- Dynamic obstacle spawning and management
- Collision detection and handling
- Strategic gameplay enhancement
- Visual differentiation and effects
"""

from typing import List, Optional, Dict, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import random
import math
from .grid import Position, Grid


class ObstacleType(Enum):
    """Enumeration of obstacle types."""
    STATIC_WALL = "static_wall"
    BREAKABLE_WALL = "breakable_wall"
    MOVING_OBSTACLE = "moving_obstacle"
    SPIKE_TRAP = "spike_trap"
    TELEPORTER = "teleporter"
    SPEED_PAD = "speed_pad"
    SCORE_MULTIPLIER = "score_multiplier"
    SAFE_ZONE = "safe_zone"


class ObstacleBehavior(Enum):
    """Enumeration of obstacle behaviors."""
    SOLID = "solid"           # Blocks movement completely
    BREAKABLE = "breakable"   # Can be destroyed
    MOVING = "moving"         # Moves around the grid
    HAZARDOUS = "hazardous"   # Causes damage or game over
    BENEFICIAL = "beneficial" # Provides positive effects
    TELEPORTING = "teleporting" # Moves snake to different location


@dataclass
class ObstacleProperties:
    """Properties of an obstacle."""
    obstacle_type: ObstacleType
    behavior: ObstacleBehavior
    health: int = 1  # For breakable obstacles
    damage: int = 0  # Damage to snake if hazardous
    points: int = 0  # Points awarded for interaction
    duration: float = 0.0  # Duration of effect (0 for permanent)
    movement_speed: float = 0.0  # Movement speed for moving obstacles
    movement_pattern: str = "static"  # Movement pattern type
    visual_effect: str = "none"  # Visual effect to apply
    sound_effect: str = "none"  # Sound effect to play


class Obstacle:
    """
    Represents an obstacle or wall in the game.
    
    Obstacles can have different types, behaviors, and effects on gameplay.
    """
    
    # Obstacle type definitions with their properties
    OBSTACLE_TYPES = {
        ObstacleType.STATIC_WALL: ObstacleProperties(
            obstacle_type=ObstacleType.STATIC_WALL,
            behavior=ObstacleBehavior.SOLID,
            points=0,
            visual_effect="wall"
        ),
        ObstacleType.BREAKABLE_WALL: ObstacleProperties(
            obstacle_type=ObstacleType.BREAKABLE_WALL,
            behavior=ObstacleBehavior.BREAKABLE,
            health=3,
            points=10,
            visual_effect="breakable"
        ),
        ObstacleType.MOVING_OBSTACLE: ObstacleProperties(
            obstacle_type=ObstacleType.MOVING_OBSTACLE,
            behavior=ObstacleBehavior.MOVING,
            movement_speed=2.0,
            movement_pattern="patrol",
            points=5,
            visual_effect="moving"
        ),
        ObstacleType.SPIKE_TRAP: ObstacleProperties(
            obstacle_type=ObstacleType.SPIKE_TRAP,
            behavior=ObstacleBehavior.HAZARDOUS,
            damage=1,
            points=15,
            visual_effect="spikes"
        ),
        ObstacleType.TELEPORTER: ObstacleProperties(
            obstacle_type=ObstacleType.TELEPORTER,
            behavior=ObstacleBehavior.TELEPORTING,
            points=20,
            visual_effect="teleporter"
        ),
        ObstacleType.SPEED_PAD: ObstacleProperties(
            obstacle_type=ObstacleType.SPEED_PAD,
            behavior=ObstacleBehavior.BENEFICIAL,
            points=5,
            duration=3.0,
            visual_effect="speed_pad"
        ),
        ObstacleType.SCORE_MULTIPLIER: ObstacleProperties(
            obstacle_type=ObstacleType.SCORE_MULTIPLIER,
            behavior=ObstacleBehavior.BENEFICIAL,
            points=25,
            duration=5.0,
            visual_effect="multiplier"
        ),
        ObstacleType.SAFE_ZONE: ObstacleProperties(
            obstacle_type=ObstacleType.SAFE_ZONE,
            behavior=ObstacleBehavior.BENEFICIAL,
            points=0,
            duration=8.0,
            visual_effect="safe_zone"
        )
    }
    
    def __init__(self, position: Position, obstacle_type: ObstacleType = ObstacleType.STATIC_WALL):
        """Initialize an obstacle."""
        self.position = position
        self.obstacle_type = obstacle_type
        self.properties = self.OBSTACLE_TYPES[obstacle_type]
        
        # State variables
        self.health = self.properties.health
        self.active = True
        self.creation_time = 0.0
        self.last_movement_time = 0.0
        
        # Movement variables for moving obstacles
        self.movement_direction = (1, 0)  # Default right direction
        self.movement_timer = 0.0
        self.patrol_points: List[Position] = []
        self.current_patrol_index = 0
        
        # Effect variables
        self.effect_timer = 0.0
        self.effect_active = False
        
        # Visual state
        self.animation_timer = 0.0
        self.visual_state = "normal"
    
    def get_position(self) -> Position:
        """Get the obstacle's position."""
        return self.position
    
    def get_type(self) -> ObstacleType:
        """Get the obstacle type."""
        return self.obstacle_type
    
    def get_behavior(self) -> ObstacleBehavior:
        """Get the obstacle's behavior."""
        return self.properties.behavior
    
    def is_active(self) -> bool:
        """Check if the obstacle is active."""
        return self.active
    
    def is_solid(self) -> bool:
        """Check if the obstacle blocks movement."""
        return self.properties.behavior == ObstacleBehavior.SOLID
    
    def is_breakable(self) -> bool:
        """Check if the obstacle can be destroyed."""
        return self.properties.behavior == ObstacleBehavior.BREAKABLE
    
    def is_moving(self) -> bool:
        """Check if the obstacle moves."""
        return self.properties.behavior == ObstacleBehavior.MOVING
    
    def is_hazardous(self) -> bool:
        """Check if the obstacle is dangerous."""
        return self.properties.behavior == ObstacleBehavior.HAZARDOUS
    
    def is_beneficial(self) -> bool:
        """Check if the obstacle provides benefits."""
        return self.properties.behavior == ObstacleBehavior.BENEFICIAL
    
    def get_health(self) -> int:
        """Get the obstacle's current health."""
        return self.health
    
    def get_damage(self) -> int:
        """Get the damage this obstacle causes."""
        return self.properties.damage
    
    def get_points(self) -> int:
        """Get the points awarded for this obstacle."""
        return self.properties.points
    
    def take_damage(self, damage: int) -> bool:
        """
        Apply damage to the obstacle.
        
        Returns:
            True if obstacle was destroyed, False otherwise
        """
        if not self.is_breakable():
            return False
        
        self.health -= damage
        if self.health <= 0:
            self.active = False
            return True
        
        return False
    
    def update(self, delta_time: float, grid: Grid) -> None:
        """Update the obstacle's state."""
        if not self.active:
            return
        
        # Update timers
        self.animation_timer += delta_time
        self.movement_timer += delta_time
        
        # Handle moving obstacles
        if self.is_moving():
            self._update_movement(delta_time, grid)
        
        # Handle temporary effects
        if self.properties.duration > 0:
            self._update_effects(delta_time)
    
    def _update_movement(self, delta_time: float, grid: Grid) -> None:
        """Update movement for moving obstacles."""
        if self.movement_timer < 1.0 / self.properties.movement_speed:
            return
        
        self.movement_timer = 0.0
        
        # Get new position based on movement pattern
        new_position = self._calculate_new_position(grid)
        
        if new_position and new_position != self.position:
            # Update grid occupancy
            grid.free_position(self.position)
            grid.occupy_position(new_position)
            self.position = new_position
    
    def _calculate_new_position(self, grid: Grid) -> Optional[Position]:
        """Calculate the new position for moving obstacles."""
        if self.properties.movement_pattern == "patrol":
            return self._calculate_patrol_position(grid)
        elif self.properties.movement_pattern == "bounce":
            return self._calculate_bounce_position(grid)
        elif self.properties.movement_pattern == "circular":
            return self._calculate_circular_position(grid)
        else:
            return self._calculate_random_position(grid)
    
    def _calculate_patrol_position(self, grid: Grid) -> Optional[Position]:
        """Calculate patrol movement position."""
        if not self.patrol_points:
            # Generate patrol points if none exist
            self._generate_patrol_points(grid)
        
        if not self.patrol_points:
            return None
        
        # Move towards next patrol point
        target = self.patrol_points[self.current_patrol_index]
        dx = target.x - self.position.x
        dy = target.y - self.position.y
        
        # Simple movement towards target
        new_x = self.position.x + (1 if dx > 0 else -1 if dx < 0 else 0)
        new_y = self.position.y + (1 if dy > 0 else -1 if dy < 0 else 0)
        
        new_pos = Position(new_x, new_y)
        
        # Check if reached target
        if new_pos == target:
            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
        
        # Validate new position
        if grid.is_position_valid(new_pos) and grid.is_position_free(new_pos):
            return new_pos
        
        return None
    
    def _calculate_bounce_position(self, grid: Grid) -> Optional[Position]:
        """Calculate bounce movement position."""
        new_x = self.position.x + self.movement_direction[0]
        new_y = self.position.y + self.movement_direction[1]
        
        # Check boundaries and bounce
        if new_x < 0 or new_x >= grid.width:
            self.movement_direction = (-self.movement_direction[0], self.movement_direction[1])
            new_x = self.position.x + self.movement_direction[0]
        
        if new_y < 0 or new_y >= grid.height:
            self.movement_direction = (self.movement_direction[0], -self.movement_direction[1])
            new_y = self.position.y + self.movement_direction[1]
        
        new_pos = Position(new_x, new_y)
        
        # Validate new position
        if grid.is_position_valid(new_pos) and grid.is_position_free(new_pos):
            return new_pos
        
        return None
    
    def _calculate_circular_position(self, grid: Grid) -> Optional[Position]:
        """Calculate circular movement position."""
        # Simple circular movement
        angle = self.animation_timer * 2.0  # 2 radians per second
        radius = 3
        
        center_x = grid.width // 2
        center_y = grid.height // 2
        
        new_x = int(center_x + radius * math.cos(angle))
        new_y = int(center_y + radius * math.sin(angle))
        
        new_pos = Position(new_x, new_y)
        
        # Validate new position
        if grid.is_position_valid(new_pos) and grid.is_position_free(new_pos):
            return new_pos
        
        return None
    
    def _calculate_random_position(self, grid: Grid) -> Optional[Position]:
        """Calculate random movement position."""
        # Random movement in current direction
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        for _ in range(4):  # Try all directions
            direction = random.choice(directions)
            new_x = self.position.x + direction[0]
            new_y = self.position.y + direction[1]
            
            new_pos = Position(new_x, new_y)
            
            if grid.is_position_valid(new_pos) and grid.is_position_free(new_pos):
                self.movement_direction = direction
                return new_pos
        
        return None
    
    def _generate_patrol_points(self, grid: Grid) -> None:
        """Generate patrol points for moving obstacles."""
        self.patrol_points = []
        
        # Generate 3-5 patrol points
        num_points = random.randint(3, 5)
        
        for _ in range(num_points):
            attempts = 0
            while attempts < 10:
                x = random.randint(1, grid.width - 2)
                y = random.randint(1, grid.height - 2)
                
                pos = Position(x, y)
                if grid.is_position_free(pos):
                    self.patrol_points.append(pos)
                    break
                attempts += 1
        
        if self.patrol_points:
            self.current_patrol_index = 0
    
    def _update_effects(self, delta_time: float) -> None:
        """Update temporary effects."""
        self.effect_timer += delta_time
        
        if self.effect_timer >= self.properties.duration:
            self.effect_active = False
            self.effect_timer = 0.0
    
    def activate_effect(self) -> Dict[str, Any]:
        """Activate the obstacle's effect and return effect data."""
        if not self.is_beneficial():
            return {}
        
        self.effect_active = True
        self.effect_timer = 0.0
        
        effect_data = {
            "type": self.obstacle_type.value,
            "points": self.properties.points,
            "duration": self.properties.duration,
            "effect": self.properties.visual_effect
        }
        
        return effect_data
    
    def get_visual_state(self) -> str:
        """Get the current visual state of the obstacle."""
        if not self.active:
            return "destroyed"
        
        if self.effect_active:
            return "active"
        
        if self.is_moving() and self.movement_timer > 0.5:
            return "moving"
        
        return "normal"
    
    def get_animation_progress(self) -> float:
        """Get the current animation progress (0.0 to 1.0)."""
        return (self.animation_timer % 2.0) / 2.0  # 2 second cycle


class ObstacleManager:
    """
    Manages all obstacles and walls in the game.
    
    Handles:
    - Obstacle spawning and placement
    - Dynamic obstacle management
    - Collision detection
    - Obstacle effects and interactions
    """
    
    def __init__(self, grid: Grid, max_obstacles: int = 15):
        """Initialize the obstacle manager."""
        self.grid = grid
        self.max_obstacles = max_obstacles
        self.active_obstacles: List[Obstacle] = []
        self.obstacle_spawn_timer = 0.0
        self.spawn_interval = 5.0  # Seconds between spawns
        
        # Obstacle spawning settings
        self.obstacle_spawning_enabled = True
        self.difficulty_scaling = True
        self.obstacle_density = 0.1  # 10% of grid can be obstacles
        
        # Obstacle type probabilities
        self.obstacle_probabilities = {
            ObstacleType.STATIC_WALL: 0.4,
            ObstacleType.BREAKABLE_WALL: 0.2,
            ObstacleType.MOVING_OBSTACLE: 0.15,
            ObstacleType.SPIKE_TRAP: 0.1,
            ObstacleType.TELEPORTER: 0.05,
            ObstacleType.SPEED_PAD: 0.05,
            ObstacleType.SCORE_MULTIPLIER: 0.03,
            ObstacleType.SAFE_ZONE: 0.02
        }
        
        # Obstacle placement rules
        self.placement_rules = {
            "min_distance_from_snake": 3,  # Minimum distance from snake
            "max_obstacles_per_row": 3,     # Maximum obstacles per row/column
            "avoid_center": True,           # Avoid placing obstacles in center
            "maintain_paths": True          # Ensure paths remain accessible
        }
    
    def spawn_obstacles(self, num_obstacles: int = 1, 
                       obstacle_types: Optional[List[ObstacleType]] = None) -> List[Obstacle]:
        """
        Spawn new obstacles.
        
        Args:
            num_obstacles: Number of obstacles to spawn
            obstacle_types: Specific obstacle types to spawn (None for random)
            
        Returns:
            List of spawned obstacles
        """
        spawned_obstacles = []
        
        for _ in range(num_obstacles):
            if len(self.active_obstacles) >= self.max_obstacles:
                break
            
            # Select obstacle type
            if obstacle_types:
                obstacle_type = random.choice(obstacle_types)
            else:
                obstacle_type = self._select_obstacle_type()
            
            # Find valid position
            position = self._find_valid_obstacle_position(obstacle_type)
            
            if position:
                # Create and add obstacle
                obstacle = Obstacle(position, obstacle_type)
                self.active_obstacles.append(obstacle)
                
                # Mark position as occupied
                self.grid.occupy_position(position)
                
                spawned_obstacles.append(obstacle)
        
        return spawned_obstacles
    
    def _select_obstacle_type(self) -> ObstacleType:
        """Select an obstacle type based on probabilities."""
        rand = random.random()
        cumulative_prob = 0.0
        
        for obstacle_type, probability in self.obstacle_probabilities.items():
            cumulative_prob += probability
            if rand <= cumulative_prob:
                return obstacle_type
        
        # Fallback to static wall
        return ObstacleType.STATIC_WALL
    
    def _find_valid_obstacle_position(self, obstacle_type: ObstacleType) -> Optional[Position]:
        """Find a valid position for an obstacle."""
        attempts = 0
        max_attempts = 50
        
        while attempts < max_attempts:
            x = random.randint(0, self.grid.width - 1)
            y = random.randint(0, self.grid.height - 1)
            
            position = Position(x, y)
            
            if self._is_valid_obstacle_position(position, obstacle_type):
                return position
            
            attempts += 1
        
        return None
    
    def _is_valid_obstacle_position(self, position: Position, obstacle_type: ObstacleType) -> bool:
        """Check if a position is valid for an obstacle."""
        # Check if position is free
        if not self.grid.is_position_free(position):
            return False
        
        # Check placement rules
        if not self._check_placement_rules(position, obstacle_type):
            return False
        
        # Check if obstacle type has special requirements
        if obstacle_type == ObstacleType.MOVING_OBSTACLE:
            return self._check_moving_obstacle_requirements(position)
        elif obstacle_type == ObstacleType.TELEPORTER:
            return self._check_teleporter_requirements(position)
        
        return True
    
    def _check_placement_rules(self, position: Position, obstacle_type: ObstacleType) -> bool:
        """Check if obstacle placement follows the rules."""
        # Check minimum distance from snake (if snake exists)
        if self.placement_rules["min_distance_from_snake"] > 0:
            # This would need access to snake position
            pass
        
        # Check maximum obstacles per row/column
        if self.placement_rules["max_obstacles_per_row"] > 0:
            row_count = sum(1 for obs in self.active_obstacles if obs.position.y == position.y)
            col_count = sum(1 for obs in self.active_obstacles if obs.position.x == position.x)
            
            if row_count >= self.placement_rules["max_obstacles_per_row"] or \
               col_count >= self.placement_rules["max_obstacles_per_row"]:
                return False
        
        # Avoid center if specified
        if self.placement_rules["avoid_center"]:
            center_x = self.grid.width // 2
            center_y = self.grid.height // 2
            center_distance = abs(position.x - center_x) + abs(position.y - center_y)
            
            if center_distance < 3:
                return False
        
        return True
    
    def _check_moving_obstacle_requirements(self, position: Position) -> bool:
        """Check if position is suitable for moving obstacles."""
        # Moving obstacles need some free space around them
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                check_pos = Position(position.x + dx, position.y + dy)
                if self.grid.is_position_valid(check_pos) and not self.grid.is_position_free(check_pos):
                    return False
        
        return True
    
    def _check_teleporter_requirements(self, position: Position) -> bool:
        """Check if position is suitable for teleporters."""
        # Teleporters need to be placed in accessible areas
        # This is a simplified check
        return True
    
    def update(self, delta_time: float) -> None:
        """Update all obstacles."""
        self.obstacle_spawn_timer += delta_time
        
        # Update active obstacles
        for obstacle in self.active_obstacles[:]:  # Copy list to avoid modification during iteration
            obstacle.update(delta_time, self.grid)
            
            # Remove destroyed obstacles
            if not obstacle.active:
                self._remove_obstacle(obstacle)
        
        # Spawn new obstacles if needed
        if (self.obstacle_spawning_enabled and 
            self.obstacle_spawn_timer >= self.spawn_interval and
            len(self.active_obstacles) < self.max_obstacles):
            
            if self.spawn_obstacles():
                self.obstacle_spawn_timer = 0.0
    
    def _remove_obstacle(self, obstacle: Obstacle) -> None:
        """Remove an obstacle from the game."""
        if obstacle in self.active_obstacles:
            self.active_obstacles.remove(obstacle)
            self.grid.free_position(obstacle.position)
    
    def get_obstacle_at_position(self, position: Position) -> Optional[Obstacle]:
        """Get obstacle at a specific position, if any."""
        for obstacle in self.active_obstacles:
            if obstacle.position == position and obstacle.active:
                return obstacle
        return None
    
    def check_collision(self, position: Position) -> Tuple[bool, Optional[Obstacle]]:
        """
        Check for collision with obstacles at a position.
        
        Returns:
            Tuple of (collision_detected, obstacle_if_collision)
        """
        obstacle = self.get_obstacle_at_position(position)
        if obstacle:
            return True, obstacle
        return False, None
    
    def get_obstacle_positions(self) -> List[Position]:
        """Get positions of all active obstacles."""
        return [obstacle.position for obstacle in self.active_obstacles if obstacle.active]
    
    def get_obstacles_by_type(self, obstacle_type: ObstacleType) -> List[Obstacle]:
        """Get all obstacles of a specific type."""
        return [obstacle for obstacle in self.active_obstacles 
                if obstacle.active and obstacle.obstacle_type == obstacle_type]
    
    def clear_all_obstacles(self) -> None:
        """Clear all obstacles from the grid."""
        for obstacle in self.active_obstacles:
            self.grid.free_position(obstacle.position)
        self.active_obstacles.clear()
        self.obstacle_spawn_timer = 0.0
    
    def get_obstacle_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about obstacles."""
        type_counts = {}
        for obstacle_type in ObstacleType:
            type_counts[obstacle_type.value] = len(self.get_obstacles_by_type(obstacle_type))
        
        return {
            "total_obstacles": len(self.active_obstacles),
            "active_obstacles": len([obs for obs in self.active_obstacles if obs.active]),
            "max_obstacles": self.max_obstacles,
            "spawn_interval": self.spawn_interval,
            "spawning_enabled": self.obstacle_spawning_enabled,
            "difficulty_scaling": self.difficulty_scaling,
            "obstacle_density": self.obstacle_density,
            "type_counts": type_counts
        }
    
    def set_max_obstacles(self, max_obstacles: int) -> None:
        """Set the maximum number of obstacles."""
        self.max_obstacles = max_obstacles
    
    def set_spawn_interval(self, interval: float) -> None:
        """Set the interval between obstacle spawns."""
        self.spawn_interval = interval
    
    def set_obstacle_spawning(self, enabled: bool) -> None:
        """Enable or disable obstacle spawning."""
        self.obstacle_spawning_enabled = enabled
    
    def set_difficulty_scaling(self, enabled: bool) -> None:
        """Enable or disable difficulty-based obstacle scaling."""
        self.difficulty_scaling = enabled
    
    def set_obstacle_density(self, density: float) -> None:
        """Set the obstacle density (0.0 to 1.0)."""
        self.obstacle_density = max(0.0, min(1.0, density))
