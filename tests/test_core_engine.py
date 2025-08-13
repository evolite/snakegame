"""
Tests for the core game engine components.

This module tests the fundamental game systems to ensure they work correctly.
"""

import pytest
from src.game.game_state import GameState, GameStatus, GameConfig
from src.game.grid import Grid, Position
from src.game.grid import Direction
from src.game.snake import Snake
from src.game.food import EnhancedFoodManager, Food, FoodType
from src.game.collision import CollisionDetector
from src.game.scoring import ScoringSystem
from src.game.game_logic import GameLogic


class TestGameState:
    """Test the game state management system."""
    
    def test_initial_state(self):
        """Test initial game state."""
        state = GameState()
        assert state.status == GameStatus.MENU
        assert state.score == 0
        assert state.level == 1
        assert state.food_eaten == 0
    
    def test_reset_game(self):
        """Test game reset functionality."""
        state = GameState()
        state.score = 100
        state.food_eaten = 5
        state.reset_game()
        assert state.status == GameStatus.PLAYING
        assert state.score == 0
        assert state.food_eaten == 0
    
    def test_pause_resume(self):
        """Test pause and resume functionality."""
        state = GameState()
        state.reset_game()
        assert state.can_pause()
        
        state.pause_game()
        assert state.status == GameStatus.PAUSED
        assert state.can_resume()
        
        state.resume_game()
        assert state.status == GameStatus.PLAYING


class TestGrid:
    """Test the grid management system."""
    
    def test_grid_creation(self):
        """Test grid creation with dimensions."""
        grid = Grid(10, 20)
        assert grid.width == 10
        assert grid.height == 20
    
    def test_position_validation(self):
        """Test position validation."""
        grid = Grid(10, 10)
        valid_pos = Position(5, 5)
        invalid_pos = Position(15, 15)
        
        assert grid.is_valid_position(valid_pos)
        assert not grid.is_valid_position(invalid_pos)
    
    def test_position_occupancy(self):
        """Test position occupancy tracking."""
        grid = Grid(10, 10)
        pos = Position(5, 5)
        
        assert not grid.is_position_occupied(pos)
        grid.occupy_position(pos)
        assert grid.is_position_occupied(pos)
        grid.free_position(pos)
        assert not grid.is_position_occupied(pos)


class TestSnake:
    """Test the snake game object."""
    
    def test_snake_creation(self):
        """Test snake creation."""
        pos = Position(5, 5)
        snake = Snake(pos)
        assert snake.get_head() == pos
        assert snake.get_length() == 3
    
    def test_snake_movement(self):
        """Test snake movement."""
        grid = Grid(10, 10)
        snake = Snake(Position(5, 5))
        
        # Mark initial positions as occupied
        for segment in snake.get_body():
            grid.occupy_position(segment)
        
        # Test movement
        assert snake.move(grid)
        assert snake.get_head() == Position(6, 5)  # Moving right
    
    def test_direction_change(self):
        """Test snake direction changes."""
        snake = Snake(Position(5, 5))
        
        # Test valid direction change
        assert snake.change_direction(Direction.UP)
        
        # Test invalid direction change (180° turn)
        assert not snake.change_direction(Direction.LEFT)  # LEFT is opposite of RIGHT (initial direction)


class TestFood:
    """Test the food system."""
    
    def test_food_creation(self):
        """Test food creation."""
        pos = Position(5, 5)
        food = Food(pos, FoodType.NORMAL)
        assert food.get_position() == pos
        assert food.get_points() == 10
        assert not food.is_collected()
    
    def test_food_collection(self):
        """Test food collection."""
        food = Food(Position(5, 5))
        food.collect()
        assert food.is_collected()


class TestFoodManager:
    """Test the food manager."""
    
    def test_food_spawning(self):
        """Test food spawning."""
        grid = Grid(10, 10)
        manager = EnhancedFoodManager(grid)
        
        food = manager.spawn_food(force_normal=True)
        assert food is not None
        assert food.get_effect_type() == FoodType.NORMAL


class TestCollisionDetector:
    """Test the collision detection system."""
    
    def test_wall_collision(self):
        """Test wall collision detection."""
        grid = Grid(10, 10)
        detector = CollisionDetector(grid)
        
        valid_pos = Position(5, 5)
        invalid_pos = Position(15, 15)
        
        assert not detector.check_wall_collision(valid_pos)
        assert detector.check_wall_collision(invalid_pos)
    
    def test_snake_self_collision(self):
        """Test snake self-collision detection."""
        grid = Grid(10, 10)
        detector = CollisionDetector(grid)
        snake = Snake(Position(5, 5))
        
        # Snake shouldn't collide with itself initially
        assert not detector.check_snake_self_collision(snake)


class TestScoringSystem:
    """Test the scoring system."""
    
    def test_score_initialization(self):
        """Test scoring system initialization."""
        scoring = ScoringSystem()
        assert scoring.get_current_score() == 0
        assert scoring.get_high_score() == 0
    
    def test_food_scoring(self):
        """Test food scoring."""
        scoring = ScoringSystem()
        initial_score = scoring.get_current_score()
        
        points = scoring.add_food_score(FoodType.NORMAL)
        assert points == 10
        assert scoring.get_current_score() == initial_score + 10


class TestGameLogic:
    """Test the main game logic."""
    
    def test_game_logic_creation(self):
        """Test game logic initialization."""
        config = GameConfig()
        logic = GameLogic(config)
        assert logic.get_game_status().value == "playing"
        assert logic.get_score() == 0
    
    def test_direction_change(self):
        """Test snake direction changes through game logic."""
        config = GameConfig()
        logic = GameLogic(config)
        
        # Test valid direction change
        assert logic.change_snake_direction('up')
        
        # Test invalid direction change
        assert not logic.change_snake_direction('invalid')


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
