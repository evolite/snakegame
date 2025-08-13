"""
Tests for the UI components.

This module tests the user interface and graphics systems.
"""

import pytest
import pygame
from src.game.game_state import GameConfig
from src.ui.display import DisplayManager
from src.ui.game_renderer import GameRenderer
from src.ui.snake_renderer import SnakeRenderer
from src.ui.food_renderer import FoodRenderer


class TestDisplayManager:
    """Test the display management system."""
    
    def test_display_initialization(self):
        """Test display manager initialization."""
        config = GameConfig()
        display = DisplayManager(config)
        
        assert display.is_initialized()
        assert display.screen is not None
        assert display.clock is not None
        assert display.font is not None
    
    def test_color_management(self):
        """Test color management functionality."""
        config = GameConfig()
        display = DisplayManager(config)
        
        # Test color retrieval
        assert display.get_color('red') == (255, 0, 0)
        assert display.get_color('green') == (0, 255, 0)
        assert display.get_color('blue') == (0, 0, 255)
        
        # Test invalid color fallback
        assert display.get_color('invalid_color') == (255, 255, 255)  # white fallback
    
    def test_grid_coordinate_conversion(self):
        """Test grid to screen coordinate conversion."""
        config = GameConfig(grid_width=10, grid_height=10, cell_size=20)
        display = DisplayManager(config)
        
        # Test grid position conversion
        screen_pos = display.get_grid_position(5, 3)
        assert screen_pos == (100, 60)  # 5 * 20, 3 * 20
        
        # Test grid rect creation
        rect = display.get_grid_rect(5, 3)
        assert rect.x == 100
        assert rect.y == 60
        assert rect.width == 20
        assert rect.height == 20
    
    def test_text_rendering(self):
        """Test text rendering functionality."""
        config = GameConfig()
        display = DisplayManager(config)
        
        # Test text drawing (should not raise exceptions)
        try:
            display.draw_text("Test Text", (100, 100))
            display.draw_text("Centered Text", (200, 200), center=True)
            display.draw_text("Colored Text", (300, 300), color='red')
        except Exception as e:
            pytest.fail(f"Text rendering failed: {e}")
    
    def test_shape_rendering(self):
        """Test shape rendering functionality."""
        config = GameConfig()
        display = DisplayManager(config)
        
        # Test rectangle drawing
        rect = pygame.Rect(100, 100, 50, 50)
        try:
            display.draw_rect(rect, 'red')
            display.draw_rect(rect, 'blue', fill=False, border_width=2)
        except Exception as e:
            pytest.fail(f"Rectangle rendering failed: {e}")
        
        # Test circle drawing
        try:
            display.draw_circle((150, 150), 25, 'green')
            display.draw_circle((200, 200), 30, 'yellow', fill=False, border_width=3)
        except Exception as e:
            pytest.fail(f"Circle rendering failed: {e}")
    
    def test_cleanup(self):
        """Test display cleanup."""
        config = GameConfig()
        display = DisplayManager(config)
        
        # Test cleanup (should not raise exceptions)
        try:
            display.cleanup()
        except Exception as e:
            pytest.fail(f"Display cleanup failed: {e}")


class TestGameRenderer:
    """Test the game rendering system."""
    
    def test_game_renderer_initialization(self):
        """Test game renderer initialization."""
        config = GameConfig()
        display = DisplayManager(config)
        renderer = GameRenderer(display)
        
        assert renderer.display == display
        assert renderer.cell_size == config.cell_size
    
    def test_snake_colors(self):
        """Test snake color configuration."""
        config = GameConfig()
        display = DisplayManager(config)
        renderer = GameRenderer(display)
        
        # Test snake color scheme
        assert 'head' in renderer.snake_colors
        assert 'body' in renderer.snake_colors
        assert 'tail' in renderer.snake_colors
        assert 'outline' in renderer.snake_colors
    
    def test_food_colors(self):
        """Test food color configuration."""
        config = GameConfig()
        display = DisplayManager(config)
        renderer = GameRenderer(display)
        
        # Test food color mapping
        from src.game.food import FoodType
        assert FoodType.NORMAL in renderer.food_colors
        assert FoodType.BONUS in renderer.food_colors
        assert FoodType.SPEED_UP in renderer.food_colors


class TestSnakeRenderer:
    """Test the snake rendering system."""
    
    def test_snake_renderer_initialization(self):
        """Test snake renderer initialization."""
        config = GameConfig()
        display = DisplayManager(config)
        renderer = SnakeRenderer(display)
        
        assert renderer.display == display
        assert renderer.cell_size == config.cell_size
        assert 'default' in renderer.color_schemes
    
    def test_color_schemes(self):
        """Test snake color schemes."""
        config = GameConfig()
        display = DisplayManager(config)
        renderer = SnakeRenderer(display)
        
        # Test available schemes
        schemes = renderer.get_available_color_schemes()
        assert 'default' in schemes
        assert 'neon' in schemes
        assert 'fire' in schemes
        assert 'ice' in schemes
    
    def test_color_scheme_switching(self):
        """Test color scheme switching."""
        config = GameConfig()
        display = DisplayManager(config)
        renderer = SnakeRenderer(display)
        
        # Test scheme switching
        renderer.set_color_scheme('neon')
        assert renderer.current_scheme == 'neon'
        
        renderer.set_color_scheme('fire')
        assert renderer.current_scheme == 'fire'
        
        # Test invalid scheme (should not change)
        renderer.set_color_scheme('invalid_scheme')
        assert renderer.current_scheme == 'fire'  # Should remain unchanged


class TestFoodRenderer:
    """Test the food rendering system."""
    
    def test_food_renderer_initialization(self):
        """Test food renderer initialization."""
        config = GameConfig()
        display = DisplayManager(config)
        renderer = FoodRenderer(display)
        
        assert renderer.display == display
        assert renderer.cell_size == config.cell_size
        assert len(renderer.food_effects) > 0
    
    def test_food_effects_configuration(self):
        """Test food effects configuration."""
        config = GameConfig()
        display = DisplayManager(config)
        renderer = FoodRenderer(display)
        
        from src.game.food import FoodType
        
        # Test that all food types have effects configured
        for food_type in FoodType:
            assert food_type in renderer.food_effects
            effects = renderer.food_effects[food_type]
            assert 'color' in effects
            assert 'animation' in effects
            assert 'particles' in effects
            assert 'glow' in effects
    
    def test_animation_speed_setting(self):
        """Test animation speed configuration."""
        config = GameConfig()
        display = DisplayManager(config)
        renderer = FoodRenderer(display)
        
        # Test animation speed setting
        renderer.set_animation_speed(2.0)
        assert renderer.animation_speed == 2.0
        
        renderer.set_animation_speed(0.5)
        assert renderer.animation_speed == 0.5
    
    def test_effects_enabling(self):
        """Test effects enabling/disabling."""
        config = GameConfig()
        display = DisplayManager(config)
        renderer = FoodRenderer(display)
        
        # Test particle effects
        renderer.enable_particles(False)
        for food_type in renderer.food_effects:
            assert renderer.food_effects[food_type]['particles'] == False
        
        renderer.enable_particles(True)
        for food_type in renderer.food_effects:
            assert renderer.food_effects[food_type]['particles'] == True
        
        # Test glow effects
        renderer.enable_glow(False)
        for food_type in renderer.food_effects:
            assert renderer.food_effects[food_type]['glow'] == False


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
