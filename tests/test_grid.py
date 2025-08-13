"""
Unit tests for Grid System.

Tests the core grid components including:
- Position dataclass
- Direction enum
- Grid class
"""

import pytest
from src.game.grid import Position, Direction, Grid


class TestPosition:
    """Test the Position dataclass."""
    
    def test_position_creation(self):
        """Test creating Position objects."""
        pos = Position(5, 10)
        assert pos.x == 5
        assert pos.y == 10
    
    def test_position_equality(self):
        """Test Position equality comparison."""
        pos1 = Position(5, 10)
        pos2 = Position(5, 10)
        pos3 = Position(5, 11)
        
        assert pos1 == pos2
        assert pos1 != pos3
        assert pos1 != (5, 10)  # Different types
    
    def test_position_hash(self):
        """Test that Position objects can be hashed."""
        pos1 = Position(5, 10)
        pos2 = Position(5, 10)
        
        # Should be hashable
        hash(pos1)
        hash(pos2)
        
        # Equal positions should have same hash
        assert hash(pos1) == hash(pos2)
    
    def test_position_repr(self):
        """Test Position string representation."""
        pos = Position(5, 10)
        assert repr(pos) == "Position(x=5, y=10)"
        assert str(pos) == "Position(x=5, y=10)"
    
    def test_position_arithmetic(self):
        """Test Position arithmetic operations."""
        pos1 = Position(3, 4)
        pos2 = Position(1, 2)
        
        # Addition
        result = pos1 + pos2
        assert result == Position(4, 6)
        
        # Subtraction
        result = pos1 - pos2
        assert result == Position(2, 2)
    
    def test_position_distance_calculations(self):
        """Test distance calculation methods."""
        pos1 = Position(0, 0)
        pos2 = Position(3, 4)
        
        # Euclidean distance
        euclidean = pos1.distance_to(pos2)
        assert euclidean == 5.0  # sqrt(3^2 + 4^2)
        
        # Manhattan distance
        manhattan = pos1.manhattan_distance_to(pos2)
        assert manhattan == 7  # 3 + 4


class TestDirection:
    """Test the Direction enum."""
    
    def test_direction_values(self):
        """Test that all expected direction values exist."""
        assert Direction.UP.value == Position(0, -1)
        assert Direction.DOWN.value == Position(0, 1)
        assert Direction.LEFT.value == Position(-1, 0)
        assert Direction.RIGHT.value == Position(1, 0)
    
    def test_direction_enumeration(self):
        """Test that all direction values can be enumerated."""
        directions = list(Direction)
        assert len(directions) == 4
        assert Direction.UP in directions
        assert Direction.DOWN in directions
        assert Direction.LEFT in directions
        assert Direction.RIGHT in directions
    
    def test_direction_opposites(self):
        """Test that opposite directions are correctly identified."""
        assert Direction.get_opposite(Direction.UP) == Direction.DOWN
        assert Direction.get_opposite(Direction.DOWN) == Direction.UP
        assert Direction.get_opposite(Direction.LEFT) == Direction.RIGHT
        assert Direction.get_opposite(Direction.RIGHT) == Direction.LEFT
    
    def test_direction_from_string(self):
        """Test creating directions from string representations."""
        # Basic directions
        assert Direction.from_string("up") == Direction.UP
        assert Direction.from_string("down") == Direction.DOWN
        assert Direction.from_string("left") == Direction.LEFT
        assert Direction.from_string("right") == Direction.RIGHT
        
        # WASD keys
        assert Direction.from_string("w") == Direction.UP
        assert Direction.from_string("s") == Direction.DOWN
        assert Direction.from_string("a") == Direction.LEFT
        assert Direction.from_string("d") == Direction.RIGHT
        
        # Case insensitive
        assert Direction.from_string("UP") == Direction.UP
        assert Direction.from_string("Up") == Direction.UP
        
        # Invalid strings
        assert Direction.from_string("invalid") is None
        assert Direction.from_string("") is None


class TestGrid:
    """Test the Grid class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.grid = Grid(10, 8)
    
    def test_grid_initialization(self):
        """Test Grid initialization."""
        assert self.grid.width == 10
        assert self.grid.height == 8
        assert self.grid.get_occupied_count() == 0
        assert self.grid.get_free_count() == 80  # 10 * 8
    
    def test_grid_position_validation(self):
        """Test checking if positions are within grid bounds."""
        # Valid positions
        assert self.grid.is_valid_position(Position(0, 0))
        assert self.grid.is_valid_position(Position(9, 7))  # width-1, height-1
        assert self.grid.is_valid_position(Position(5, 4))
        
        # Invalid positions
        assert not self.grid.is_valid_position(Position(-1, 0))  # Negative x
        assert not self.grid.is_valid_position(Position(0, -1))  # Negative y
        assert not self.grid.is_valid_position(Position(10, 0))  # x >= width
        assert not self.grid.is_valid_position(Position(0, 8))   # y >= height
        assert not self.grid.is_valid_position(Position(15, 10)) # Both out of bounds
    
    def test_grid_position_occupancy(self):
        """Test position occupancy management."""
        pos = Position(5, 4)
        
        # Initially free
        assert not self.grid.is_position_occupied(pos)
        
        # Occupy position
        assert self.grid.occupy_position(pos)
        assert self.grid.is_position_occupied(pos)
        assert self.grid.get_occupied_count() == 1
        assert self.grid.get_free_count() == 79
        
        # Try to occupy again
        assert not self.grid.occupy_position(pos)
        
        # Free position
        assert self.grid.free_position(pos)
        assert not self.grid.is_position_occupied(pos)
        assert self.grid.get_occupied_count() == 0
        assert self.grid.get_free_count() == 80
        
        # Try to free again
        assert not self.grid.free_position(pos)
    
    def test_grid_wrapping(self):
        """Test position wrapping around grid boundaries."""
        # Test wrapping functionality
        wrapped = self.grid.wrap_position(Position(15, 12))
        assert wrapped == Position(5, 4)  # 15 % 10 = 5, 12 % 8 = 4
        
        wrapped = self.grid.wrap_position(Position(-3, -2))
        assert wrapped == Position(7, 6)  # -3 % 10 = 7, -2 % 8 = 6
        
        wrapped = self.grid.wrap_position(Position(0, 0))
        assert wrapped == Position(0, 0)  # No wrapping needed
    
    def test_grid_get_random_free_position(self):
        """Test getting random free positions."""
        # Initially all positions are free
        for _ in range(100):  # Test multiple random positions
            pos = self.grid.get_random_free_position()
            assert pos is not None
            assert self.grid.is_valid_position(pos)
            assert not self.grid.is_position_occupied(pos)
        
        # Occupy all positions
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                self.grid.occupy_position(Position(x, y))
        
        # No free positions left
        assert self.grid.get_random_free_position() is None
        assert self.grid.is_grid_full()
        
        # Clear and test again
        self.grid.clear_all_occupied()
        pos = self.grid.get_random_free_position()
        assert pos is not None
        assert self.grid.is_valid_position(pos)
    
    def test_grid_get_neighbors(self):
        """Test getting neighboring positions."""
        center = Position(5, 4)
        neighbors = self.grid.get_neighbors(center)
        
        # Should have 4 neighbors (up, down, left, right)
        assert len(neighbors) == 4
        
        # Check specific neighbors
        expected_neighbors = [
            Position(5, 3),  # up
            Position(5, 5),  # down
            Position(4, 4),  # left
            Position(6, 4),  # right
        ]
        
        for expected in expected_neighbors:
            assert expected in neighbors
    
    def test_grid_get_neighbors_with_diagonals(self):
        """Test getting neighbors including diagonal positions."""
        center = Position(5, 4)
        neighbors = self.grid.get_neighbors(center, include_diagonals=True)
        
        # Should have 8 neighbors (4 adjacent + 4 diagonal)
        assert len(neighbors) == 8
        
        # Check adjacent neighbors
        adjacent = [
            Position(5, 3),  # up
            Position(5, 5),  # down
            Position(4, 4),  # left
            Position(6, 4),  # right
        ]
        
        # Check diagonal neighbors
        diagonal = [
            Position(4, 3),  # up-left
            Position(6, 3),  # up-right
            Position(4, 5),  # down-left
            Position(6, 5),  # down-right
        ]
        
        for pos in adjacent + diagonal:
            assert pos in neighbors
    
    def test_grid_get_neighbors_at_edge(self):
        """Test getting neighbors at grid edge."""
        center = Position(0, 0)  # Top-left corner
        neighbors = self.grid.get_neighbors(center)
        
        # Should have only 2 neighbors (down and right)
        assert len(neighbors) == 2
        
        expected_neighbors = [
            Position(0, 1),  # down
            Position(1, 0),  # right
        ]
        
        for expected in expected_neighbors:
            assert expected in neighbors
    
    def test_grid_get_neighbors_with_diagonals_at_edge(self):
        """Test getting diagonal neighbors at grid edge."""
        center = Position(0, 0)  # Top-left corner
        neighbors = self.grid.get_neighbors(center, include_diagonals=True)
        
        # Should have only 3 neighbors (down, right, down-right)
        assert len(neighbors) == 3
        
        expected_neighbors = [
            Position(0, 1),  # down
            Position(1, 0),  # right
            Position(1, 1),  # down-right
        ]
        
        for expected in expected_neighbors:
            assert expected in neighbors
    
    def test_grid_center(self):
        """Test getting grid center position."""
        # Even dimensions
        center = self.grid.get_grid_center()
        assert center == Position(5, 4)  # 10//2 = 5, 8//2 = 4
        
        # Odd dimensions
        odd_grid = Grid(5, 5)
        center = odd_grid.get_grid_center()
        assert center == Position(2, 2)  # 5//2 = 2
    
    def test_grid_clear_all_occupied(self):
        """Test clearing all occupied positions."""
        # Occupy some positions
        positions = [Position(0, 0), Position(1, 1), Position(2, 2)]
        for pos in positions:
            self.grid.occupy_position(pos)
        
        assert self.grid.get_occupied_count() == 3
        
        # Clear all
        self.grid.clear_all_occupied()
        assert self.grid.get_occupied_count() == 0
        assert self.grid.get_free_count() == 80
        
        # All positions should be free
        for pos in positions:
            assert not self.grid.is_position_occupied(pos)


if __name__ == "__main__":
    pytest.main([__file__])
