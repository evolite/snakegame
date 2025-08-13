"""
Snake Game Object

This module contains the Snake class which handles:
- Snake body segments and movement
- Growth mechanics
- Direction changes
- Collision detection with itself
"""

from typing import List, Optional
from .grid import Position, Direction, Grid


class Snake:
    """
    Represents the snake in the game.
    
    The snake is composed of body segments, each with a position.
    The head is always at index 0, and the tail follows.
    """
    
    def __init__(self, start_position: Position, initial_length: int = 3):
        """Initialize the snake with a starting position and length."""
        self.body: List[Position] = []
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.growing = False
        
        # Initialize body segments
        for i in range(initial_length):
            segment = Position(start_position.x - i, start_position.y)
            self.body.append(segment)
    
    def get_head(self) -> Position:
        """Get the position of the snake's head."""
        return self.body[0]
    
    def get_tail(self) -> Position:
        """Get the position of the snake's tail."""
        return self.body[-1]
    
    def get_body(self) -> List[Position]:
        """Get a copy of all body segments."""
        return self.body.copy()
    
    def get_length(self) -> int:
        """Get the current length of the snake."""
        return len(self.body)
    
    def change_direction(self, new_direction: Direction) -> bool:
        """
        Change the snake's direction.
        
        Returns True if the direction change is valid (not 180° turn).
        """
        if Direction.get_opposite(new_direction) == self.direction:
            return False  # Prevent 180° turns
        
        self.next_direction = new_direction
        return True
    
    def move(self, grid: Grid, wrap_around: bool = False) -> bool:
        """
        Move the snake in the current direction.
        
        Args:
            grid: The game grid for boundary checking
            wrap_around: Whether to wrap around grid boundaries
            
        Returns:
            True if movement was successful, False if collision occurred
        """
        # Update direction from queued direction
        self.direction = self.next_direction
        
        # Calculate new head position
        new_head = self.get_head() + self.direction.value
        
        # Handle boundary conditions
        if wrap_around:
            new_head = grid.wrap_position(new_head)
        elif not grid.is_valid_position(new_head):
            return False  # Collision with wall
        
        # Check for self-collision
        if new_head in self.body:
            return False  # Collision with self
        
        # Check if new position is occupied by other objects
        if grid.is_position_occupied(new_head):
            return False  # Collision with obstacle
        
        # Move body segments
        self.body.insert(0, new_head)
        
        # Remove tail unless growing
        if not self.growing:
            tail = self.body.pop()
            grid.free_position(tail)
        else:
            self.growing = False
        
        # Mark new head position as occupied
        grid.occupy_position(new_head)
        
        return True
    
    def grow(self) -> None:
        """Mark the snake to grow on the next move."""
        self.growing = True
    
    def check_collision_with_position(self, position: Position) -> bool:
        """Check if the snake collides with a specific position."""
        return position in self.body
    
    def check_collision_with_snake(self, other_snake: 'Snake') -> bool:
        """Check if this snake collides with another snake."""
        for segment in other_snake.body:
            if self.check_collision_with_position(segment):
                return True
        return False
    
    def reset(self, start_position: Position, initial_length: int = 3) -> None:
        """Reset the snake to initial state."""
        self.body.clear()
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.growing = False
        
        # Initialize body segments
        for i in range(initial_length):
            segment = Position(start_position.x - i, start_position.y)
            self.body.append(segment)
    
    def get_direction_vector(self) -> Position:
        """Get the current direction as a position vector."""
        return self.direction.value
    
    def is_moving_horizontally(self) -> bool:
        """Check if the snake is moving horizontally."""
        return self.direction in [Direction.LEFT, Direction.RIGHT]
    
    def is_moving_vertically(self) -> bool:
        """Check if the snake is moving vertically."""
        return self.direction in [Direction.UP, Direction.DOWN]
    
    def get_movement_speed(self) -> float:
        """Get the current movement speed (can be overridden for power-ups)."""
        return 1.0  # Base speed, can be modified by game state
    
    def can_move_in_direction(self, direction: Direction) -> bool:
        """Check if the snake can move in a specific direction."""
        return Direction.get_opposite(direction) != self.direction
    
    def get_segments_in_direction(self, direction: Direction, count: int = 1) -> List[Position]:
        """Get the next N segments in a specific direction from the head."""
        segments = []
        current_pos = self.get_head()
        
        for _ in range(count):
            current_pos = current_pos + direction.value
            segments.append(current_pos)
        
        return segments
    
    def get_distance_to_tail(self) -> int:
        """Get the Manhattan distance from head to tail."""
        return self.get_head().manhattan_distance_to(self.get_tail())
    
    def is_fully_extended(self) -> bool:
        """Check if the snake is fully extended (no overlapping segments)."""
        return len(set(self.body)) == len(self.body)
