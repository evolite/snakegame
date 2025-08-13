"""
Unit tests for UI Components.

Tests the user interface components including:
- DisplayManager
- GameRenderer
- SnakeRenderer
- FoodRenderer
"""

import pytest
import pygame
from unittest.mock import Mock, patch, MagicMock
from src.ui.display import DisplayManager
from src.ui.game_renderer import GameRenderer
from src.ui.snake_renderer import SnakeRenderer
from src.ui.food_renderer import FoodRenderer
from src.game.game_state import GameConfig
from src.game.grid import Position, Direction
from src.game.snake import Snake


class TestDisplayManager:
    """Test the DisplayManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = GameConfig(
            grid_width=20,
            grid_height=15,
            cell_size=25
        )
        # Mock pygame to avoid actual display initialization
        with patch('pygame.display.set_mode'), \
             patch('pygame.display.set_caption'), \
             patch('pygame.font.Font'), \
             patch('pygame.init'), \
             patch('pygame.time.Clock'):
            self.display_manager = DisplayManager(self.config)
    
    def teardown_method(self):
        """Clean up after tests."""
        if hasattr(self, 'display_manager'):
            self.display_manager.cleanup()
    
    def test_display_manager_initialization(self):
        """Test DisplayManager initialization."""
        assert self.display_manager.config == self.config
        assert self.display_manager.screen is not None
        assert self.display_manager.font is not None
        assert self.display_manager.clock is not None
        
        # Check that colors are initialized
        assert 'black' in self.display_manager.colors
        assert 'white' in self.display_manager.colors
        assert 'red' in self.display_manager.colors
        assert 'green' in self.display_manager.colors
    
    def test_display_manager_get_screen(self):
        """Test getting the screen surface."""
        screen = self.display_manager.get_screen()
        assert screen == self.display_manager.screen
    
    def test_display_manager_get_clock(self):
        """Test getting the clock."""
        clock = self.display_manager.get_clock()
        assert clock == self.display_manager.clock
    
    def test_display_manager_get_colors(self):
        """Test getting the color palette."""
        colors = self.display_manager.get_colors()
        assert isinstance(colors, dict)
        assert len(colors) > 0
    
    def test_display_manager_get_color(self):
        """Test getting specific colors."""
        # Test valid colors
        assert self.display_manager.get_color('red') == (255, 0, 0)
        assert self.display_manager.get_color('green') == (0, 255, 0)
        assert self.display_manager.get_color('blue') == (0, 0, 255)
        
        # Test invalid color (should return white as fallback)
        assert self.display_manager.get_color('invalid_color') == (255, 255, 255)
    
    def test_display_manager_get_window_size(self):
        """Test getting window dimensions."""
        # Mock screen.get_size
        self.display_manager.screen.get_size = Mock(return_value=(500, 400))
        
        size = self.display_manager.get_window_size()
        assert size == (500, 400)
    
    def test_display_manager_get_grid_size(self):
        """Test getting grid dimensions."""
        grid_size = self.display_manager.get_grid_size()
        expected_width = 20 * 25  # grid_width * cell_size
        expected_height = 15 * 25  # grid_height * cell_size
        assert grid_size == (expected_width, expected_height)
    
    def test_display_manager_get_cell_size(self):
        """Test getting cell size."""
        cell_size = self.display_manager.get_cell_size()
        assert cell_size == 25
    
    def test_display_manager_clear_screen(self):
        """Test clearing the screen."""
        # Mock the screen.fill method
        self.display_manager.screen.fill = Mock()
        
        self.display_manager.clear_screen('black')
        
        # Should call screen.fill with black color
        self.display_manager.screen.fill.assert_called_once()
        call_args = self.display_manager.screen.fill.call_args[0]
        assert call_args[0] == (0, 0, 0)  # Black color
    
    def test_display_manager_update_display(self):
        """Test updating the display."""
        # Mock the pygame.display.flip method
        with patch('pygame.display.flip') as mock_flip:
            self.display_manager.update_display()
            mock_flip.assert_called_once()
    
    def test_display_manager_set_fps(self):
        """Test setting FPS."""
        # Mock clock.tick
        self.display_manager.clock.tick = Mock()
        
        self.display_manager.set_fps(60)
        self.display_manager.clock.tick.assert_called_once_with(60)
    
    def test_display_manager_get_fps(self):
        """Test getting FPS."""
        # Mock clock.get_fps
        self.display_manager.clock.get_fps = Mock(return_value=58.5)
        
        fps = self.display_manager.get_fps()
        assert fps == 58.5
    
    def test_display_manager_draw_text(self):
        """Test drawing text."""
        # Mock font.render and screen.blit
        mock_text_surface = Mock()
        mock_text_surface.get_rect = Mock(return_value=Mock())
        
        self.display_manager.font.render = Mock(return_value=mock_text_surface)
        self.display_manager.screen.blit = Mock()
        
        self.display_manager.draw_text("Test Text", (100, 100))
        
        # Should render text and blit to screen
        assert self.display_manager.font.render.called
        assert self.display_manager.screen.blit.called
    
    def test_display_manager_draw_rect(self):
        """Test drawing rectangles."""
        # Mock pygame.draw.rect
        with patch('pygame.draw.rect') as mock_rect:
            rect = pygame.Rect(100, 100, 50, 50)
            
            # Test filled rectangle
            self.display_manager.draw_rect(rect, 'red', fill=True)
            mock_rect.assert_called()
            
            # Test outlined rectangle
            self.display_manager.draw_rect(rect, 'blue', fill=False, border_width=2)
            mock_rect.assert_called()
    
    def test_display_manager_draw_circle(self):
        """Test drawing circles."""
        # Mock pygame.draw.circle
        with patch('pygame.draw.circle') as mock_circle:
            position = (150, 150)
            
            # Test filled circle
            self.display_manager.draw_circle(position, 25, 'green', fill=True)
            mock_circle.assert_called()
            
            # Test outlined circle
            self.display_manager.draw_circle(position, 30, 'yellow', fill=False, border_width=3)
            mock_circle.assert_called()
    
    def test_display_manager_get_grid_position(self):
        """Test grid to screen coordinate conversion."""
        screen_pos = self.display_manager.get_grid_position(5, 3)
        expected_x = 5 * 25  # grid_x * cell_size
        expected_y = 3 * 25  # grid_y * cell_size
        assert screen_pos == (expected_x, expected_y)
    
    def test_display_manager_get_grid_rect(self):
        """Test getting grid rectangle."""
        rect = self.display_manager.get_grid_rect(5, 3)
        assert rect.x == 125  # 5 * 25
        assert rect.y == 75   # 3 * 25
        assert rect.width == 25
        assert rect.height == 25
    
    def test_display_manager_is_initialized(self):
        """Test initialization check."""
        # Should be initialized after setup
        assert self.display_manager.is_initialized() is True
    
    def test_display_manager_cleanup(self):
        """Test cleanup method."""
        # Mock pygame.quit
        with patch('pygame.quit') as mock_quit:
            self.display_manager.cleanup()
            mock_quit.assert_called_once()


class TestGameRenderer:
    """Test the GameRenderer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = GameConfig()
        self.display_manager = Mock()
        self.display_manager.get_cell_size.return_value = 20
        self.display_manager.get_grid_size.return_value = (400, 300)
        self.display_manager.get_window_size.return_value = (400, 380)
        self.display_manager.screen = Mock()
        self.display_manager.font = Mock()
        self.display_manager.small_font = Mock()
        self.display_manager.large_font = Mock()
        
        self.game_renderer = GameRenderer(self.display_manager)
    
    def test_game_renderer_initialization(self):
        """Test GameRenderer initialization."""
        assert self.game_renderer.display == self.display_manager
        assert self.game_renderer.cell_size == 20
        
        # Check color configurations
        assert 'head' in self.game_renderer.snake_colors
        assert 'body' in self.game_renderer.snake_colors
        assert 'tail' in self.game_renderer.snake_colors
    
    def test_game_renderer_render_game(self):
        """Test rendering the main game."""
        # Mock snake and food
        mock_snake = Mock()
        mock_food_list = [Mock(), Mock()]
        
        # Mock drawing methods
        self.game_renderer._render_grid = Mock()
        self.game_renderer._render_snake = Mock()
        self.game_renderer._render_food = Mock()
        self.game_renderer._render_hud = Mock()
        
        # Render game
        self.game_renderer.render_game(
            snake=mock_snake,
            food_list=mock_food_list,
            score=150,
            level=3,
            food_eaten=8,
            game_time=45.5,
            high_score=300
        )
        
        # Check that all drawing methods were called
        self.game_renderer._render_grid.assert_called_once()
        self.game_renderer._render_snake.assert_called_once_with(mock_snake)
        self.game_renderer._render_food.assert_called_once_with(mock_food_list)
        self.game_renderer._render_hud.assert_called_once_with(150, 3, 8, 45.5, 300)
    
    def test_game_renderer_render_grid(self):
        """Test rendering the game grid."""
        # Mock display.draw_line
        self.display_manager.draw_line = Mock()
        
        self.game_renderer._render_grid()
        
        # Should draw grid lines
        assert self.display_manager.draw_line.called
    
    def test_game_renderer_render_snake(self):
        """Test rendering the snake."""
        mock_snake = Mock()
        mock_snake.get_body.return_value = [Position(5, 5), Position(4, 5), Position(3, 5)]
        
        # Mock rendering methods
        self.game_renderer._render_snake_head = Mock()
        self.game_renderer._render_snake_segment = Mock()
        
        self.game_renderer._render_snake(mock_snake)
        
        # Should render head and segments
        assert self.game_renderer._render_snake_head.called
        assert self.game_renderer._render_snake_segment.called
    
    def test_game_renderer_render_food(self):
        """Test rendering food items."""
        mock_food1 = Mock()
        mock_food1.is_collected.return_value = False
        mock_food2 = Mock()
        mock_food2.is_collected.return_value = True  # Collected food
        
        food_list = [mock_food1, mock_food2]
        
        # Mock rendering method
        self.game_renderer._render_food_item = Mock()
        
        self.game_renderer._render_food(food_list)
        
        # Should only render uncollected food
        self.game_renderer._render_food_item.assert_called_once_with(mock_food1)
    
    def test_game_renderer_render_hud(self):
        """Test rendering the HUD."""
        # Mock display methods
        self.display_manager.draw_rect = Mock()
        self.display_manager.draw_text = Mock()
        self.display_manager.get_fps.return_value = 58.5
        
        self.game_renderer._render_hud(150, 3, 8, 45.5, 300)
        
        # Should draw HUD elements
        assert self.display_manager.draw_rect.called
        assert self.display_manager.draw_text.called
    
    def test_game_renderer_render_game_over_screen(self):
        """Test rendering the game over screen."""
        # Mock pygame.Surface
        with patch('pygame.Surface') as mock_surface:
            mock_surface_instance = Mock()
            mock_surface.return_value = mock_surface_instance
            
            self.game_renderer.render_game_over_screen(150, 300, 8, 45.5)
            
            # Should create overlay and draw text
            mock_surface.assert_called()
    
    def test_game_renderer_render_pause_screen(self):
        """Test rendering the pause screen."""
        # Mock pygame.Surface
        with patch('pygame.Surface') as mock_surface:
            mock_surface_instance = Mock()
            mock_surface.return_value = mock_surface_instance
            
            self.game_renderer.render_pause_screen()
            
            # Should create overlay and draw text
            mock_surface.assert_called()
    
    def test_game_renderer_render_menu_screen(self):
        """Test rendering the menu screen."""
        title = "Main Menu"
        options = ["Start Game", "Settings", "Quit"]
        selected_index = 1
        
        # Mock display.draw_text
        self.display_manager.draw_text = Mock()
        
        self.game_renderer.render_menu_screen(title, options, selected_index)
        
        # Should draw title, options, and instructions
        assert self.display_manager.draw_text.called


class TestSnakeRenderer:
    """Test the SnakeRenderer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.display_manager = Mock()
        self.display_manager.get_cell_size.return_value = 20
        self.display_manager.get_grid_rect.return_value = pygame.Rect(100, 100, 20, 20)
        
        self.snake_renderer = SnakeRenderer(self.display_manager)
    
    def test_snake_renderer_initialization(self):
        """Test SnakeRenderer initialization."""
        assert self.snake_renderer.display == self.display_manager
        assert self.snake_renderer.cell_size == 20
    
    def test_snake_renderer_render_snake(self):
        """Test rendering the snake."""
        # Create a mock snake with body
        mock_snake = Mock()
        mock_snake.get_body.return_value = [Position(5, 5), Position(4, 5), Position(3, 5)]
        
        # Mock pygame.draw.rect
        with patch('pygame.draw.rect') as mock_rect:
            self.snake_renderer.render_snake(mock_snake)
            
            # Should draw snake segments
            assert mock_rect.called


class TestFoodRenderer:
    """Test the FoodRenderer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.display_manager = Mock()
        self.display_manager.get_cell_size.return_value = 20
        self.display_manager.get_grid_rect.return_value = pygame.Rect(100, 100, 20, 20)
        
        self.food_renderer = FoodRenderer(self.display_manager)
    
    def test_food_renderer_initialization(self):
        """Test FoodRenderer initialization."""
        assert self.food_renderer.display == self.display_manager
        assert self.food_renderer.cell_size == 20
    
    def test_food_renderer_render_food(self):
        """Test rendering food items."""
        # Create mock food objects
        mock_food1 = Mock()
        mock_food1.is_collected.return_value = False
        mock_food1.get_position.return_value = Position(5, 5)
        mock_food1.get_effect_type.return_value = "normal"
        
        mock_food2 = Mock()
        mock_food2.is_collected.return_value = True  # Collected food
        
        food_list = [mock_food1, mock_food2]
        
        # Mock pygame.draw.circle
        with patch('pygame.draw.circle') as mock_circle:
            self.food_renderer.render_food(food_list)
            
            # Should only render uncollected food
            assert mock_circle.called


if __name__ == "__main__":
    pytest.main([__file__])
