"""
Snake Renderer

This module provides specialized rendering for the snake with:
- Advanced visual effects
- Smooth animations
- Segment styling
- Growth animations
"""

import pygame
from typing import List, Tuple, Dict
from ..game.grid import Position
from ..game.snake import Snake
from .display import DisplayManager


class SnakeRenderer:
    """
    Specialized renderer for snake visualization.
    
    Provides advanced visual effects and animations for the snake.
    """
    
    def __init__(self, display_manager: DisplayManager):
        """Initialize the snake renderer."""
        self.display = display_manager
        self.cell_size = display_manager.get_cell_size()
        
        # Snake color schemes
        self.color_schemes = {
            'default': {
                'head': 'green',
                'body': 'lime',
                'tail': 'olive',
                'outline': 'dark_gray',
                'highlight': 'yellow'
            },
            'neon': {
                'head': 'cyan',
                'body': 'blue',
                'tail': 'navy',
                'outline': 'white',
                'highlight': 'yellow'
            },
            'fire': {
                'head': 'red',
                'body': 'orange',
                'tail': 'yellow',
                'outline': 'dark_gray',
                'highlight': 'white'
            },
            'ice': {
                'head': 'cyan',
                'body': 'aqua',
                'tail': 'light_gray',
                'outline': 'white',
                'highlight': 'blue'
            }
        }
        
        # Current color scheme
        self.current_scheme = 'default'
        
        # Animation properties
        self.animation_timer = 0.0
        self.animation_speed = 2.0  # seconds per cycle
        
        # Special effects
        self.glow_effect = True
        self.shadow_effect = True
        self.segment_rounding = True
    
    def set_color_scheme(self, scheme_name: str) -> None:
        """Set the snake color scheme."""
        if scheme_name in self.color_schemes:
            self.current_scheme = scheme_name
    
    def get_current_colors(self) -> Dict[str, str]:
        """Get the current color scheme."""
        return self.color_schemes[self.current_scheme]
    
    def render_snake(self, snake: Snake, delta_time: float = 0.0) -> None:
        """
        Render the complete snake with all visual effects.
        
        Args:
            snake: The snake to render
            delta_time: Time elapsed since last frame
        """
        # Update animation timer
        self.animation_timer += delta_time
        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0.0
        
        body = snake.get_body()
        
        # Render each segment
        for i, segment in enumerate(body):
            if i == 0:
                self._render_snake_head(segment, snake)
            elif i == len(body) - 1:
                self._render_snake_tail(segment, i)
            else:
                self._render_snake_body(segment, i, len(body))
    
    def _render_snake_head(self, position: Position, snake: Snake) -> None:
        """Render the snake's head with special effects."""
        colors = self.get_current_colors()
        rect = self.display.get_grid_rect(position.x, position.y)
        
        # Draw shadow if enabled
        if self.shadow_effect:
            shadow_rect = rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            self.display.draw_rect(shadow_rect, 'black', True)
        
        # Draw head background
        self.display.draw_rect(rect, colors['head'], True)
        
        # Draw head outline
        self.display.draw_rect(rect, colors['outline'], False, 2)
        
        # Draw eyes with animation
        self._render_snake_eyes(rect, colors)
        
        # Draw tongue (animated)
        self._render_snake_tongue(rect, snake)
        
        # Add glow effect if enabled
        if self.glow_effect:
            self._add_glow_effect(rect, colors['head'])
    
    def _render_snake_eyes(self, rect: pygame.Rect, colors: Dict[str, str]) -> None:
        """Render the snake's eyes with animation."""
        eye_size = max(2, self.cell_size // 8)
        eye_offset = self.cell_size // 4
        
        # Animate eye size based on timer
        animation_factor = (pygame.math.sin(self.animation_timer * 10) + 1) / 2
        eye_size = int(eye_size * (0.8 + 0.2 * animation_factor))
        
        # Left eye
        left_eye_pos = (rect.centerx - eye_offset, rect.centery - eye_offset)
        self.display.draw_circle(left_eye_pos, eye_size, 'black')
        self.display.draw_circle(left_eye_pos, eye_size // 2, 'white')
        
        # Right eye
        right_eye_pos = (rect.centerx + eye_offset, rect.centery - eye_offset)
        self.display.draw_circle(right_eye_pos, eye_size, 'black')
        self.display.draw_circle(right_eye_pos, eye_size // 2, 'white')
    
    def _render_snake_tongue(self, rect: pygame.Rect, snake: Snake) -> None:
        """Render the snake's tongue with animation."""
        # Get snake direction to position tongue
        direction = snake.get_direction_vector()
        
        # Calculate tongue position
        tongue_start = rect.center
        tongue_end = (
            tongue_start[0] + direction.x * (self.cell_size // 2),
            tongue_start[1] + direction.y * (self.cell_size // 2)
        )
        
        # Animate tongue length
        animation_factor = (pygame.math.sin(self.animation_timer * 15) + 1) / 2
        tongue_length = int(self.cell_size // 4 * (0.5 + 0.5 * animation_factor))
        
        # Calculate final tongue end
        direction_vector = pygame.math.Vector2(direction.x, direction.y)
        direction_vector.scale_to_length(tongue_length)
        tongue_end = (
            tongue_start[0] + direction_vector.x,
            tongue_start[1] + direction_vector.y
        )
        
        # Draw tongue
        self.display.draw_line(tongue_start, tongue_end, 'red', 2)
        
        # Draw tongue tip
        tip_size = 2
        self.display.draw_circle(tongue_end, tip_size, 'red')
    
    def _render_snake_body(self, position: Position, segment_index: int, total_segments: int) -> None:
        """Render a snake body segment."""
        colors = self.get_current_colors()
        rect = self.display.get_grid_rect(position.x, position.y)
        
        # Calculate segment color variation
        color_variation = self._calculate_segment_color_variation(segment_index, total_segments)
        segment_color = self._blend_colors(colors['body'], colors['highlight'], color_variation)
        
        # Draw shadow if enabled
        if self.shadow_effect:
            shadow_rect = rect.copy()
            shadow_rect.x += 1
            shadow_rect.y += 1
            self.display.draw_rect(shadow_rect, 'black', True)
        
        # Draw segment with rounded corners if enabled
        if self.segment_rounding:
            self._render_rounded_segment(rect, segment_color, colors['outline'])
        else:
            self.display.draw_rect(rect, segment_color, True)
            self.display.draw_rect(rect, colors['outline'], False, 1)
        
        # Add segment pattern
        self._render_segment_pattern(rect, segment_index)
    
    def _render_snake_tail(self, position: Position, segment_index: int) -> None:
        """Render the snake's tail segment."""
        colors = self.get_current_colors()
        rect = self.display.get_grid_rect(position.x, position.y)
        
        # Draw shadow if enabled
        if self.shadow_effect:
            shadow_rect = rect.copy()
            shadow_rect.x += 1
            shadow_rect.y += 1
            self.display.draw_rect(shadow_rect, 'black', True)
        
        # Draw tail with special styling
        self.display.draw_rect(rect, colors['tail'], True)
        self.display.draw_rect(rect, colors['outline'], False, 1)
        
        # Add tail pattern
        self._render_tail_pattern(rect)
    
    def _render_rounded_segment(self, rect: pygame.Rect, color: str, outline_color: str) -> None:
        """Render a segment with rounded corners."""
        # For simplicity, we'll use a filled rectangle with rounded corners
        # In a more advanced implementation, you could use pygame.draw.ellipse for corners
        
        # Main segment
        self.display.draw_rect(rect, color, True)
        
        # Outline
        self.display.draw_rect(rect, outline_color, False, 1)
        
        # Add subtle inner highlight
        inner_rect = rect.inflate(-2, -2)
        highlight_color = self._lighten_color(color, 0.3)
        self.display.draw_rect(inner_rect, highlight_color, False, 1)
    
    def _render_segment_pattern(self, rect: pygame.Rect, segment_index: int) -> None:
        """Render a pattern on the body segment."""
        # Create a subtle pattern based on segment index
        pattern_type = segment_index % 4
        
        if pattern_type == 0:
            # Dots pattern
            center = rect.center
            dot_size = 1
            self.display.draw_circle(center, dot_size, 'dark_gray')
        elif pattern_type == 1:
            # Lines pattern
            center = rect.center
            line_length = self.cell_size // 6
            start_pos = (center[0] - line_length, center[1])
            end_pos = (center[0] + line_length, center[1])
            self.display.draw_line(start_pos, end_pos, 'dark_gray', 1)
        elif pattern_type == 2:
            # Cross pattern
            center = rect.center
            line_length = self.cell_size // 6
            # Horizontal line
            h_start = (center[0] - line_length, center[1])
            h_end = (center[0] + line_length, center[1])
            self.display.draw_line(h_start, h_end, 'dark_gray', 1)
            # Vertical line
            v_start = (center[0], center[1] - line_length)
            v_end = (center[0], center[1] + line_length)
            self.display.draw_line(v_start, v_end, 'dark_gray', 1)
    
    def _render_tail_pattern(self, rect: pygame.Rect) -> None:
        """Render a special pattern on the tail segment."""
        center = rect.center
        
        # Draw a small triangle pointing outward
        triangle_size = self.cell_size // 8
        points = [
            (center[0], center[1] - triangle_size),
            (center[0] - triangle_size, center[1] + triangle_size),
            (center[0] + triangle_size, center[1] + triangle_size)
        ]
        
        self.display.draw_polygon(points, 'dark_gray')
    
    def _calculate_segment_color_variation(self, segment_index: int, total_segments: int) -> float:
        """Calculate color variation for a segment."""
        # Create a wave pattern based on segment position
        wave = pygame.math.sin(segment_index * 0.5 + self.animation_timer * 2)
        return (wave + 1) / 2  # Normalize to 0-1 range
    
    def _blend_colors(self, color1: str, color2: str, factor: float) -> str:
        """Blend two colors based on a factor."""
        # For simplicity, return the first color
        # In a full implementation, you'd blend the RGB values
        return color1
    
    def _lighten_color(self, color: str, factor: float) -> str:
        """Lighten a color by a factor."""
        # For simplicity, return a lighter variant
        # In a full implementation, you'd adjust the RGB values
        if color == 'green':
            return 'lime'
        elif color == 'blue':
            return 'cyan'
        elif color == 'red':
            return 'pink'
        else:
            return color
    
    def _add_glow_effect(self, rect: pygame.Rect, color: str) -> None:
        """Add a glow effect around the element."""
        # Create a larger, semi-transparent version for glow
        glow_rect = rect.inflate(4, 4)
        
        # Create glow surface
        glow_surface = pygame.Surface(glow_rect.size)
        glow_surface.set_alpha(64)
        glow_surface.fill(self.display.get_color(color))
        
        # Draw glow
        self.display.screen.blit(glow_surface, glow_rect)
    
    def render_growth_animation(self, position: Position, animation_progress: float) -> None:
        """
        Render a growth animation at a specific position.
        
        Args:
            position: Position where growth occurs
            animation_progress: Animation progress (0.0 to 1.0)
        """
        colors = self.get_current_colors()
        rect = self.display.get_grid_rect(position.x, position.y)
        
        # Scale the segment based on animation progress
        scaled_rect = rect.inflate(
            int(rect.width * animation_progress),
            int(rect.height * animation_progress)
        )
        
        # Center the scaled rect
        scaled_rect.center = rect.center
        
        # Draw growing segment
        self.display.draw_rect(scaled_rect, colors['body'], True)
        self.display.draw_rect(scaled_rect, colors['outline'], False, 2)
        
        # Add sparkle effect
        if animation_progress > 0.5:
            sparkle_alpha = int(255 * (1.0 - animation_progress))
            sparkle_surface = pygame.Surface(rect.size)
            sparkle_surface.set_alpha(sparkle_alpha)
            sparkle_surface.fill(self.display.get_color('yellow'))
            self.display.screen.blit(sparkle_surface, rect)
    
    def render_death_animation(self, snake: Snake, animation_progress: float) -> None:
        """
        Render a death animation for the snake.
        
        Args:
            snake: The snake to animate
            animation_progress: Animation progress (0.0 to 1.0)
        """
        body = snake.get_body()
        
        for i, segment in enumerate(body):
            # Calculate segment fade based on position and progress
            segment_fade = max(0, 1.0 - animation_progress - (i * 0.1))
            
            if segment_fade > 0:
                # Create faded surface
                segment_surface = pygame.Surface((self.cell_size, self.cell_size))
                segment_surface.set_alpha(int(255 * segment_fade))
                
                # Fill with segment color
                colors = self.get_current_colors()
                if i == 0:
                    color = colors['head']
                elif i == len(body) - 1:
                    color = colors['tail']
                else:
                    color = colors['body']
                
                segment_surface.fill(self.display.get_color(color))
                
                # Draw to screen
                rect = self.display.get_grid_rect(segment.x, segment.y)
                self.display.screen.blit(segment_surface, rect)
    
    def get_available_color_schemes(self) -> List[str]:
        """Get list of available color schemes."""
        return list(self.color_schemes.keys())
    
    def create_custom_color_scheme(self, name: str, colors: Dict[str, str]) -> None:
        """Create a custom color scheme."""
        self.color_schemes[name] = colors.copy()
    
    def set_effects(self, glow: bool = None, shadow: bool = None, rounding: bool = None) -> None:
        """Set visual effects."""
        if glow is not None:
            self.glow_effect = glow
        if shadow is not None:
            self.shadow_effect = shadow
        if rounding is not None:
            self.segment_rounding = rounding
