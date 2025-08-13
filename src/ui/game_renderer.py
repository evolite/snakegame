"""
Game Renderer

This module handles the rendering of all game elements:
- Snake visualization
- Food rendering
- Grid and background
- HUD and UI elements
- Visual effects and animations
- Power-ups display
"""

import pygame
from typing import List, Tuple
from ..game.grid import Position
from ..game.snake import Snake
from ..game.food import Food, FoodType
from ..game.power_ups import PowerUpsManager
from .display import DisplayManager
from .visual_effects import VisualEffectsManager
from .power_ups_renderer import PowerUpsRenderer


class GameRenderer:
    """
    Handles the rendering of all game elements.
    
    This class is responsible for drawing:
    - The game grid and background
    - The snake and its segments
    - Food items
    - HUD elements (score, level, etc.)
    - UI overlays
    - Visual effects and animations
    - Power-ups status and indicators
    """
    
    def __init__(self, display_manager: DisplayManager):
        """Initialize the game renderer."""
        self.display = display_manager
        self.cell_size = display_manager.get_cell_size()
        
        # Initialize visual effects manager
        self.visual_effects = VisualEffectsManager()
        
        # Initialize power-ups renderer
        self.power_ups_renderer = PowerUpsRenderer(display_manager)
        
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
        
        # Visual effects settings
        self.enable_particles = True
        self.enable_animations = True
        self.enable_background_effects = True
        
        # Power-ups display settings
        self.show_power_ups_hud = True
        self.power_ups_hud_position = (10, 10)
        
        # Background effect timer
        self.background_effect_timer = 0.0
        self.background_effect_interval = 5.0  # Create new effect every 5 seconds
    
    def render_game(self, snake: Snake, food_list: List[Food], 
                   score: int, level: int, food_eaten: int, 
                   game_time: float, high_score: int, 
                   power_ups_manager: PowerUpsManager = None,
                   obstacle_manager = None,
                   delta_time: float = 0.0, current_difficulty: str = "Medium") -> None:
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
            power_ups_manager: Power-ups manager for status display
            delta_time: Time elapsed since last frame
        """
        # Update visual effects
        self.visual_effects.update(delta_time)
        
        # Update background effects
        self._update_background_effects(delta_time)
        
        # Clear the screen
        self.display.clear_screen(self.background_color)
        
        # Render background effects
        if self.enable_background_effects:
            self._render_background_effects()
        
        # Render the game grid
        self._render_grid()
        
        # Render the snake
        self._render_snake(snake)
        
        # Render food items
        self._render_food(food_list)
        
        # Render obstacles
        if obstacle_manager:
            self._render_obstacles(obstacle_manager)
        
        # Render visual effects (particles, animations)
        if self.enable_particles:
            self.visual_effects.draw(self.display.screen)
        
        # Render HUD
        self._render_hud(score, level, food_eaten, game_time, high_score, current_difficulty)
        
        # Render power-ups HUD
        if self.show_power_ups_hud and power_ups_manager:
            self._render_power_ups_hud(power_ups_manager)
    
    def _render_power_ups_hud(self, power_ups_manager: PowerUpsManager) -> None:
        """Render the power-ups HUD."""
        self.power_ups_renderer.render_power_ups_hud(
            power_ups_manager, 
            self.display.screen, 
            self.power_ups_hud_position
        )
    
    def _update_background_effects(self, delta_time: float) -> None:
        """Update background effects timer."""
        self.background_effect_timer += delta_time
        if self.background_effect_timer >= self.background_effect_interval:
            self.background_effect_timer = 0.0
            if self.enable_background_effects:
                self.visual_effects.create_background_effect()
    
    def _render_background_effects(self) -> None:
        """Render subtle background effects."""
        # This will be handled by the visual effects manager
        pass
    
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
                   game_time: float, high_score: int, current_difficulty: str = "Medium") -> None:
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
                             self.display.font, self.hud_text_color)
        
        # Level and food information
        level_text = f"Level: {level}"
        self.display.draw_text(level_text, (200, hud_y + 10), 
                             self.display.font, self.hud_text_color)
        
        food_text = f"Food: {food_eaten}"
        self.display.draw_text(food_text, (200, hud_y + 35), 
                             self.display.font, self.hud_text_color)
        
        # Game time
        time_text = f"Time: {game_time:.1f}s"
        self.display.draw_text(time_text, (350, hud_y + 10), 
                             self.display.font, self.hud_text_color)
        
        # FPS display
        fps = self.display.get_fps()
        fps_text = f"FPS: {fps:.1f}"
        self.display.draw_text(fps_text, (350, hud_y + 35), 
                             self.display.font, self.hud_text_color)
        
        # Difficulty display
        difficulty_text = f"Difficulty: {self.current_difficulty}"
        self.display.draw_text(difficulty_text, (500, hud_y + 35), 
                             self.display.font, self.hud_text_color)
        
        # Visual effects info
        if self.enable_particles:
            effect_count = self.visual_effects.get_active_effect_count()
            effects_text = f"Effects: {effect_count}"
            self.display.draw_text(effects_text, (500, hud_y + 10), 
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
                             self.display.font, 'light_gray', True)
        
        # Instructions
        instruction_text = "Press R to restart or Q to quit"
        self.display.draw_text(instruction_text, (center_x, center_y + 70), 
                             self.display.font, 'light_gray', True)
    
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
                             self.display.font, 'light_gray', True)
    
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
                             self.display.font, 'light_gray', True)
    
    def render_high_scores_screen(self, high_scores: List) -> None:
        """Render the high scores screen."""
        center_x, center_y = self.display.get_window_size()
        center_x //= 2
        center_y //= 2
        
        # Title
        self.display.draw_text("🏆 HIGH SCORES", (center_x, center_y - 200), 
                             self.display.large_font, 'gold', True)
        
        # Draw high scores
        if not high_scores:
            self.display.draw_text("No high scores yet!", (center_x, center_y), 
                                 self.display.font, 'light_gray', True)
            self.display.draw_text("Play a game to set your first record!", (center_x, center_y + 50), 
                                 self.display.font, 'light_gray', True)
        else:
            # Draw score entries
            start_y = center_y - 100
            for i, score_entry in enumerate(high_scores[:10]):  # Top 10 scores
                # Rank
                rank_color = 'gold' if i == 0 else 'silver' if i == 1 else 'bronze' if i == 2 else 'white'
                rank_text = f"{i + 1}."
                self.display.draw_text(rank_text, (center_x - 200, start_y + i * 40), 
                                     self.display.font, rank_color, False)
                
                # Player name
                self.display.draw_text(score_entry.player_name, (center_x - 100, start_y + i * 40), 
                                     self.display.font, 'white', False)
                
                # Score
                self.display.draw_text(str(score_entry.score), (center_x + 50, start_y + i * 40), 
                                     self.display.font, 'white', False)
                
                # Difficulty
                self.display.draw_text(score_entry.difficulty.title(), (center_x + 150, start_y + i * 40), 
                                     self.display.font, 'light_gray', False)
        
        # Draw instructions
        self.display.draw_text("Press Enter or Esc to return to menu", 
                             (center_x, center_y + 200), 
                             self.display.font, 'light_gray', True)
    
    # Visual effects integration methods
    
    def create_food_collection_effect(self, position: Tuple[float, float]) -> None:
        """Create a particle explosion effect when food is collected."""
        if self.enable_particles:
            self.visual_effects.create_food_collection_effect(position)
    
    def create_power_up_effect(self, position: Tuple[float, float]) -> None:
        """Create a power-up activation effect."""
        if self.enable_particles:
            self.visual_effects.create_power_up_effect(position)
    
    def create_score_popup(self, position: Tuple[float, float], score: int) -> None:
        """Create a score popup animation."""
        if self.enable_animations:
            self.visual_effects.create_score_popup(position, score)
    
    def create_screen_transition(self) -> None:
        """Create a screen transition effect."""
        if self.enable_animations:
            self.visual_effects.create_screen_transition()
    
    def set_visual_effects_enabled(self, particles: bool = None, animations: bool = None, 
                                  background_effects: bool = None) -> None:
        """Enable or disable visual effects."""
        if particles is not None:
            self.enable_particles = particles
        if animations is not None:
            self.enable_animations = animations
        if background_effects is not None:
            self.enable_background_effects = background_effects
    
    def set_power_ups_display_enabled(self, enabled: bool) -> None:
        """Enable or disable power-ups HUD display."""
        self.show_power_ups_hud = enabled
    
    def set_power_ups_hud_position(self, position: Tuple[int, int]) -> None:
        """Set the position of the power-ups HUD."""
        self.power_ups_hud_position = position
    
    def clear_all_visual_effects(self) -> None:
        """Clear all active visual effects."""
        self.visual_effects.clear_all_effects()
    
    def get_visual_effects_manager(self) -> VisualEffectsManager:
        """Get the visual effects manager for advanced configuration."""
        return self.visual_effects
    
    def get_power_ups_renderer(self) -> PowerUpsRenderer:
        """Get the power-ups renderer for advanced configuration."""
        return self.power_ups_renderer
    
    def _render_obstacles(self, obstacle_manager) -> None:
        """Render all obstacles."""
        for obstacle in obstacle_manager.active_obstacles:
            if obstacle.is_active():
                self._render_obstacle(obstacle)
    
    def _render_obstacle(self, obstacle) -> None:
        """Render a single obstacle."""
        position = obstacle.get_position()
        obstacle_type = obstacle.get_type()
        
        # Get obstacle color based on type
        color = self._get_obstacle_color(obstacle_type)
        
        # Get obstacle rect
        rect = self.display.get_grid_rect(position.x, position.y)
        
        # Render obstacle with visual effects
        if obstacle_type.value == "static_wall":
            # Solid wall
            self.display.draw_rect(rect, color)
            self.display.draw_rect(rect, 'dark_gray', False, 2)
        elif obstacle_type.value == "breakable_wall":
            # Breakable wall with cracks
            self.display.draw_rect(rect, color)
            self.display.draw_rect(rect, 'brown', False, 2)
        elif obstacle_type.value == "spike_trap":
            # Spike trap with spikes
            self.display.draw_rect(rect, color)
            self._render_spikes(rect)
        elif obstacle_type.value == "speed_pad":
            # Speed pad with arrows
            self.display.draw_rect(rect, color)
            self._render_speed_pad_arrows(rect)
        elif obstacle_type.value == "score_multiplier":
            # Score multiplier with star
            self.display.draw_rect(rect, color)
            self._render_multiplier_star(rect)
        else:
            # Default obstacle rendering
            self.display.draw_rect(rect, color)
            self.display.draw_rect(rect, 'dark_gray', False, 1)
    
    def _get_obstacle_color(self, obstacle_type) -> str:
        """Get the color for an obstacle type."""
        obstacle_colors = {
            "static_wall": "gray",
            "breakable_wall": "brown",
            "moving_obstacle": "purple",
            "spike_trap": "red",
            "teleporter": "blue",
            "speed_pad": "green",
            "score_multiplier": "gold",
            "safe_zone": "cyan"
        }
        return obstacle_colors.get(obstacle_type.value, "gray")
    
    def _render_spikes(self, rect) -> None:
        """Render spikes on a spike trap."""
        spike_color = "dark_red"
        spike_size = max(2, self.cell_size // 6)
        
        # Draw multiple spikes
        for i in range(3):
            x_offset = (i - 1) * (self.cell_size // 4)
            spike_pos = (rect.centerx + x_offset, rect.centery - self.cell_size // 4)
            self.display.draw_circle(spike_pos, spike_size, spike_color)
    
    def _render_speed_pad_arrows(self, rect) -> None:
        """Render arrows on a speed pad."""
        arrow_color = "dark_green"
        
        # Draw forward arrow
        arrow_points = [
            (rect.centerx - self.cell_size // 4, rect.centery),
            (rect.centerx + self.cell_size // 4, rect.centery),
            (rect.centerx + self.cell_size // 6, rect.centery - self.cell_size // 6),
            (rect.centerx + self.cell_size // 6, rect.centery + self.cell_size // 6)
        ]
        self.display.draw_polygon(arrow_points, arrow_color)
    
    def _render_multiplier_star(self, rect) -> None:
        """Render a star on a score multiplier obstacle."""
        star_color = "dark_gold"
        star_size = self.cell_size // 3
        
        # Draw a simple star shape
        center = (rect.centerx, rect.centery)
        self.display.draw_circle(center, star_size, star_color)
