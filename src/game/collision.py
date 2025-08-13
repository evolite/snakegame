"""
Collision Detection System

This module handles all collision detection in the game:
- Snake collision with walls
- Snake collision with itself
- Snake collision with food
- Snake collision with obstacles
- Boundary collision detection
"""

from typing import List, Optional, Tuple
from .grid import Position, Grid
from .snake import Snake
from .food import Food


class CollisionDetector:
    """
    Central collision detection system.
    
    Handles all collision detection logic and provides methods
    to check for various types of collisions.
    """
    
    def __init__(self, grid: Grid):
        """Initialize the collision detector with a game grid."""
        self.grid = grid
    
    def check_wall_collision(self, position: Position) -> bool:
        """
        Check if a position collides with the grid boundaries.
        
        Args:
            position: The position to check
            
        Returns:
            True if collision with wall, False otherwise
        """
        return not self.grid.is_valid_position(position)
    
    def check_snake_wall_collision(self, snake: Snake) -> bool:
        """
        Check if the snake's head collides with a wall.
        
        Args:
            snake: The snake to check
            
        Returns:
            True if collision with wall, False otherwise
        """
        head = snake.get_head()
        return self.check_wall_collision(head)
    
    def check_snake_self_collision(self, snake: Snake) -> bool:
        """
        Check if the snake collides with itself.
        
        Args:
            snake: The snake to check
            
        Returns:
            True if collision with self, False otherwise
        """
        head = snake.get_head()
        body = snake.get_body()
        
        # Check if head position appears in body (excluding head)
        return head in body[1:]
    
    def check_snake_food_collision(self, snake: Snake, food: Food) -> bool:
        """
        Check if the snake's head collides with food.
        
        Args:
            snake: The snake to check
            food: The food to check against
            
        Returns:
            True if collision with food, False otherwise
        """
        if food.is_collected():
            return False
        
        head = snake.get_head()
        return head == food.get_position()
    
    def check_snake_food_collision_at_position(self, snake: Snake, position: Position) -> bool:
        """
        Check if the snake's head collides with food at a specific position.
        
        Args:
            snake: The snake to check
            position: The position to check for food
            
        Returns:
            True if collision with food at position, False otherwise
        """
        head = snake.get_head()
        return head == position
    
    def check_snake_obstacle_collision(self, snake: Snake, obstacles: List[Position]) -> bool:
        """
        Check if the snake collides with any obstacles.
        
        Args:
            snake: The snake to check
            obstacles: List of obstacle positions
            
        Returns:
            True if collision with obstacle, False otherwise
        """
        head = snake.get_head()
        return head in obstacles
    
    def check_snake_snake_collision(self, snake1: Snake, snake2: Snake) -> bool:
        """
        Check if two snakes collide with each other.
        
        Args:
            snake1: First snake
            snake2: Second snake
            
        Returns:
            True if collision between snakes, False otherwise
        """
        # Check if any segment of snake1 collides with snake2
        for segment in snake1.get_body():
            if snake2.check_collision_with_position(segment):
                return True
        
        # Check if any segment of snake2 collides with snake1
        for segment in snake2.get_body():
            if snake1.check_collision_with_position(segment):
                return True
        
        return False
    
    def check_position_occupied(self, position: Position) -> bool:
        """
        Check if a position is occupied by any game object.
        
        Args:
            position: The position to check
            
        Returns:
            True if position is occupied, False otherwise
        """
        return self.grid.is_position_occupied(position)
    
    def check_snake_movement_validity(self, snake: Snake, new_direction: 'Direction') -> bool:
        """
        Check if a snake can move in a specific direction without collision.
        
        Args:
            snake: The snake to check
            new_direction: The direction to check
            
        Returns:
            True if movement is valid, False if collision would occur
        """
        # Calculate new head position
        current_head = snake.get_head()
        new_head = current_head + new_direction.value
        
        # Check wall collision
        if self.check_wall_collision(new_head):
            return False
        
        # Check self collision (excluding tail if snake will move)
        if new_head in snake.get_body()[:-1]:
            return False
        
        # Check if new position is occupied
        if self.check_position_occupied(new_head):
            return False
        
        return True
    
    def get_collision_type(self, snake: Snake, food_list: List[Food], 
                          obstacles: List[Position] = None) -> Optional[str]:
        """
        Determine the type of collision for a snake.
        
        Args:
            snake: The snake to check
            food_list: List of food items to check against
            obstacles: Optional list of obstacle positions
            
        Returns:
            String describing collision type, or None if no collision
        """
        obstacles = obstacles or []
        
        # Check wall collision
        if self.check_snake_wall_collision(snake):
            return "wall"
        
        # Check self collision
        if self.check_snake_self_collision(snake):
            return "self"
        
        # Check obstacle collision
        if self.check_snake_obstacle_collision(snake, obstacles):
            return "obstacle"
        
        # Check food collision
        for food in food_list:
            if self.check_snake_food_collision(snake, food):
                return "food"
        
        return None
    
    def get_collision_positions(self, snake: Snake, food_list: List[Food],
                               obstacles: List[Position] = None) -> List[Position]:
        """
        Get all positions where the snake would collide.
        
        Args:
            snake: The snake to check
            food_list: List of food items
            obstacles: Optional list of obstacle positions
            
        Returns:
            List of collision positions
        """
        obstacles = obstacles or []
        collision_positions = []
        
        # Check all possible movement directions
        for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            # This would need to be implemented with actual Direction enum
            # For now, we'll just check the current head position
            pass
        
        return collision_positions
    
    def is_position_safe_for_snake(self, position: Position, snake: Snake) -> bool:
        """
        Check if a position is safe for the snake to move to.
        
        Args:
            position: The position to check
            snake: The snake that would move there
            
        Returns:
            True if position is safe, False otherwise
        """
        # Check wall collision
        if self.check_wall_collision(position):
            return False
        
        # Check self collision (excluding tail if snake will move)
        if position in snake.get_body()[:-1]:
            return False
        
        # Check if position is occupied
        if self.check_position_occupied(position):
            return False
        
        return True
    
    def get_safe_movements(self, snake: Snake) -> List['Direction']:
        """
        Get all safe movement directions for a snake.
        
        Args:
            snake: The snake to check
            
        Returns:
            List of safe movement directions
        """
        safe_directions = []
        current_head = snake.get_head()
        
        # Check each direction
        for direction_name in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            # This would need proper Direction enum implementation
            # For now, return empty list
            pass
        
        return safe_directions
    
    def predict_collision(self, snake: Snake, steps_ahead: int = 1) -> Optional[str]:
        """
        Predict if a collision will occur in the next N steps.
        
        Args:
            snake: The snake to check
            steps_ahead: Number of steps to look ahead
            
        Returns:
            Collision type if predicted, None otherwise
        """
        # This is a simplified prediction
        # In a full implementation, you'd simulate movement steps
        
        if steps_ahead <= 0:
            return None
        
        # Check immediate collision
        return self.get_collision_type(snake, [])
    
    def get_collision_distance(self, snake: Snake, target: Position) -> int:
        """
        Calculate the distance to a potential collision.
        
        Args:
            snake: The snake to check
            target: The target position
            
        Returns:
            Distance to collision, or -1 if no collision path
        """
        head = snake.get_head()
        return head.manhattan_distance_to(target)
