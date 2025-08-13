"""
Main Game Logic

This module contains the core game logic that orchestrates all game systems:
- Game loop management
- Game over detection
- Game state transitions
- System coordination
"""

from typing import Optional, List, Dict, Any
from .game_state import GameState, GameStatus, GameConfig
from .grid import Grid, Position
from .snake import Snake
from .food import FoodManager, Food
from .collision import CollisionDetector
from .scoring import ScoringSystem


class GameLogic:
    """
    Main game logic controller.
    
    Orchestrates all game systems and manages the game flow.
    """
    
    def __init__(self, config: Optional[GameConfig] = None):
        """Initialize the game logic with optional configuration."""
        self.config = config or GameConfig()
        self.game_state = GameState(config)
        
        # Initialize game systems
        self.grid = Grid(config.grid_width, config.grid_height)
        self.snake = Snake(self.grid.get_grid_center())
        self.food_manager = FoodManager(self.grid)
        self.collision_detector = CollisionDetector(self.grid)
        self.scoring_system = ScoringSystem()
        
        # Game loop variables
        self.last_update_time = 0.0
        self.update_timer = 0.0
        self.game_speed = config.initial_speed
        
        # Initialize game
        self._initialize_game()
    
    def _initialize_game(self) -> None:
        """Initialize the game state and systems."""
        # Clear grid
        self.grid.clear_all_occupied()
        
        # Reset snake
        center = self.grid.get_grid_center()
        self.snake.reset(center)
        
        # Mark snake positions as occupied
        for segment in self.snake.get_body():
            self.grid.occupy_position(segment)
        
        # Spawn initial food
        self.food_manager.spawn_food(force_normal=True)
        
        # Reset scoring
        self.scoring_system.reset_score()
        
        # Set game status
        self.game_state.reset_game()
    
    def update(self, delta_time: float) -> None:
        """
        Update the game logic.
        
        Args:
            delta_time: Time elapsed since last update in seconds
        """
        if not self.game_state.is_game_active():
            return
        
        # Update game time
        self.game_state.update_game_time(delta_time)
        self.scoring_system.update_game_time(delta_time)
        
        # Update food manager
        self.food_manager.update(delta_time)
        
        # Update score multiplier
        self.scoring_system.score_multiplier.update(delta_time)
        
        # Handle game speed and movement
        self._handle_movement(delta_time)
        
        # Check for game over conditions
        self._check_game_over()
    
    def _handle_movement(self, delta_time: float) -> None:
        """Handle snake movement based on game speed."""
        self.update_timer += delta_time
        
        # Calculate movement interval based on game speed
        movement_interval = 1.0 / self.game_speed
        
        if self.update_timer >= movement_interval:
            self.update_timer = 0.0
            
            # Move snake
            if not self._move_snake():
                # Movement failed - game over
                self._handle_game_over("collision")
                return
            
            # Check for food collection
            self._check_food_collection()
            
            # Update game speed based on food eaten
            self._update_game_speed()
    
    def _move_snake(self) -> bool:
        """Move the snake and handle collisions."""
        # Attempt to move snake
        if not self.snake.move(self.grid):
            return False
        
        return True
    
    def _check_food_collection(self) -> None:
        """Check if snake has collected food."""
        head_position = self.snake.get_head()
        food = self.food_manager.collect_food_at_position(head_position)
        
        if food:
            # Snake ate food
            self.snake.grow()
            
            # Add score
            points = self.scoring_system.add_food_score(food.get_effect_type())
            
            # Update game state
            self.game_state.add_score(points)
            
            # Spawn new food
            self.food_manager.spawn_food()
    
    def _update_game_speed(self) -> None:
        """Update game speed based on current level and food eaten."""
        self.game_speed = self.game_state.get_current_speed()
    
    def _check_game_over(self) -> None:
        """Check for game over conditions."""
        if self.game_state.status != GameStatus.PLAYING:
            return
        
        # Check wall collision
        if self.collision_detector.check_snake_wall_collision(self.snake):
            self._handle_game_over("wall")
            return
        
        # Check self collision
        if self.collision_detector.check_snake_self_collision(self.snake):
            self._handle_game_over("self")
            return
        
        # Check if grid is full (snake won)
        if self.grid.is_grid_full():
            self._handle_game_over("victory")
            return
    
    def _handle_game_over(self, reason: str) -> None:
        """Handle game over conditions."""
        self.game_state.end_game()
        
        # Save high score if applicable
        if self.scoring_system.is_new_high_score():
            self.scoring_system.save_high_score()
        
        # Log game over reason
        print(f"Game Over: {reason}")
    
    def change_snake_direction(self, direction: str) -> bool:
        """
        Change the snake's direction.
        
        Args:
            direction: Direction string ('up', 'down', 'left', 'right')
            
        Returns:
            True if direction change was successful
        """
        from .grid import Direction
        
        # Convert string to Direction enum
        direction_map = {
            'up': Direction.UP,
            'down': Direction.DOWN,
            'left': Direction.LEFT,
            'right': Direction.RIGHT,
            'w': Direction.UP,
            's': Direction.DOWN,
            'a': Direction.LEFT,
            'd': Direction.RIGHT
        }
        
        new_direction = direction_map.get(direction.lower())
        if new_direction is None:
            return False
        
        # Check if movement in new direction is valid
        if not self.collision_detector.check_snake_movement_validity(self.snake, new_direction):
            return False
        
        # Change direction
        return self.snake.change_direction(new_direction)
    
    def pause_game(self) -> None:
        """Pause the current game."""
        self.game_state.pause_game()
    
    def resume_game(self) -> None:
        """Resume a paused game."""
        self.game_state.resume_game()
    
    def restart_game(self) -> None:
        """Restart the game."""
        self._initialize_game()
    
    def get_game_status(self) -> GameStatus:
        """Get the current game status."""
        return self.game_state.status
    
    def get_score(self) -> int:
        """Get the current score."""
        return self.scoring_system.get_current_score()
    
    def get_high_score(self) -> int:
        """Get the high score."""
        return self.scoring_system.get_high_score()
    
    def get_level(self) -> int:
        """Get the current level."""
        return self.game_state.level
    
    def get_food_eaten(self) -> int:
        """Get the number of food items eaten."""
        return self.game_state.food_eaten
    
    def get_game_time(self) -> float:
        """Get the current game time."""
        return self.game_state.game_time
    
    def get_snake_length(self) -> int:
        """Get the current snake length."""
        return self.snake.get_length()
    
    def get_snake_body(self) -> List[Position]:
        """Get the snake's body positions."""
        return self.snake.get_body()
    
    def get_food_positions(self) -> List[Position]:
        """Get all active food positions."""
        return self.food_manager.get_food_positions()
    
    def get_game_stats(self) -> Dict[str, Any]:
        """Get comprehensive game statistics."""
        return {
            "status": self.game_state.status.value,
            "score": self.get_score(),
            "high_score": self.get_high_score(),
            "level": self.get_level(),
            "food_eaten": self.get_food_eaten(),
            "game_time": self.get_game_time(),
            "snake_length": self.get_snake_length(),
            "game_speed": self.game_speed,
            "grid_width": self.grid.width,
            "grid_height": self.grid.height
        }
    
    def is_game_active(self) -> bool:
        """Check if the game is currently active."""
        return self.game_state.is_game_active()
    
    def is_game_paused(self) -> bool:
        """Check if the game is paused."""
        return self.game_state.status == GameStatus.PAUSED
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game_state.status == GameStatus.GAME_OVER
    
    def set_difficulty(self, difficulty: str) -> None:
        """Set the game difficulty."""
        from .game_state import Difficulty
        
        difficulty_map = {
            'easy': Difficulty.EASY,
            'medium': Difficulty.MEDIUM,
            'hard': Difficulty.HARD
        }
        
        new_difficulty = difficulty_map.get(difficulty.lower())
        if new_difficulty:
            self.game_state.difficulty = new_difficulty
            self.scoring_system.set_difficulty(difficulty.lower())
    
    def get_difficulty(self) -> str:
        """Get the current game difficulty."""
        return self.game_state.difficulty.value
    
    def get_available_moves(self) -> List[str]:
        """Get all available movement directions for the snake."""
        from .grid import Direction
        
        available_moves = []
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            if self.collision_detector.check_snake_movement_validity(self.snake, direction):
                available_moves.append(direction.name.lower())
        
        return available_moves
