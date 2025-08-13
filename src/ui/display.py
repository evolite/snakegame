"""
Display System

This module handles the main display setup, window management, and rendering coordination.
It uses Pygame as the graphics library for optimal game performance.
"""

import pygame
from typing import Tuple, Optional
from ..game.game_state import GameConfig


class DisplayManager:
    """
    Manages the game display and window.
    
    Handles:
    - Window creation and management
    - Display settings and configuration
    - Rendering coordination
    - Screen updates and refresh
    """
    
    def __init__(self, config: GameConfig):
        """Initialize the display manager."""
        self.config = config
        self.screen = None
        self.clock = None
        self.font = None
        self.small_font = None
        self.large_font = None
        
        # Color definitions
        self.colors = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'gray': (128, 128, 128),
            'dark_gray': (64, 64, 64),
            'light_gray': (192, 192, 192),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'cyan': (0, 255, 255),
            'magenta': (255, 0, 255),
            'orange': (255, 165, 0),
            'purple': (128, 0, 128),
            'brown': (139, 69, 19),
            'pink': (255, 192, 203),
            'gold': (255, 215, 0),
            'silver': (192, 192, 192),
            'navy': (0, 0, 128),
            'maroon': (128, 0, 0),
            'olive': (128, 128, 0),
            'teal': (0, 128, 128),
            'lime': (0, 255, 0),
            'aqua': (0, 255, 255),
            'fuchsia': (255, 0, 255)
        }
        
        # Initialize Pygame
        self._initialize_pygame()
    
    def _initialize_pygame(self) -> None:
        """Initialize Pygame and create the game window."""
        pygame.init()
        
        # Calculate window dimensions
        window_width = self.config.grid_width * self.config.cell_size
        window_height = self.config.grid_height * self.config.cell_size
        
        # Add space for HUD
        hud_height = 80
        window_height += hud_height
        
        # Create the game window
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("🐍 Python Snake Game")
        
        # Set window icon (if available)
        try:
            icon = pygame.Surface((32, 32))
            icon.fill(self.colors['green'])
            pygame.display.set_icon(icon)
        except:
            pass  # Icon setting is optional
        
        # Initialize clock for frame rate control
        self.clock = pygame.time.Clock()
        
        # Initialize fonts
        self._initialize_fonts()
    
    def _initialize_fonts(self) -> None:
        """Initialize font objects for text rendering."""
        try:
            # Try to use system fonts
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 18)
            self.large_font = pygame.font.Font(None, 36)
        except:
            # Fallback to default font
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 18)
            self.large_font = pygame.font.Font(None, 36)
    
    def get_screen(self) -> pygame.Surface:
        """Get the main screen surface."""
        return self.screen
    
    def get_clock(self) -> pygame.time.Clock:
        """Get the Pygame clock for frame rate control."""
        return self.clock
    
    def get_colors(self) -> dict:
        """Get the color palette."""
        return self.colors
    
    def get_color(self, color_name: str) -> Tuple[int, int, int]:
        """Get a specific color by name."""
        return self.colors.get(color_name, self.colors['white'])
    
    def get_window_size(self) -> Tuple[int, int]:
        """Get the window dimensions."""
        return self.screen.get_size()
    
    def get_grid_size(self) -> Tuple[int, int]:
        """Get the grid dimensions in pixels."""
        return (
            self.config.grid_width * self.config.cell_size,
            self.config.grid_height * self.config.cell_size
        )
    
    def get_cell_size(self) -> int:
        """Get the size of each grid cell in pixels."""
        return self.config.cell_size
    
    def clear_screen(self, color: str = 'black') -> None:
        """Clear the screen with a specified color."""
        self.screen.fill(self.get_color(color))
    
    def update_display(self) -> None:
        """Update the display and handle events."""
        pygame.display.flip()
    
    def set_fps(self, fps: int) -> None:
        """Set the target frame rate."""
        self.clock.tick(fps)
    
    def get_fps(self) -> float:
        """Get the current frame rate."""
        return self.clock.get_fps()
    
    def draw_text(self, text: str, position: Tuple[int, int], 
                  font: Optional[pygame.font.Font] = None, 
                  color: str = 'white', 
                  center: bool = False) -> None:
        """
        Draw text on the screen.
        
        Args:
            text: Text to render
            position: (x, y) position
            font: Font to use (defaults to main font)
            color: Color name
            center: Whether to center the text at the position
        """
        if font is None:
            font = self.font
        
        text_surface = font.render(text, True, self.get_color(color))
        
        if center:
            text_rect = text_surface.get_rect(center=position)
        else:
            text_rect = text_surface.get_rect(topleft=position)
        
        self.screen.blit(text_surface, text_rect)
    
    def draw_rect(self, rect: pygame.Rect, color: str = 'white', 
                  fill: bool = True, border_width: int = 1) -> None:
        """
        Draw a rectangle on the screen.
        
        Args:
            rect: Rectangle to draw
            color: Color name
            fill: Whether to fill the rectangle
            border_width: Width of the border (0 for filled)
        """
        if fill:
            pygame.draw.rect(self.screen, self.get_color(color), rect)
        else:
            pygame.draw.rect(self.screen, self.get_color(color), rect, border_width)
    
    def draw_circle(self, position: Tuple[int, int], radius: int, 
                   color: str = 'white', fill: bool = True, 
                   border_width: int = 1) -> None:
        """
        Draw a circle on the screen.
        
        Args:
            position: (x, y) center position
            radius: Radius of the circle
            color: Color name
            fill: Whether to fill the circle
            border_width: Width of the border (0 for filled)
        """
        if fill:
            pygame.draw.circle(self.screen, self.get_color(color), position, radius)
        else:
            pygame.draw.circle(self.screen, self.get_color(color), position, radius, border_width)
    
    def draw_line(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], 
                  color: str = 'white', width: int = 1) -> None:
        """
        Draw a line on the screen.
        
        Args:
            start_pos: Starting position (x, y)
            end_pos: Ending position (x, y)
            color: Color name
            width: Width of the line
        """
        pygame.draw.line(self.screen, self.get_color(color), start_pos, end_pos, width)
    
    def draw_polygon(self, points: list, color: str = 'white', 
                     fill: bool = True, border_width: int = 1) -> None:
        """
        Draw a polygon on the screen.
        
        Args:
            points: List of (x, y) points
            color: Color name
            fill: Whether to fill the polygon
            border_width: Width of the border (0 for filled)
        """
        if fill:
            pygame.draw.polygon(self.screen, self.get_color(color), points)
        else:
            pygame.draw.polygon(self.screen, self.get_color(color), points, border_width)
    
    def get_grid_position(self, grid_x: int, grid_y: int) -> Tuple[int, int]:
        """
        Convert grid coordinates to screen coordinates.
        
        Args:
            grid_x: Grid X coordinate
            grid_y: Grid Y coordinate
            
        Returns:
            (screen_x, screen_y) screen coordinates
        """
        screen_x = grid_x * self.config.cell_size
        screen_y = grid_y * self.config.cell_size
        return (screen_x, screen_y)
    
    def get_grid_rect(self, grid_x: int, grid_y: int) -> pygame.Rect:
        """
        Get the screen rectangle for a grid position.
        
        Args:
            grid_x: Grid X coordinate
            grid_y: Grid Y coordinate
            
        Returns:
            pygame.Rect for the grid cell
        """
        screen_x, screen_y = self.get_grid_position(grid_x, grid_y)
        return pygame.Rect(screen_x, screen_y, self.config.cell_size, self.config.cell_size)
    
    def cleanup(self) -> None:
        """Clean up Pygame resources."""
        pygame.quit()
    
    def is_initialized(self) -> bool:
        """Check if the display is properly initialized."""
        return self.screen is not None and self.clock is not None
