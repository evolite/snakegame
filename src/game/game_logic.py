"""
Main Game Logic

This module contains the core game logic that orchestrates all game systems:
- Game loop management
- Game over detection
- Game state transitions
- System coordination
- Power-ups management
- Enhanced food system integration
- Speed progression system integration
"""

from typing import Optional, List, Dict, Any
from .game_state import GameState, GameStatus, GameConfig
from .grid import Grid, Position
from .snake import Snake
from .food import EnhancedFoodManager, Food, FoodType, FoodRarity
from .collision import CollisionDetector
from .scoring import ScoringSystem
from .power_ups import PowerUpsManager, PowerUpType
from .speed_system import SpeedProgressionSystem, SpeedConfig
from .difficulty_manager import DifficultyManager


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
        self.food_manager = EnhancedFoodManager(self.grid)
        self.collision_detector = CollisionDetector(self.grid)
        self.scoring_system = ScoringSystem()
        self.power_ups_manager = PowerUpsManager()
        
        # Initialize difficulty manager
        self.difficulty_manager = DifficultyManager()
        
        # Initialize speed progression system with difficulty-based settings
        current_settings = self.difficulty_manager.get_current_settings()
        speed_config = SpeedConfig(
            initial_speed=current_settings.initial_speed,
            max_speed=current_settings.max_speed,
            base_increase=current_settings.speed_increase_rate
        )
        self.speed_system = SpeedProgressionSystem(speed_config)
        
        # Game loop variables
        self.last_update_time = 0.0
        self.update_timer = 0.0
        
        # Enhanced food system variables
        self.food_combo_count = 0
        self.last_special_food_time = 0.0
        self.special_food_interval = 60.0  # Spawn special food every 60 seconds
        
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
        self.food_manager.spawn_food(
            current_score=self.game_state.score,
            current_level=self.game_state.level,
            force_normal=True
        )
        
        # Reset scoring
        self.scoring_system.reset_score()
        
        # Reset power-ups
        self.power_ups_manager.clear_all_power_ups()
        
        # Reset speed system
        self.speed_system.reset_speed()
        
        # Reset food system variables
        self.food_combo_count = 0
        self.last_special_food_time = 0.0
        
        # Set game status
        self.game_state.reset_game()
        
        # Update game state difficulty
        self.game_state.difficulty = self.difficulty_manager.get_current_difficulty()
    
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
        
        # Update power-ups manager
        self.power_ups_manager.update(delta_time)
        
        # Update enhanced food manager
        self.food_manager.update(
            delta_time, 
            current_score=self.game_state.score,
            current_level=self.game_state.level
        )
        
        # Update speed progression system
        self.speed_system.update(
            delta_time,
            current_food_eaten=self.game_state.food_eaten,
            current_level=self.game_state.level,
            current_score=self.game_state.score,
            difficulty=self.game_state.difficulty.value
        )
        
        # Update score multiplier
        self.scoring_system.score_multiplier.update(delta_time)
        
        # Handle special food spawning
        self._handle_special_food_spawning(delta_time)
        
        # Handle game speed and movement
        self._handle_movement(delta_time)
        
        # Check for game over conditions
        self._check_game_over()
    
    def _handle_special_food_spawning(self, delta_time: float) -> None:
        """Handle special food spawning based on game progression."""
        self.last_special_food_time += delta_time
        
        # Spawn special event food periodically
        if self.last_special_food_time >= self.special_food_interval:
            self.food_manager.spawn_special_event_food()
            self.last_special_food_time = 0.0
    
    def _handle_movement(self, delta_time: float) -> None:
        """Handle snake movement based on speed progression and power-ups."""
        self.update_timer += delta_time
        
        # Get current speed from speed progression system
        base_speed = self.speed_system.get_current_speed()
        
        # Get speed multiplier from power-ups
        power_up_speed_multiplier = self.power_ups_manager.get_speed_multiplier()
        
        # Calculate final movement speed
        final_speed = base_speed * power_up_speed_multiplier
        
        # Calculate movement interval based on final speed
        movement_interval = 1.0 / final_speed
        
        if self.update_timer >= movement_interval:
            self.update_timer = 0.0
            
            # Move snake
            self._move_snake()
            
            # Check for food collection
            self._check_food_collection()
            
            # Check for collisions
            self._check_collisions()
    
    def _move_snake(self) -> None:
        """Move the snake and handle grid updates."""
        # Get current head position
        old_head = self.snake.get_head()
        
        # Move snake
        new_head = self.snake.move()
        
        if new_head:
            # Free old tail position if snake didn't grow
            if not self.snake.has_grown():
                old_tail = self.snake.get_tail()
                if old_tail:
                    self.grid.free_position(old_tail)
            
            # Mark new head position as occupied
            self.grid.occupy_position(new_head)
            
            # Handle magnet effect
            if self.power_ups_manager.has_magnet_effect():
                self._apply_magnet_effect()
    
    def _check_food_collection(self) -> None:
        """Check if the snake has collected food and handle effects."""
        head_position = self.snake.get_head()
        if not head_position:
            return
        
        # Check for food at head position
        food = self.food_manager.collect_food_at_position(head_position)
        
        if food:
            # Get food properties
            food_type = food.get_effect_type()
            points = food.get_points()
            rarity = food.get_rarity()
            effect_strength = food.get_effect_strength()
            
            # Apply power-up effects based on food type
            self._apply_enhanced_food_effects(food_type, food, effect_strength)
            
            # Apply score multiplier from power-ups
            score_multiplier = self.power_ups_manager.get_score_multiplier()
            adjusted_points = int(points * score_multiplier)
            
            # Add rarity bonus
            rarity_bonus = self._get_rarity_bonus(rarity)
            final_points = int(adjusted_points * rarity_bonus)
            
            # Add speed-based score bonus
            speed_score_bonus = self.speed_system.get_speed_based_score_multiplier()
            final_points = int(final_points * speed_score_bonus)
            
            # Apply difficulty-based scoring multiplier
            difficulty_score = self.difficulty_manager.calculate_difficulty_score(final_points)
            
            # Add score
            self.scoring_system.add_score(difficulty_score)
            self.game_state.add_score(difficulty_score)
            
            # Grow snake
            self._grow_snake(food_type, effect_strength)
            
            # Spawn new food
            self.food_manager.spawn_food(
                current_score=self.game_state.score,
                current_level=self.game_state.level
            )
    
    def _apply_enhanced_food_effects(self, food_type: FoodType, food: Food, effect_strength: float) -> None:
        """
        Apply enhanced effects based on food type.
        
        Args:
            food_type: Type of food collected
            food: The food item
            effect_strength: Strength of the effect
        """
        current_time = self.game_state.game_time
        
        if food_type == FoodType.SPEED_UP:
            # Activate speed boost power-up
            self.power_ups_manager.activate_power_up(PowerUpType.SPEED_BOOST, current_time)
            
        elif food_type == FoodType.SPEED_DOWN:
            # Activate slow motion power-up
            self.power_ups_manager.activate_power_up(PowerUpType.SLOW_MOTION, current_time)
            
        elif food_type == FoodType.DOUBLE_POINTS:
            # Activate double points power-up
            self.power_ups_manager.activate_power_up(PowerUpType.DOUBLE_POINTS, current_time)
            
        elif food_type == FoodType.INVINCIBILITY:
            # Activate invincibility power-up
            self.power_ups_manager.activate_power_up(PowerUpType.INVINCIBILITY, current_time)
            
        elif food_type == FoodType.BONUS:
            # Activate score multiplier power-up
            self.power_ups_manager.activate_power_up(PowerUpType.SCORE_MULTIPLIER, current_time)
            
        elif food_type == FoodType.GROWTH_BOOST:
            # Activate growth boost power-up
            self.power_ups_manager.activate_power_up(PowerUpType.GROWTH_BOOST, current_time)
            
        elif food_type == FoodType.MAGNET_FOOD:
            # Activate magnet power-up
            self.power_ups_manager.activate_power_up(PowerUpType.MAGNET, current_time)
            
        elif food_type == FoodType.SHIELD_FOOD:
            # Activate shield power-up
            self.power_ups_manager.activate_power_up(PowerUpType.SHIELD, current_time)
            
        elif food_type == FoodType.TIME_FREEZE:
            # Activate time freeze effect (custom implementation)
            self._activate_time_freeze_effect(effect_strength)
            
        elif food_type == FoodType.GHOST_MODE:
            # Activate ghost mode effect (custom implementation)
            self._activate_ghost_mode_effect(effect_strength)
            
        elif food_type == FoodType.EXPLOSIVE_FOOD:
            # Activate explosive effect (custom implementation)
            self._activate_explosive_effect(effect_strength)
            
        elif food_type == FoodType.TELEPORT_FOOD:
            # Activate teleport effect (custom implementation)
            self._activate_teleport_effect(effect_strength)
            
        elif food_type == FoodType.RAINBOW_FOOD:
            # Activate rainbow effect - all power-ups
            self._activate_rainbow_effect(effect_strength)
    
    def _activate_time_freeze_effect(self, effect_strength: float) -> None:
        """Activate time freeze effect."""
        # This would slow down the game timer and movement
        # Implementation depends on specific game mechanics
        pass
    
    def _activate_ghost_mode_effect(self, effect_strength: float) -> None:
        """Activate ghost mode effect."""
        # This would allow the snake to pass through walls
        # Implementation depends on collision system
        pass
    
    def _activate_explosive_effect(self, effect_strength: float) -> None:
        """Activate explosive effect."""
        # This would clear nearby obstacles or create explosions
        # Implementation depends on obstacle system
        pass
    
    def _activate_teleport_effect(self, effect_strength: float) -> None:
        """Activate teleport effect."""
        # This would move the snake to a random location
        # Implementation depends on grid system
        pass
    
    def _activate_rainbow_effect(self, effect_strength: float) -> None:
        """Activate rainbow effect - all power-ups active."""
        current_time = self.game_state.game_time
        
        # Activate all available power-ups
        for power_up_type in PowerUpType:
            self.power_ups_manager.activate_power_up(power_up_type, current_time)
    
    def _get_rarity_bonus(self, rarity: FoodRarity) -> float:
        """Get score bonus multiplier based on food rarity."""
        rarity_bonuses = {
            FoodRarity.COMMON: 1.0,
            FoodRarity.UNCOMMON: 1.2,
            FoodRarity.RARE: 1.5,
            FoodRarity.EPIC: 2.0,
            FoodRarity.LEGENDARY: 3.0
        }
        return rarity_bonuses.get(rarity, 1.0)
    
    def _grow_snake(self, food_type: FoodType, effect_strength: float) -> None:
        """
        Grow the snake based on food type and power-ups.
        
        Args:
            food_type: Type of food that was collected
            effect_strength: Strength of the effect
        """
        # Get growth multiplier from power-ups
        growth_multiplier = self.power_ups_manager.get_growth_multiplier()
        
        # Calculate growth amount
        base_growth = 1
        if food_type == FoodType.BONUS:
            base_growth = 2
        elif food_type == FoodType.INVINCIBILITY:
            base_growth = 2
        elif food_type == FoodType.GROWTH_BOOST:
            base_growth = int(effect_strength)
        
        # Apply growth multiplier
        total_growth = int(base_growth * growth_multiplier)
        
        # Grow snake
        for _ in range(total_growth):
            self.snake.grow()
            
            # Mark new segment position as occupied
            new_segment = self.snake.get_tail()
            if new_segment:
                self.grid.occupy_position(new_segment)
    
    def _apply_magnet_effect(self) -> None:
        """Apply magnet effect to attract nearby food."""
        if not self.power_ups_manager.has_magnet_effect():
            return
        
        head_position = self.snake.get_head()
        if not head_position:
            return
        
        # Get all food positions
        food_positions = self.food_manager.get_food_positions()
        
        # Check for food within magnet range
        magnet_range = 3  # 3 cells radius
        
        for food_pos in food_positions:
            distance = abs(food_pos.x - head_position.x) + abs(food_pos.y - head_position.y)
            
            if distance <= magnet_range and distance > 0:
                # Move food towards snake head
                self._move_food_towards_head(food_pos, head_position)
    
    def _move_food_towards_head(self, food_pos: Position, head_pos: Position) -> None:
        """
        Move food one step towards the snake head.
        
        Args:
            food_pos: Current food position
            head_pos: Snake head position
        """
        # Calculate direction to head
        dx = 0
        dy = 0
        
        if food_pos.x < head_pos.x:
            dx = 1
        elif food_pos.x > head_pos.x:
            dx = -1
            
        if food_pos.y < head_pos.y:
            dy = 1
        elif food_pos.y > head_pos.y:
            dy = -1
        
        # Calculate new position
        new_x = food_pos.x + dx
        new_y = food_pos.y + dy
        
        # Check if new position is free
        new_pos = Position(new_x, new_y)
        if self.grid.is_position_free(new_pos):
            # Move food to new position
            self.grid.free_position(food_pos)
            self.grid.occupy_position(new_pos)
            
            # Update food position in food manager
            # Note: This would require modifying the food manager to support position updates
    
    def _check_collisions(self) -> None:
        """Check for collisions and handle them."""
        head_position = self.snake.get_head()
        if not head_position:
            return
        
        # Check if snake is invincible
        if self.power_ups_manager.is_invincible():
            return
        
        # Check wall collision
        if self.collision_detector.check_wall_collision(head_position):
            self._handle_collision()
            return
        
        # Check self collision
        if self.collision_detector.check_self_collision(self.snake):
            self._handle_collision()
            return
    
    def _handle_collision(self) -> None:
        """Handle collision events."""
        # Check if shield is active
        if self.power_ups_manager.has_power_up(PowerUpType.SHIELD):
            # Consume shield
            self.power_ups_manager.deactivate_power_up(PowerUpType.SHIELD)
            return
        
        # Game over
        self.game_state.end_game()
    
    def _check_game_over(self) -> None:
        """Check for game over conditions."""
        if self.game_state.status == GameStatus.GAME_OVER:
            # Game over logic
            pass
    
    def get_power_ups_manager(self) -> PowerUpsManager:
        """Get the power-ups manager."""
        return self.power_ups_manager
    
    def get_game_state(self) -> GameState:
        """Get the current game state."""
        return self.game_state
    
    def get_snake(self) -> Snake:
        """Get the snake instance."""
        return self.snake
    
    def get_food_manager(self) -> EnhancedFoodManager:
        """Get the enhanced food manager."""
        return self.food_manager
    
    def get_scoring_system(self) -> ScoringSystem:
        """Get the scoring system."""
        return self.scoring_system
    
    def get_speed_system(self) -> SpeedProgressionSystem:
        """Get the speed progression system."""
        return self.speed_system
    
    def get_current_speed(self) -> float:
        """Get the current game speed including power-up effects."""
        base_speed = self.speed_system.get_current_speed()
        power_up_multiplier = self.power_ups_manager.get_speed_multiplier()
        return base_speed * power_up_multiplier
    
    def get_current_score_multiplier(self) -> float:
        """Get the current score multiplier including power-up effects."""
        base_multiplier = self.scoring_system.score_multiplier.get_multiplier()
        power_up_multiplier = self.power_ups_manager.get_score_multiplier()
        return base_multiplier * power_up_multiplier
    
    def get_food_statistics(self) -> Dict[str, Any]:
        """Get comprehensive food statistics."""
        return self.food_manager.get_food_statistics()
    
    def get_special_event_status(self) -> Dict[str, Any]:
        """Get the current special event status."""
        return self.food_manager.get_special_event_status()
    
    def get_speed_statistics(self) -> Dict[str, Any]:
        """Get comprehensive speed statistics."""
        return self.speed_system.get_speed_statistics()
    
    def get_speed_progression_info(self) -> Dict[str, Any]:
        """Get speed progression information."""
        return self.speed_system.get_speed_progression_info()
    
    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self._initialize_game()
    
    def pause_game(self) -> None:
        """Pause the game."""
        self.game_state.pause_game()
    
    def resume_game(self) -> None:
        """Resume the game."""
        self.game_state.resume_game()
    
    def end_game(self) -> None:
        """End the current game."""
        self.game_state.end_game()
    
    def change_snake_direction(self, direction: str) -> bool:
        """
        Change the snake's direction.
        
        Args:
            direction: New direction ('up', 'down', 'left', 'right')
            
        Returns:
            True if direction was changed, False otherwise
        """
        # Map direction strings to snake direction enum
        direction_mapping = {
            'up': 'UP',
            'down': 'DOWN',
            'left': 'LEFT',
            'right': 'RIGHT'
        }
        
        if direction.lower() in direction_mapping:
            new_direction = direction_mapping[direction.lower()]
            return self.snake.change_direction(new_direction)
        
        return False
    
    def get_game_status(self) -> GameStatus:
        """Get the current game status."""
        return self.game_state.status
    
    def get_score(self) -> int:
        """Get the current score."""
        return self.game_state.score
    
    def get_high_score(self) -> int:
        """Get the high score."""
        return self.game_state.high_score
    
    def get_level(self) -> int:
        """Get the current level."""
        return self.game_state.level
    
    def get_food_eaten(self) -> int:
        """Get the number of food items eaten."""
        return self.game_state.food_eaten
    
    def get_game_time(self) -> float:
        """Get the current game time."""
        return self.game_state.game_time
    
    # Speed system control methods
    
    def set_speed_progression_type(self, progression_type: str) -> None:
        """Set the speed progression algorithm."""
        from .speed_system import SpeedProgressionType
        type_mapping = {
            'linear': SpeedProgressionType.LINEAR,
            'exponential': SpeedProgressionType.EXPONENTIAL,
            'logarithmic': SpeedProgressionType.LOGARITHMIC,
            'stepped': SpeedProgressionType.STEPPED,
            'custom': SpeedProgressionType.CUSTOM
        }
        
        if progression_type.lower() in type_mapping:
            self.speed_system.set_progression_type(type_mapping[progression_type.lower()])
    
    def set_speed_transition_type(self, transition_type: str) -> None:
        """Set the speed transition type."""
        from .speed_system import SpeedTransitionType
        type_mapping = {
            'instant': SpeedTransitionType.INSTANT,
            'smooth': SpeedTransitionType.SMOOTH,
            'ease_in': SpeedTransitionType.EASE_IN,
            'ease_out': SpeedTransitionType.EASE_OUT,
            'ease_in_out': SpeedTransitionType.EASE_IN_OUT
        }
        
        if transition_type.lower() in type_mapping:
            self.speed_system.set_transition_type(type_mapping[transition_type.lower()])
    
    def set_speed_multiplier(self, multiplier: float) -> None:
        """Set the speed multiplier."""
        self.speed_system.set_speed_multiplier(multiplier)
    
    def enable_speed_progression(self, enabled: bool) -> None:
        """Enable or disable speed progression."""
        self.speed_system.enable_speed_progression(enabled)
    
    def get_speed_difficulty_rating(self) -> str:
        """Get the current speed difficulty rating."""
        return self.speed_system.get_speed_difficulty_rating()
    
    # Difficulty management methods
    
    def set_difficulty(self, difficulty: str) -> None:
        """Set the game difficulty level."""
        from .game_state import Difficulty
        difficulty_mapping = {
            'easy': Difficulty.EASY,
            'medium': Difficulty.MEDIUM,
            'hard': Difficulty.HARD
        }
        
        if difficulty.lower() in difficulty_mapping:
            new_difficulty = difficulty_mapping[difficulty.lower()]
            self.difficulty_manager.set_difficulty(new_difficulty)
            
            # Update speed system with new difficulty settings
            current_settings = self.difficulty_manager.get_current_settings()
            self.speed_system.set_initial_speed(current_settings.initial_speed)
            self.speed_system.set_max_speed(current_settings.max_speed)
            self.speed_system.set_base_increase(current_settings.speed_increase_rate)
            
            # Update game state
            self.game_state.difficulty = new_difficulty
    
    def get_current_difficulty(self) -> str:
        """Get the current difficulty level."""
        return self.difficulty_manager.get_current_difficulty().value
    
    def get_difficulty_settings(self) -> Dict:
        """Get the current difficulty settings."""
        return self.difficulty_manager.get_difficulty_comparison()
    
    def get_difficulty_stats(self) -> Dict:
        """Get difficulty usage statistics."""
        return self.difficulty_manager.get_difficulty_stats()
    
    def calculate_difficulty_score(self, base_score: int) -> int:
        """Calculate the final score based on difficulty multiplier."""
        return self.difficulty_manager.calculate_difficulty_score(base_score)
    
    def get_difficulty_display_info(self) -> Dict:
        """Get display information for the current difficulty."""
        current_difficulty = self.difficulty_manager.get_current_difficulty()
        return {
            'name': self.difficulty_manager.get_difficulty_display_name(current_difficulty),
            'description': self.difficulty_manager.get_difficulty_description(current_difficulty),
            'color': self.difficulty_manager.get_difficulty_color(current_difficulty),
            'icon': self.difficulty_manager.get_difficulty_icon(current_difficulty)
        }
