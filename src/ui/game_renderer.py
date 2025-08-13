"""
Game Renderer

This module handles the rendering of all game elements:
- Snake visualization
- Food rendering
- Grid and background
- HUD and UI elements
"""

import pygame
from typing import List, Tuple
from ..game.grid import Position
from ..game.snake import Snake
from ..game.food import Food, FoodType
from .display import DisplayManager


class GameRenderer:
    """
    Handles the rendering of all game elements.
    
    This class is responsible for drawing:
    - The game grid and background
    - The snake and its segments
    - Food items
    - HUD elements (score, level, etc.)
    - UI overlays
    """
    
    def __init__(self, display_manager: DisplayManager):
        """Initialize the game renderer."""
        self.display = display_manager
        self.cell_size = display_manager.get_cell_size()
        
        # Snake rendering settings
        self.snake_colors = {
            'head': 'green',
            'body': 'lime',
            'tail': 'olive',
            'outline': 'dark_gray'
        }
        
        # Food rendering settings
        self.food_colors = {
            FoodType.NORMAL: 'red',
            FoodType.BONUS: 'gold',
            FoodType.SPEED_UP: 'blue',
            FoodType.SPEED_DOWN: 'purple',
            FoodType.DOUBLE_POINTS: 'green',
            FoodType.INVINCIBILITY: 'white'
        }
        
        # Grid rendering settings
        self.grid_color = 'dark_gray'
        self.background_color = 'black'
        self.hud_background_color = 'navy'
        self.hud_text_color = 'white'
    
    def render_game(self, snake: Snake, food_list: List[Food], 
                   score: int, level: int, food_eaten: int, 
                   game_time: float, high_score: int) -> None:
        """
        Render the complete game state.
        
        Args:
            snake: The snake to render
            food_list: List of food items to render
            score: Current score
            level: Current level
            food_eaten: Number of food items eaten
            game_time: Current game time
            high_score: High score
        """
        # Clear the screen
        self.display.clear_screen(self.background_color)
        
        # Render the game grid
        self._render_grid()
        
        # Render the snake
        self._render_snake(snake)
        
        # Render food items
        self._render_food(food_list)
        
        # Render HUD
        self._render_hud(score, level, food_eaten, game_time, high_score)
    
    def _render_grid(self) -> None:
        """Render the game grid background."""
        grid_width, grid_height = self.display.get_grid_size()
        
        # Draw grid lines
        for x in range(0, grid_width + 1, self.cell_size):
            start_pos = (x, 0)
            end_pos = (x, grid_height)
            self.display.draw_line(start_pos, end_pos, self.grid_color, 1)
        
        for y in range(0, grid_height + 1, self.cell_size):
            start_pos = (0, y)
            end_pos = (grid_width, y)
            self.display.draw_line(start_pos, end_pos, self.grid_color, 1)
    
    def _render_snake(self, snake: Snake) -> None:
        """Render the snake and its segments."""
        body = snake.get_body()
        
        for i, segment in enumerate(body):
            # Determine segment type and color
            if i == 0:
                # Head
                color = self.snake_colors['head']
                self._render_snake_head(segment)
            elif i == len(body) - 1:
                # Tail
                color = self.snake_colors['tail']
                self._render_snake_segment(segment, color)
            else:
                # Body
                color = self.snake_colors['body']
                self._render_snake_segment(segment, color)
    
    def _render_snake_head(self, position: Position) -> None:
        """Render the snake's head with special styling."""
        rect = self.display.get_grid_rect(position.x, position.y)
        
        # Draw head background
        self.display.draw_rect(rect, self.snake_colors['head'])
        
        # Draw head outline
        self.display.draw_rect(rect, self.snake_colors['outline'], False, 2)
        
        # Draw eyes
        eye_size = max(2, self.cell_size // 8)
        eye_offset = self.cell_size // 4
        
        # Left eye
        left_eye_pos = (rect.centerx - eye_offset, rect.centery - eye_offset)
        self.display.draw_circle(left_eye_pos, eye_size, 'black')
        
        # Right eye
        right_eye_pos = (rect.centerx + eye_offset, rect.centery - eye_offset)
        self.display.draw_circle(right_eye_pos, eye_size, 'black')
    
    def _render_snake_segment(self, position: Position, color: str) -> None:
        """Render a snake body segment."""
        rect = self.display.get_grid_rect(position.x, position.y)
        
        # Draw segment with rounded corners effect
        self.display.draw_rect(rect, color)
        
        # Add subtle outline
        self.display.draw_rect(rect, self.snake_colors['outline'], False, 1)
    
    def _render_food(self, food_list: List[Food]) -> None:
        """Render all food items."""
        for food in food_list:
            if not food.is_collected():
                self._render_food_item(food)
    
    def _render_food_item(self, food: Food) -> None:
        """Render a single food item."""
        position = food.get_position()
        food_type = food.get_effect_type()
        
        # Get color for food type
        color = self.food_colors.get(food_type, 'red')
        
        # Calculate center position
        rect = self.display.get_grid_rect(position.x, position.y)
        center = rect.center
        
        # Draw food based on type
        if food_type == FoodType.NORMAL:
            # Simple circle for normal food
            radius = max(3, self.cell_size // 6)
            self.display.draw_circle(center, radius, color)
        elif food_type == FoodType.BONUS:
            # Star shape for bonus food
            self._render_star(center, color)
        elif food_type == FoodType.SPEED_UP:
            # Lightning bolt for speed up
            self._render_lightning(center, color)
        elif food_type == FoodType.SPEED_DOWN:
            # Snail for speed down
            self._render_snail(center, color)
        elif food_type == FoodType.DOUBLE_POINTS:
            # 2x symbol
            self._render_double_points(center, color)
        elif food_type == FoodType.INVINCIBILITY:
            # Shield for invincibility
            self._render_shield(center, color)
        else:
            # Fallback to circle
            radius = max(3, self.cell_size // 6)
            self.display.draw_circle(center, radius, color)
    
    def _render_star(self, center: Tuple[int, int], color: str) -> None:
        """Render a star shape."""
        size = self.cell_size // 4
        points = []
        
        # Create star points
        for i in range(10):
            angle = i * 36 * 3.14159 / 180
            if i % 2 == 0:
                radius = size
            else:
                radius = size // 2
            
            x = center[0] + radius * pygame.math.Vector2(1, 0).rotate(angle)[0]
            y = center[1] + radius * pygame.math.Vector2(1, 0).rotate(angle)[1]
            points.append((x, y))
        
        # Draw star
        if len(points) >= 3:
            self.display.draw_polygon(points, color)
    
    def _render_lightning(self, center: Tuple[int, int], color: str) -> None:
        """Render a lightning bolt symbol."""
        size = self.cell_size // 4
        points = [
            (center[0], center[1] - size),
            (center[0] - size//2, center[1] - size//4),
            (center[0] + size//2, center[1] + size//4),
            (center[0], center[1] + size)
        ]
        
        self.display.draw_polygon(points, color)
    
    def _render_snail(self, center: Tuple[int, int], color: str) -> None:
        """Render a snail symbol."""
        size = self.cell_size // 4
        
        # Draw snail shell (spiral)
        self.display.draw_circle(center, size, color)
        self.display.draw_circle(center, size//2, self.background_color)
    
    def _render_double_points(self, center: Tuple[int, int], color: str) -> None:
        """Render 2x symbol."""
        text = "2×"
        self.display.draw_text(text, center, self.display.large_font, color, True)
    
    def _render_shield(self, center: Tuple[int, int], color: str) -> None:
        """Render a shield symbol."""
        size = self.cell_size // 4
        points = [
            (center[0], center[1] - size),
            (center[0] - size, center[1] - size//2),
            (center[0] - size, center[1] + size//2),
            (center[0], center[1] + size),
            (center[0] + size, center[1] + size//2),
            (center[0] + size, center[1] - size//2)
        ]
        
        self.display.draw_polygon(points, color)
    
    def _render_hud(self, score: int, level: int, food_eaten: int, 
                   game_time: float, high_score: int) -> None:
        """Render the heads-up display."""
        grid_width, grid_height = self.display.get_grid_size()
        hud_y = grid_height
        
        # HUD background
        hud_rect = pygame.Rect(0, hud_y, grid_width, 80)
        self.display.draw_rect(hud_rect, self.hud_background_color)
        
        # Score information
        score_text = f"Score: {score}"
        self.display.draw_text(score_text, (10, hud_y + 10), 
                             self.display.font, self.hud_text_color)
        
        high_score_text = f"High Score: {high_score}"
        self.display.draw_text(high_score_text, (10, hud_y + 35), 
                             self.display.small_font, self.hud_text_color)
        
        # Level and food information
        level_text = f"Level: {level}"
        self.display.draw_text(level_text, (200, hud_y + 10), 
                             self.display.font, self.hud_text_color)
        
        food_text = f"Food: {food_eaten}"
        self.display.draw_text(food_text, (200, hud_y + 35), 
                             self.display.small_font, self.hud_text_color)
        
        # Game time
        time_text = f"Time: {game_time:.1f}s"
        self.display.draw_text(time_text, (350, hud_y + 10), 
                             self.display.font, self.hud_text_color)
        
        # FPS display
        fps = self.display.get_fps()
        fps_text = f"FPS: {fps:.1f}"
        self.display.draw_text(fps_text, (350, hud_y + 35), 
                             self.display.small_font, self.hud_text_color)
    
    def render_game_over_screen(self, final_score: int, high_score: int, 
                               food_eaten: int, game_time: float) -> None:
        """Render the game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface(self.display.get_window_size())
        overlay.set_alpha(128)
        overlay.fill(self.display.get_color('black'))
        self.display.screen.blit(overlay, (0, 0))
        
        # Game over text
        center_x, center_y = self.display.get_window_size()
        center_x //= 2
        center_y //= 2
        
        self.display.draw_text("GAME OVER", (center_x, center_y - 60), 
                             self.display.large_font, 'red', True)
        
        # Final score
        score_text = f"Final Score: {final_score}"
        self.display.draw_text(score_text, (center_x, center_y - 20), 
                             self.display.font, 'white', True)
        
        # High score indicator
        if final_score >= high_score:
            new_record_text = "NEW HIGH SCORE!"
            self.display.draw_text(new_record_text, (center_x, center_y + 10), 
                                 self.display.font, 'gold', True)
        else:
            high_score_text = f"High Score: {high_score}"
            self.display.draw_text(high_score_text, (center_x, center_y + 10), 
                                 self.display.font, 'white', True)
        
        # Game statistics
        stats_text = f"Food Eaten: {food_eaten} | Time: {game_time:.1f}s"
        self.display.draw_text(stats_text, (center_x, center_y + 40), 
                             self.display.small_font, 'light_gray', True)
        
        # Instructions
        instruction_text = "Press R to restart or Q to quit"
        self.display.draw_text(instruction_text, (center_x, center_y + 70), 
                             self.display.small_font, 'light_gray', True)
    
    def render_pause_screen(self) -> None:
        """Render the pause screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface(self.display.get_window_size())
        overlay.set_alpha(128)
        overlay.fill(self.display.get_color('black'))
        self.display.screen.blit(overlay, (0, 0))
        
        # Pause text
        center_x, center_y = self.display.get_window_size()
        center_x //= 2
        center_y //= 2
        
        self.display.draw_text("PAUSED", (center_x, center_y - 20), 
                             self.display.large_font, 'yellow', True)
        
        # Instructions
        instruction_text = "Press P to resume or Q to quit"
        self.display.draw_text(instruction_text, (center_x, center_y + 20), 
                             self.display.small_font, 'light_gray', True)
    
    def render_menu_screen(self, title: str, options: List[str], 
                          selected_index: int = 0) -> None:
        """Render a menu screen."""
        center_x, center_y = self.display.get_window_size()
        center_x //= 2
        center_y //= 2
        
        # Title
        self.display.draw_text(title, (center_x, center_y - 80), 
                             self.display.large_font, 'white', True)
        
        # Menu options
        for i, option in enumerate(options):
            color = 'yellow' if i == selected_index else 'white'
            y_offset = center_y - 20 + (i * 40)
            self.display.draw_text(option, (center_x, y_offset), 
                                 self.display.font, color, True)
        
        # Instructions
        instruction_text = "Use arrow keys to navigate, Enter to select"
        self.display.draw_text(instruction_text, (center_x, center_y + 80), 
                             self.display.small_font, 'light_gray', True)
