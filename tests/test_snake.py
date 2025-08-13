"""
Unit tests for Snake Mechanics.

Tests the Snake class including:
- Initialization and setup
- Movement mechanics
- Growth and shrinking
- Direction changes
- Collision detection
- Boundary handling
"""

import pytest
from src.game.snake import Snake
from src.game.grid import Position, Direction, Grid


class TestSnake:
    """Test the Snake class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.grid = Grid(20, 15)
        self.start_position = Position(10, 7)  # Center of grid
        self.snake = Snake(self.start_position)
    
    def test_snake_initialization(self):
        """Test Snake initialization."""
        assert len(self.snake.body) == 3  # Default initial length
        assert self.snake.direction == Direction.RIGHT
        assert not self.snake.growing
        
        # Check initial body positions (should be in a line to the left)
        expected_body = [
            Position(10, 7),  # Head
            Position(9, 7),   # Body
            Position(8, 7),   # Tail
        ]
        
        assert self.snake.body == expected_body
    
    def test_snake_initialization_with_custom_position(self):
        """Test Snake initialization with custom starting position."""
        start_pos = Position(5, 5)
        snake = Snake(start_pos)
        
        expected_body = [
            Position(5, 5),  # Head
            Position(4, 5),  # Body
            Position(3, 5),  # Tail
        ]
        
        assert snake.body == expected_body
        assert snake.direction == Direction.RIGHT
    
    def test_snake_initialization_with_custom_length(self):
        """Test Snake initialization with custom length."""
        snake = Snake(self.start_position, initial_length=5)
        
        assert len(snake.body) == 5
        assert not snake.growing
        
        # Check that all body segments are in a line
        expected_body = [
            Position(10, 7),  # Head
            Position(9, 7),   # Body
            Position(8, 7),   # Body
            Position(7, 7),   # Body
            Position(6, 7),   # Tail
        ]
        
        assert snake.body == expected_body
    
    def test_snake_get_head(self):
        """Test getting the snake's head position."""
        head = self.snake.get_head()
        assert head == self.snake.body[0]
        assert head == Position(10, 7)
    
    def test_snake_get_tail(self):
        """Test getting the snake's tail position."""
        tail = self.snake.get_tail()
        assert tail == self.snake.body[-1]
        assert tail == Position(8, 7)
    
    def test_snake_get_body(self):
        """Test getting a copy of the snake's body."""
        body_copy = self.snake.get_body()
        assert body_copy == self.snake.body
        assert body_copy is not self.snake.body  # Should be a copy
    
    def test_snake_change_direction(self):
        """Test changing snake direction."""
        # Change to valid direction
        result = self.snake.change_direction(Direction.UP)
        assert result is True
        assert self.snake.next_direction == Direction.UP
        
        # Move to apply the direction change
        self.snake.move(self.grid)
        assert self.snake.direction == Direction.UP
        
        # Change to another valid direction
        result = self.snake.change_direction(Direction.LEFT)
        assert result is True
        assert self.snake.next_direction == Direction.LEFT
        
        # Move to apply the direction change
        self.snake.move(self.grid)
        assert self.snake.direction == Direction.LEFT
    
    def test_snake_change_direction_to_opposite(self):
        """Test that snake cannot change to opposite direction."""
        initial_direction = self.snake.direction
        
        # Try to change to opposite direction
        result = self.snake.change_direction(Direction.LEFT)
        
        # Direction change should be rejected
        assert result is False
        assert self.snake.next_direction == Direction.RIGHT  # Should not change
    
    def test_snake_change_direction_to_same(self):
        """Test that snake can change to the same direction."""
        initial_direction = self.snake.direction
        
        # Change to same direction
        result = self.snake.change_direction(initial_direction)
        
        # Direction change should be accepted
        assert result is True
        assert self.snake.next_direction == initial_direction
    
    def test_snake_move(self):
        """Test basic snake movement."""
        initial_head = self.snake.get_head()
        initial_body = self.snake.body.copy()
        
        # Move snake
        result = self.snake.move(self.grid)
        
        # Movement should be successful
        assert result is True
        
        # Head should move in current direction
        new_head = self.snake.get_head()
        expected_head = initial_head + Direction.RIGHT.value
        assert new_head == expected_head
        
        # Body should follow (each segment moves to previous segment's position)
        assert self.snake.body[1] == initial_body[0]  # Body follows head
        assert self.snake.body[2] == initial_body[1]  # Tail follows body
    
    def test_snake_move_in_different_direction(self):
        """Test snake movement in different directions."""
        # Change direction and move
        self.snake.change_direction(Direction.UP)
        initial_head = self.snake.get_head()
        
        self.snake.move(self.grid)
        
        new_head = self.snake.get_head()
        expected_head = initial_head + Direction.UP.value
        assert new_head == expected_head
    
    def test_snake_grow(self):
        """Test snake growth."""
        initial_length = len(self.snake.body)
        
        # Mark snake to grow
        self.snake.grow()
        assert self.snake.growing is True
        
        # Move snake (should grow)
        self.snake.move(self.grid)
        
        # Length should increase by 1
        assert len(self.snake.body) == initial_length + 1
        assert self.snake.growing is False
    
    def test_snake_grow_multiple_times(self):
        """Test multiple snake growths."""
        initial_length = len(self.snake.body)
        
        # Grow multiple times
        for i in range(3):
            self.snake.grow()
            self.snake.move(self.grid)
            assert len(self.snake.body) == initial_length + i + 1
    
    def test_snake_move_with_wrap_around(self):
        """Test snake movement with wrap around."""
        # Move snake to edge
        while self.snake.get_head().x < self.grid.width - 1:
            self.snake.move(self.grid)
        
        # Now at right edge, next move should wrap around
        result = self.snake.move(self.grid, wrap_around=True)
        assert result is True
        
        # Head should be at left side
        head = self.snake.get_head()
        assert head.x == 0
    
    def test_snake_move_without_wrap_around(self):
        """Test snake movement without wrap around."""
        # Move snake to edge
        while self.snake.get_head().x < self.grid.width - 1:
            self.snake.move(self.grid)
        
        # Now at right edge, next move should fail without wrap around
        result = self.snake.move(self.grid, wrap_around=False)
        assert result is False
    
    def test_snake_check_collision_with_position(self):
        """Test collision detection with specific position."""
        # Check collision with head
        head = self.snake.get_head()
        assert self.snake.check_collision_with_position(head) is True
        
        # Check collision with body
        body = self.snake.body[1]
        assert self.snake.check_collision_with_position(body) is True
        
        # Check collision with empty position
        empty_pos = Position(0, 0)
        assert self.snake.check_collision_with_position(empty_pos) is False
    
    def test_snake_check_collision_with_other_snake(self):
        """Test collision detection with another snake."""
        other_snake = Snake(Position(15, 10))
        
        # Initially no collision
        assert not self.snake.check_collision_with_snake(other_snake)
        
        # Move other snake to overlap
        other_snake.body[0] = self.snake.get_head()
        
        # Now there should be a collision
        assert self.snake.check_collision_with_snake(other_snake)
    
    def test_snake_reset(self):
        """Test resetting the snake."""
        # Modify snake state
        self.snake.grow()
        self.snake.change_direction(Direction.DOWN)
        self.snake.move(self.grid)
        
        # Reset snake
        self.snake.reset(self.start_position)
        
        # Should be back to initial state
        assert len(self.snake.body) == 3
        assert self.snake.direction == Direction.RIGHT
        assert not self.snake.growing
        
        # Check body positions are reset
        expected_body = [
            Position(10, 7),  # Head
            Position(9, 7),   # Body
            Position(8, 7),   # Tail
        ]
        
        assert self.snake.body == expected_body
    
    def test_snake_reset_with_custom_position(self):
        """Test resetting snake with custom position."""
        custom_pos = Position(5, 5)
        self.snake.reset(custom_pos)
        
        expected_body = [
            Position(5, 5),  # Head
            Position(4, 5),  # Body
            Position(3, 5),  # Tail
        ]
        
        assert self.snake.body == expected_body
    
    def test_snake_reset_with_custom_length(self):
        """Test resetting snake with custom length."""
        self.snake.reset(self.start_position, initial_length=5)
        
        assert len(self.snake.body) == 5
        expected_body = [
            Position(10, 7),  # Head
            Position(9, 7),   # Body
            Position(8, 7),   # Body
            Position(7, 7),   # Body
            Position(6, 7),   # Tail
        ]
        
        assert self.snake.body == expected_body
    
    def test_snake_get_length(self):
        """Test getting snake length."""
        assert self.snake.get_length() == 3
        
        # Grow and check length
        self.snake.grow()
        self.snake.move(self.grid)
        assert self.snake.get_length() == 4
    
    def test_snake_direction_vector(self):
        """Test getting direction vector."""
        vector = self.snake.get_direction_vector()
        assert vector == Direction.RIGHT.value
        assert vector == Position(1, 0)
    
    def test_snake_movement_direction_checks(self):
        """Test movement direction checks."""
        # Initially moving right
        assert self.snake.is_moving_horizontally() is True
        assert self.snake.is_moving_vertically() is False
        
        # Change to vertical movement
        self.snake.change_direction(Direction.UP)
        self.snake.move(self.grid)
        
        assert self.snake.is_moving_horizontally() is False
        assert self.snake.is_moving_vertically() is True
    
    def test_snake_can_move_in_direction(self):
        """Test checking if snake can move in specific direction."""
        # Can move in perpendicular directions
        assert self.snake.can_move_in_direction(Direction.UP) is True
        assert self.snake.can_move_in_direction(Direction.DOWN) is True
        
        # Cannot move in opposite direction
        assert self.snake.can_move_in_direction(Direction.LEFT) is False
    
    def test_snake_get_segments_in_direction(self):
        """Test getting segments in a specific direction."""
        segments = self.snake.get_segments_in_direction(Direction.RIGHT, 2)
        
        head = self.snake.get_head()
        expected_segments = [
            head + Direction.RIGHT.value,
            head + Direction.RIGHT.value + Direction.RIGHT.value
        ]
        
        assert segments == expected_segments
    
    def test_snake_distance_to_tail(self):
        """Test getting distance to tail."""
        distance = self.snake.get_distance_to_tail()
        assert distance == 2  # Manhattan distance from head to tail
    
    def test_snake_is_fully_extended(self):
        """Test checking if snake is fully extended."""
        # Initially fully extended
        assert self.snake.is_fully_extended() is True
        
        # Create overlapping segments
        self.snake.body[1] = self.snake.body[0]
        
        # Now not fully extended
        assert self.snake.is_fully_extended() is False


if __name__ == "__main__":
    pytest.main([__file__])
