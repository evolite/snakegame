"""
Pytest configuration and common fixtures for the Snake Game tests.

This file provides shared test fixtures and configuration that can be used
across all test modules.
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock

# Add the src directory to the Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Mock pygame for testing (since we don't want to initialize the display)
@pytest.fixture(autouse=True)
def mock_pygame():
    """Mock pygame to avoid display initialization during testing."""
    import sys
    from unittest.mock import MagicMock
    
    # Create a mock pygame module
    mock_pygame = MagicMock()
    mock_pygame.init = MagicMock()
    mock_pygame.quit = MagicMock()
    mock_pygame.display = MagicMock()
    mock_pygame.event = MagicMock()
    mock_pygame.time = MagicMock()
    mock_pygame.math = MagicMock()
    mock_pygame.Surface = MagicMock()
    mock_pygame.Rect = MagicMock()
    mock_pygame.Color = MagicMock()
    
    # Mock pygame constants
    mock_pygame.QUIT = 12
    mock_pygame.KEYDOWN = 768
    mock_pygame.KEYUP = 769
    mock_pygame.K_UP = 273
    mock_pygame.K_DOWN = 274
    mock_pygame.K_LEFT = 276
    mock_pygame.K_RIGHT = 275
    mock_pygame.K_w = 119
    mock_pygame.K_a = 97
    mock_pygame.K_s = 115
    mock_pygame.K_d = 100
    mock_pygame.K_ESCAPE = 27
    mock_pygame.K_RETURN = 13
    mock_pygame.K_SPACE = 32
    mock_pygame.K_p = 112
    mock_pygame.K_q = 113
    mock_pygame.K_r = 114
    
    # Replace pygame in sys.modules
    sys.modules['pygame'] = mock_pygame
    
    yield mock_pygame
    
    # Clean up
    if 'pygame' in sys.modules:
        del sys.modules['pygame']


@pytest.fixture
def mock_display():
    """Create a mock display manager for testing."""
    mock_display = Mock()
    mock_display.screen = Mock()
    mock_display.clock = Mock()
    mock_display.font = Mock()
    mock_display.small_font = Mock()
    mock_display.large_font = Mock()
    mock_display.get_window_size.return_value = (800, 600)
    mock_display.get_grid_size.return_value = (800, 520)
    mock_display.get_cell_size.return_value = 20
    mock_display.get_fps.return_value = 60.0
    mock_display.get_color.return_value = (255, 255, 255)
    mock_display.draw_text = Mock()
    mock_display.draw_rect = Mock()
    mock_display.draw_circle = Mock()
    mock_display.draw_polygon = Mock()
    mock_display.get_grid_rect.return_value = Mock()
    mock_display.clear_screen = Mock()
    mock_display.update_display = Mock()
    mock_display.is_initialized.return_value = True
    return mock_display


@pytest.fixture
def mock_grid():
    """Create a mock grid for testing."""
    mock_grid = Mock()
    mock_grid.width = 40
    mock_grid.height = 30
    mock_grid.is_valid_position.return_value = True
    mock_grid.is_position_occupied.return_value = False
    mock_grid.occupy_position = Mock()
    mock_grid.free_position = Mock()
    mock_grid.get_grid_center.return_value = Mock()
    mock_grid.clear_all_occupied = Mock()
    return mock_grid


@pytest.fixture
def mock_snake():
    """Create a mock snake for testing."""
    mock_snake = Mock()
    mock_snake.get_head.return_value = Mock()
    mock_snake.get_body.return_value = [Mock(), Mock(), Mock()]
    mock_snake.get_length.return_value = 3
    mock_snake.get_tail.return_value = Mock()
    mock_snake.change_direction.return_value = True
    mock_snake.move.return_value = True
    mock_snake.grow = Mock()
    mock_snake.reset = Mock()
    mock_snake.growing = False
    return mock_snake


@pytest.fixture
def mock_food_manager():
    """Create a mock food manager for testing."""
    mock_food_manager = Mock()
    mock_food_manager.get_food_list.return_value = []
    mock_food_manager.spawn_food.return_value = Mock()
    mock_food_manager.collect_food_at_position.return_value = None
    return mock_food_manager


@pytest.fixture
def mock_power_ups_manager():
    """Create a mock power-ups manager for testing."""
    mock_power_ups_manager = Mock()
    mock_power_ups_manager.get_score_multiplier.return_value = 1.0
    mock_power_ups_manager.activate_power_up = Mock()
    mock_power_ups_manager.has_magnet_effect.return_value = False
    mock_power_ups_manager.clear_all_power_ups = Mock()
    return mock_power_ups_manager


@pytest.fixture
def mock_scoring_system():
    """Create a mock scoring system for testing."""
    mock_scoring_system = Mock()
    mock_scoring_system.score_multiplier = Mock()
    mock_scoring_system.score_multiplier.get_multiplier.return_value = 1.0
    mock_scoring_system.score_multiplier.update = Mock()
    mock_scoring_system.add_score = Mock()
    mock_scoring_system.reset_score = Mock()
    mock_scoring_system.get_current_score.return_value = 0
    mock_scoring_system.get_high_score.return_value = 0
    return mock_scoring_system


@pytest.fixture
def mock_speed_system():
    """Create a mock speed system for testing."""
    mock_speed_system = Mock()
    mock_speed_system.get_speed_based_score_multiplier.return_value = 1.0
    mock_speed_system.reset_speed = Mock()
    mock_speed_system.set_initial_speed = Mock()
    mock_speed_system.set_max_speed = Mock()
    mock_speed_system.set_base_increase = Mock()
    return mock_speed_system


@pytest.fixture
def mock_difficulty_manager():
    """Create a mock difficulty manager for testing."""
    mock_difficulty_manager = Mock()
    mock_difficulty_manager.get_current_difficulty.return_value = Mock()
    mock_difficulty_manager.get_current_settings.return_value = Mock()
    mock_difficulty_manager.calculate_difficulty_score.return_value = 100
    return mock_difficulty_manager


@pytest.fixture
def game_config():
    """Create a game configuration for testing."""
    from src.game.game_state import GameConfig
    return GameConfig(
        grid_width=20,
        grid_height=15,
        cell_size=20,
        initial_speed=8.0,
        speed_increase=0.5,
        max_speed=25.0
    )


@pytest.fixture
def sample_position():
    """Create a sample position for testing."""
    from src.game.grid import Position
    return Position(5, 5)


@pytest.fixture
def sample_direction():
    """Create a sample direction for testing."""
    from src.game.grid import Direction
    return Direction.RIGHT


# Test markers
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "ui: marks tests as UI tests"
    )
    config.addinivalue_line(
        "markers", "game_logic: marks tests as game logic tests"
    )
