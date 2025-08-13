"""
Speed Indicator Renderer

This module provides specialized rendering for the speed progression system with:
- Speed bars and indicators
- Transition animations
- Difficulty ratings
- Speed statistics display
"""

import pygame
import math
from typing import Dict, Any, Tuple
from ..game.speed_system import SpeedProgressionSystem, SpeedProgressionType, SpeedTransitionType
from .display import DisplayManager


class SpeedIndicator:
    """
    Specialized renderer for speed progression visualization.
    
    Provides visual feedback for current speed, transitions, and progression.
    """
    
    def __init__(self, display_manager: DisplayManager):
        """Initialize the speed indicator renderer."""
        self.display = display_manager
        
        # Speed indicator settings
        self.indicator_width = 200
        self.indicator_height = 30
        self.bar_height = 20
        self.text_height = 25
        
        # Animation properties
        self.animation_timer = 0.0
        self.animation_speed = 3.0  # seconds per cycle
        
        # Color schemes
        self.speed_colors = {
            'easy': 'green',
            'medium': 'yellow',
            'hard': 'orange',
            'extreme': 'red'
        }
        
        # Transition effect colors
        self.transition_colors = {
            'smooth': 'blue',
            'ease_in': 'cyan',
            'ease_out': 'magenta',
            'ease_in_out': 'purple',
            'instant': 'white'
        }
    
    def render_speed_indicator(self, speed_system: SpeedProgressionSystem, 
                             surface: pygame.Surface, position: Tuple[int, int]) -> None:
        """
        Render the main speed indicator at the specified position.
        
        Args:
            speed_system: The speed progression system
            surface: Surface to render on
            position: Position to render the indicator
        """
        x, y = position
        
        # Get speed information
        speed_info = speed_system.get_speed_progression_info()
        current_speed = speed_info['current_speed']
        target_speed = speed_info['target_speed']
        max_speed = speed_info['max_speed']
        min_speed = speed_info['min_speed']
        is_transitioning = speed_info['is_transitioning']
        transition_progress = speed_info['transition_progress']
        progression_type = speed_info['progression_type']
        transition_type = speed_info['transition_type']
        
        # Calculate speed ratio for bar display
        speed_ratio = (current_speed - min_speed) / (max_speed - min_speed)
        speed_ratio = max(0.0, min(1.0, speed_ratio))
        
        # Draw container background
        container_rect = pygame.Rect(x, y, self.indicator_width, self.indicator_height)
        pygame.draw.rect(surface, self.display.get_color('dark_gray'), container_rect)
        pygame.draw.rect(surface, self.display.get_color('white'), container_rect, 2)
        
        # Draw speed bar background
        bar_rect = pygame.Rect(x + 5, y + 5, self.indicator_width - 10, self.bar_height)
        pygame.draw.rect(surface, self.display.get_color('black'), bar_rect)
        pygame.draw.rect(surface, self.display.get_color('light_gray'), bar_rect, 1)
        
        # Calculate bar fill width
        fill_width = int((self.indicator_width - 10) * speed_ratio)
        
        # Determine bar color based on difficulty
        difficulty_rating = speed_system.get_speed_difficulty_rating()
        bar_color = self.speed_colors.get(difficulty_rating.lower(), 'white')
        
        # Draw speed bar fill
        if fill_width > 0:
            fill_rect = pygame.Rect(x + 5, y + 5, fill_width, self.bar_height)
            pygame.draw.rect(surface, self.display.get_color(bar_color), fill_rect)
            
            # Add transition effect if transitioning
            if is_transitioning:
                self._add_transition_effect(surface, fill_rect, transition_progress, transition_type)
        
        # Draw speed text
        speed_text = f"Speed: {current_speed:.1f}"
        font = pygame.font.Font(None, 18)
        text_surface = font.render(speed_text, True, self.display.get_color('white'))
        text_rect = text_surface.get_rect(center=bar_rect.center)
        surface.blit(text_surface, text_rect)
        
        # Draw progression type indicator
        self._render_progression_indicator(surface, (x, y + self.indicator_height), progression_type)
    
    def render_detailed_speed_info(self, speed_system: SpeedProgressionSystem, 
                                 surface: pygame.Surface, position: Tuple[int, int]) -> None:
        """
        Render detailed speed information display.
        
        Args:
            speed_system: The speed progression system
            surface: Surface to render on
            position: Position to render the information
        """
        x, y = position
        
        # Get comprehensive speed information
        speed_stats = speed_system.get_speed_statistics()
        speed_info = speed_system.get_speed_progression_info()
        
        # Calculate container size
        info_width = 300
        info_height = 200
        
        # Draw container
        container_rect = pygame.Rect(x, y, info_width, info_height)
        pygame.draw.rect(surface, self.display.get_color('navy'), container_rect)
        pygame.draw.rect(surface, self.display.get_color('white'), container_rect, 2)
        
        # Draw title
        title_font = pygame.font.Font(None, 24)
        title_surface = title_font.render("Speed Information", True, self.display.get_color('white'))
        title_rect = title_surface.get_rect(centerx=container_rect.centerx, top=y + 10)
        surface.blit(title_surface, title_rect)
        
        # Draw speed details
        detail_y = y + 50
        line_height = 25
        
        details = [
            f"Current Speed: {speed_info['current_speed']:.1f}",
            f"Target Speed: {speed_info['target_speed']:.1f}",
            f"Min Speed: {speed_info['min_speed']:.1f}",
            f"Max Speed: {speed_info['max_speed']:.1f}",
            f"Progression: {speed_info['progression_type']}",
            f"Transition: {speed_info['transition_type']}",
            f"Difficulty: {speed_system.get_speed_difficulty_rating()}",
            f"Speed Multiplier: {speed_stats['speed_multiplier']:.2f}x"
        ]
        
        for i, detail in enumerate(details):
            detail_y_pos = detail_y + (i * line_height)
            detail_surface = pygame.font.Font(None, 16).render(detail, True, self.display.get_color('white'))
            surface.blit(detail_surface, (x + 10, detail_y_pos))
        
        # Draw transition progress bar if transitioning
        if speed_info['is_transitioning']:
            self._render_transition_progress_bar(surface, (x + 10, detail_y + 200), 
                                              speed_info['transition_progress'])
    
    def render_speed_progression_chart(self, speed_system: SpeedProgressionSystem, 
                                     surface: pygame.Surface, position: Tuple[int, int]) -> None:
        """
        Render a speed progression chart.
        
        Args:
            speed_system: The speed progression system
            surface: Surface to render on
            position: Position to render the chart
        """
        x, y = position
        
        # Get speed history
        speed_stats = speed_system.get_speed_statistics()
        speed_history = speed_stats.get('speed_history_count', 0)
        
        if speed_history < 2:
            return  # Need at least 2 points for a chart
        
        # Chart dimensions
        chart_width = 250
        chart_height = 150
        
        # Draw chart container
        chart_rect = pygame.Rect(x, y, chart_width, chart_height)
        pygame.draw.rect(surface, self.display.get_color('dark_gray'), chart_rect)
        pygame.draw.rect(surface, self.display.get_color('white'), chart_rect, 2)
        
        # Draw chart title
        title_font = pygame.font.Font(None, 18)
        title_surface = title_font.render("Speed Progression", True, self.display.get_color('white'))
        title_rect = title_surface.get_rect(centerx=chart_rect.centerx, top=y + 5)
        surface.blit(title_surface, title_rect)
        
        # Draw chart area
        chart_area_rect = pygame.Rect(x + 10, y + 25, chart_width - 20, chart_height - 35)
        pygame.draw.rect(surface, self.display.get_color('black'), chart_area_rect)
        
        # Draw speed line (simplified - in a real implementation, you'd plot actual data)
        self._draw_speed_line(surface, chart_area_rect, speed_system)
    
    def _render_progression_indicator(self, surface: pygame.Surface, position: Tuple[int, int], 
                                    progression_type: str) -> None:
        """Render a small indicator for the progression type."""
        x, y = position
        
        # Small indicator box
        indicator_size = 20
        indicator_rect = pygame.Rect(x, y, indicator_size, indicator_size)
        
        # Color based on progression type
        progression_colors = {
            'linear': 'blue',
            'exponential': 'red',
            'logarithmic': 'green',
            'stepped': 'yellow',
            'custom': 'purple'
        }
        
        color = progression_colors.get(progression_type, 'white')
        pygame.draw.rect(surface, self.display.get_color(color), indicator_rect)
        pygame.draw.rect(surface, self.display.get_color('white'), indicator_rect, 1)
        
        # Draw progression type abbreviation
        abbrev = progression_type[:3].upper()
        font = pygame.font.Font(None, 14)
        text_surface = font.render(abbrev, True, self.display.get_color('black'))
        text_rect = text_surface.get_rect(center=indicator_rect.center)
        surface.blit(text_surface, text_rect)
    
    def _add_transition_effect(self, surface: pygame.Surface, rect: pygame.Rect, 
                              progress: float, transition_type: str) -> None:
        """Add a visual effect for speed transitions."""
        if not rect or progress <= 0:
            return
        
        # Get transition color
        transition_color = self.transition_colors.get(transition_type, 'white')
        
        # Create transition effect based on type
        if transition_type == 'smooth':
            # Simple pulse effect
            pulse_alpha = int(128 * (1 - progress))
            if pulse_alpha > 0:
                pulse_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
                pygame.draw.rect(pulse_surface, (*self.display.get_color(transition_color), pulse_alpha), 
                               pulse_surface.get_rect())
                surface.blit(pulse_surface, rect)
        
        elif transition_type in ['ease_in', 'ease_out', 'ease_in_out']:
            # Gradient effect
            gradient_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            for i in range(rect.width):
                alpha = int(64 * (1 - progress))
                if alpha > 0:
                    pygame.draw.line(gradient_surface, (*self.display.get_color(transition_color), alpha),
                                   (i, 0), (i, rect.height))
            surface.blit(gradient_surface, rect)
    
    def _render_transition_progress_bar(self, surface: pygame.Surface, position: Tuple[int, int], 
                                      progress: float) -> None:
        """Render a progress bar for speed transitions."""
        x, y = position
        bar_width = 200
        bar_height = 15
        
        # Background bar
        bg_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(surface, self.display.get_color('dark_gray'), bg_rect)
        pygame.draw.rect(surface, self.display.get_color('white'), bg_rect, 1)
        
        # Progress bar
        if progress > 0:
            progress_width = int(bar_width * progress)
            progress_rect = pygame.Rect(x, y, progress_width, bar_height)
            pygame.draw.rect(surface, self.display.get_color('cyan'), progress_rect)
        
        # Progress text
        progress_text = f"Transition: {progress * 100:.0f}%"
        font = pygame.font.Font(None, 14)
        text_surface = font.render(progress_text, True, self.display.get_color('white'))
        text_rect = text_surface.get_rect(center=bg_rect.center)
        surface.blit(text_surface, text_rect)
    
    def _draw_speed_line(self, surface: pygame.Surface, chart_rect: pygame.Rect, 
                        speed_system: SpeedProgressionSystem) -> None:
        """Draw a simplified speed progression line."""
        # This is a simplified visualization - in a real implementation,
        # you would plot actual speed history data
        
        # Get current speed info
        speed_info = speed_system.get_speed_progression_info()
        current_speed = speed_info['current_speed']
        max_speed = speed_info['max_speed']
        min_speed = speed_info['min_speed']
        
        # Calculate relative position
        speed_ratio = (current_speed - min_speed) / (max_speed - min_speed)
        speed_ratio = max(0.0, min(1.0, speed_ratio))
        
        # Draw a simple line representing current speed
        line_y = chart_rect.bottom - int(chart_rect.height * speed_ratio)
        line_start = (chart_rect.left, line_y)
        line_end = (chart_rect.right, line_y)
        
        pygame.draw.line(surface, self.display.get_color('cyan'), line_start, line_end, 2)
        
        # Draw speed label
        speed_text = f"{current_speed:.1f}"
        font = pygame.font.Font(None, 14)
        text_surface = font.render(speed_text, True, self.display.get_color('white'))
        text_rect = text_surface.get_rect(midright=(chart_rect.right - 5, line_y))
        surface.blit(text_surface, text_rect)
    
    def render_speed_controls(self, speed_system: SpeedProgressionSystem, 
                            surface: pygame.Surface, position: Tuple[int, int]) -> None:
        """
        Render speed control interface.
        
        Args:
            speed_system: The speed progression system
            surface: Surface to render on
            position: Position to render the controls
        """
        x, y = position
        
        # Control panel dimensions
        panel_width = 250
        panel_height = 120
        
        # Draw control panel
        panel_rect = pygame.Rect(x, y, panel_width, panel_height)
        pygame.draw.rect(surface, self.display.get_color('dark_gray'), panel_rect)
        pygame.draw.rect(surface, self.display.get_color('white'), panel_rect, 2)
        
        # Draw title
        title_font = pygame.font.Font(None, 20)
        title_surface = title_font.render("Speed Controls", True, self.display.get_color('white'))
        title_rect = title_surface.get_rect(centerx=panel_rect.centerx, top=y + 10)
        surface.blit(title_surface, title_rect)
        
        # Draw control options
        controls_y = y + 40
        line_height = 20
        
        # Speed multiplier control
        multiplier_text = f"Multiplier: {speed_system.get_speed_multiplier():.2f}x"
        font = pygame.font.Font(None, 16)
        text_surface = font.render(multiplier_text, True, self.display.get_color('white'))
        surface.blit(text_surface, (x + 10, controls_y))
        
        # Speed progression type
        speed_info = speed_system.get_speed_progression_info()
        progression_text = f"Type: {speed_info['progression_type']}"
        text_surface = font.render(progression_text, True, self.display.get_color('white'))
        surface.blit(text_surface, (x + 10, controls_y + line_height))
        
        # Speed transition type
        transition_text = f"Transition: {speed_info['transition_type']}"
        text_surface = font.render(transition_text, True, self.display.get_color('white'))
        surface.blit(text_surface, (x + 10, controls_y + line_height * 2))
        
        # Speed enabled status
        speed_stats = speed_system.get_speed_statistics()
        enabled_text = f"Enabled: {'Yes' if speed_stats['speed_enabled'] else 'No'}"
        text_surface = font.render(enabled_text, True, self.display.get_color('white'))
        surface.blit(text_surface, (x + 10, controls_y + line_height * 3))
    
    def update_animation(self, delta_time: float) -> None:
        """Update animation timer for visual effects."""
        self.animation_timer += delta_time
        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0.0
    
    def get_speed_color(self, speed_ratio: float) -> str:
        """Get color based on speed ratio."""
        if speed_ratio < 0.3:
            return 'green'
        elif speed_ratio < 0.6:
            return 'yellow'
        elif speed_ratio < 0.8:
            return 'orange'
        else:
            return 'red'
