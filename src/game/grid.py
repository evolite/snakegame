"""
Grid Management System

This module handles the game grid, coordinate system, and spatial relationships.
It provides utilities for grid-based movement, boundary checking, and position calculations.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import random
from enum import Enum


@dataclass(frozen=True)
class Position:
    """Represents a 2D grid position."""
    x: int
    y: int
    
    def __add__(self, other: 'Position') -> 'Position':
        """Add two positions together."""
        return Position(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Position') -> 'Position':
        """Subtract one position from another."""
        return Position(self.x - other.x, self.y - other.y)
    
    def __eq__(self, other: object) -> bool:
        """Check if two positions are equal."""
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        """Make Position hashable for use in sets and dictionaries."""
        return hash((self.x, self.y))
    
    def distance_to(self, other: 'Position') -> float:
        """Calculate Euclidean distance to another position."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def manhattan_distance_to(self, other: 'Position') -> int:
        """Calculate Manhattan distance to another position."""
        return abs(self.x - other.x) + abs(self.y - other.y)


class Direction(Enum):
    """Enumeration of movement directions."""
    UP = Position(0, -1)
    DOWN = Position(0, 1)
    LEFT = Position(-1, 0)
    RIGHT = Position(1, 0)
    
    @classmethod
    def get_opposite(cls, direction: 'Direction') -> 'Direction':
        """Get the opposite direction."""
        opposites = {
            cls.UP: cls.DOWN,
            cls.DOWN: cls.UP,
            cls.LEFT: cls.RIGHT,
            cls.RIGHT: cls.LEFT
        }
        return opposites[direction]
    
    @classmethod
    def from_string(cls, direction_str: str) -> Optional['Direction']:
        """Create a direction from a string representation."""
        direction_map = {
            'up': cls.UP,
            'down': cls.DOWN,
            'left': cls.LEFT,
            'right': cls.RIGHT,
            'w': cls.UP,
            's': cls.DOWN,
            'a': cls.LEFT,
            'd': cls.RIGHT
        }
        return direction_map.get(direction_str.lower())


class Grid:
    """
    Game grid management system.
    
    Handles grid boundaries, position validation, and provides utilities
    for grid-based operations.
    """
    
    def __init__(self, width: int, height: int):
        """Initialize the grid with specified dimensions."""
        self.width = width
        self.height = height
        self._occupied_positions: set[Position] = set()
        
    def is_valid_position(self, position: Position) -> bool:
        """Check if a position is within the grid boundaries."""
        return 0 <= position.x < self.width and 0 <= position.y < self.height
    
    def is_position_occupied(self, position: Position) -> bool:
        """Check if a position is occupied by an object."""
        return position in self._occupied_positions
    
    def is_position_free(self, position: Position) -> bool:
        """Check if a position is free (not occupied)."""
        return not self.is_position_occupied(position)
    
    def occupy_position(self, position: Position) -> bool:
        """Mark a position as occupied. Returns False if already occupied."""
        if self.is_position_occupied(position):
            return False
        self._occupied_positions.add(position)
        return True
    
    def free_position(self, position: Position) -> bool:
        """Mark a position as free. Returns False if not occupied."""
        if not self.is_position_occupied(position):
            return False
        self._occupied_positions.remove(position)
        return True
    
    def get_random_free_position(self) -> Optional[Position]:
        """Get a random unoccupied position on the grid."""
        free_positions = []
        for x in range(self.width):
            for y in range(self.height):
                pos = Position(x, y)
                if not self.is_position_occupied(pos):
                    free_positions.append(pos)
        
        if not free_positions:
            return None
        
        return random.choice(free_positions)
    
    def get_neighbors(self, position: Position, include_diagonals: bool = False) -> List[Position]:
        """Get valid neighboring positions."""
        neighbors = []
        
        # Cardinal directions
        directions = [
            Direction.UP.value,
            Direction.DOWN.value,
            Direction.LEFT.value,
            Direction.RIGHT.value
        ]
        
        # Add diagonal directions if requested
        if include_diagonals:
            directions.extend([
                Position(-1, -1),  # Top-left
                Position(1, -1),   # Top-right
                Position(-1, 1),   # Bottom-left
                Position(1, 1)     # Bottom-right
            ])
        
        for direction in directions:
            neighbor = position + direction
            if self.is_valid_position(neighbor):
                neighbors.append(neighbor)
        
        return neighbors
    
    def clear_all_occupied(self) -> None:
        """Clear all occupied positions."""
        self._occupied_positions.clear()
    
    def get_occupied_count(self) -> int:
        """Get the number of occupied positions."""
        return len(self._occupied_positions)
    
    def get_free_count(self) -> int:
        """Get the number of free positions."""
        return (self.width * self.height) - len(self._occupied_positions)
    
    def is_grid_full(self) -> bool:
        """Check if the grid is completely full."""
        return len(self._occupied_positions) >= (self.width * self.height)
    
    def get_grid_center(self) -> Position:
        """Get the center position of the grid."""
        return Position(self.width // 2, self.height // 2)
    
    def wrap_position(self, position: Position) -> Position:
        """Wrap a position around the grid boundaries (for wraparound mode)."""
        x = position.x % self.width
        y = position.y % self.height
        return Position(x, y)
