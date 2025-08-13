"""
Snake Renderer

This module provides specialized rendering for the snake with:
- Advanced visual effects
- Smooth animations
- Segment styling
- Growth animations
- Movement wave effects
"""

import pygame
import math
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
        
        # Movement animation properties
        self.movement_timer = 0.0
        self.movement_speed = 8.0  # waves per second
        self.wave_amplitude = 2.0  # pixels
        
        # Growth animation properties
        self.growth_animations = {}  # segment_id -> animation_data
        self.growth_duration = 0.5  # seconds
        
        # Special effects
        self.glow_effect = True
        self.shadow_effect = True
        self.segment_rounding = True
        self.wave_effect = True
        self.growth_effect = True
    
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
        # Update animation timers
        self.animation_timer += delta_time
        self.movement_timer += delta_time
        
        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0.0
        
        body = snake.get_body()
        
        # Update growth animations
        self._update_growth_animations(delta_time)
        
        # Render each segment
        for i, segment in enumerate(body):
            if i == 0:
                self._render_snake_head(segment, snake)
            elif i == len(body) - 1:
                self._render_snake_tail(segment, i)
            else:
                self._render_snake_body(segment, i, len(body))
    
    def _update_growth_animations(self, delta_time: float) -> None:
        """Update growth animations for all segments."""
        completed_animations = []
        
        for segment_id, animation_data in self.growth_animations.items():
            animation_data['elapsed'] += delta_time
            if animation_data['elapsed'] >= animation_data['duration']:
                completed_animations.append(segment_id)
        
        # Remove completed animations
        for segment_id in completed_animations:
            del self.growth_animations[segment_id]
    
    def add_growth_animation(self, segment_id: str, position: Position) -> None:
        """Add a growth animation for a new segment."""
        self.growth_animations[segment_id] = {
            'position': position,
            'elapsed': 0.0,
            'duration': self.growth_duration,
            'initial_scale': 0.0,
            'target_scale': 1.0
        }
    
    def _render_snake_head(self, position: Position, snake: Snake) -> None:
        """Render the snake's head with special effects."""
        colors = self.get_current_colors()
        rect = self.display.get_grid_rect(position.x, position.y)
        
        # Apply movement wave effect
        if self.wave_effect:
            rect.y += self._calculate_wave_offset(0, self.movement_timer)
        
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
        animation_factor = (math.sin(self.animation_timer * 10) + 1) / 2
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
        animation_factor = (math.sin(self.animation_timer * 15) + 1) / 2
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
        
        # Apply movement wave effect
        if self.wave_effect:
            rect.y += self._calculate_wave_offset(segment_index, self.movement_timer)
        
        # Check for growth animation
        growth_scale = self._get_growth_scale(position)
        if growth_scale != 1.0:
            rect = self._scale_rect(rect, growth_scale)
        
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
        
        # Add segment-specific effects
        self._add_segment_effects(rect, segment_index, total_segments)
    
    def _render_snake_tail(self, position: Position, segment_index: int) -> None:
        """Render the snake's tail with special effects."""
        colors = self.get_current_colors()
        rect = self.display.get_grid_rect(position.x, position.y)
        
        # Apply movement wave effect
        if self.wave_effect:
            rect.y += self._calculate_wave_offset(segment_index, self.movement_timer)
        
        # Check for growth animation
        growth_scale = self._get_growth_scale(position)
        if growth_scale != 1.0:
            rect = self._scale_rect(rect, growth_scale)
        
        # Draw shadow if enabled
        if self.shadow_effect:
            shadow_rect = rect.copy()
            shadow_rect.x += 1
            shadow_rect.y += 1
            self.display.draw_rect(shadow_rect, 'black', True)
        
        # Draw tail with special styling
        self.display.draw_rect(rect, colors['tail'], True)
        self.display.draw_rect(rect, colors['outline'], False, 2)
        
        # Add tail-specific effects
        self._add_tail_effects(rect)
    
    def _calculate_wave_offset(self, segment_index: int, time: float) -> float:
        """Calculate wave offset for a segment based on its position and time."""
        if not self.wave_effect:
            return 0.0
        
        # Create a wave that propagates along the snake
        wave_phase = time * self.movement_speed - segment_index * 0.5
        return math.sin(wave_phase) * self.wave_amplitude
    
    def _get_growth_scale(self, position: Position) -> float:
        """Get the growth scale for a segment at the given position."""
        for animation_data in self.growth_animations.values():
            if (animation_data['position'].x == position.x and 
                animation_data['position'].y == position.y):
                progress = animation_data['elapsed'] / animation_data['duration']
                return animation_data['initial_scale'] + (animation_data['target_scale'] - animation_data['initial_scale']) * progress
        
        return 1.0
    
    def _scale_rect(self, rect: pygame.Rect, scale: float) -> pygame.Rect:
        """Scale a rectangle from its center."""
        scaled_rect = rect.copy()
        scaled_rect.width = int(rect.width * scale)
        scaled_rect.height = int(rect.height * scale)
        scaled_rect.center = rect.center
        return scaled_rect
    
    def _render_rounded_segment(self, rect: pygame.Rect, fill_color: str, outline_color: str) -> None:
        """Render a segment with rounded corners."""
        # For now, use regular rectangle with outline
        # In a more advanced implementation, we could use pygame.draw.rect with border_radius
        self.display.draw_rect(rect, fill_color, True)
        self.display.draw_rect(rect, outline_color, False, 1)
    
    def _add_segment_effects(self, rect: pygame.Rect, segment_index: int, total_segments: int) -> None:
        """Add special effects to body segments."""
        # Add subtle glow effect to middle segments
        if segment_index > 0 and segment_index < total_segments - 1:
            if self.glow_effect:
                self._add_subtle_glow(rect, 'white', 0.3)
    
    def _add_tail_effects(self, rect: pygame.Rect) -> None:
        """Add special effects to the tail segment."""
        # Add a subtle pulse effect
        pulse_factor = (math.sin(self.animation_timer * 8) + 1) / 2
        pulse_alpha = int(100 * pulse_factor)
        
        if pulse_alpha > 0:
            # Create a subtle glow around the tail
            glow_rect = rect.inflate(4, 4)
            glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (255, 255, 255, pulse_alpha), glow_surface.get_rect())
            self.display.screen.blit(glow_surface, glow_rect)
    
    def _add_glow_effect(self, rect: pygame.Rect, color: str) -> None:
        """Add a glow effect around the given rectangle."""
        if not self.glow_effect:
            return
        
        # Create a larger rectangle for the glow
        glow_rect = rect.inflate(8, 8)
        glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        
        # Draw multiple layers for glow effect
        for i in range(3):
            alpha = 50 - i * 15
            if alpha > 0:
                glow_color = self.display.get_color(color)
                glow_color = (*glow_color, alpha)
                pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), border_radius=2)
        
        self.display.screen.blit(glow_surface, glow_rect)
    
    def _add_subtle_glow(self, rect: pygame.Rect, color: str, intensity: float) -> None:
        """Add a subtle glow effect."""
        if not self.glow_effect:
            return
        
        glow_rect = rect.inflate(4, 4)
        glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        
        alpha = int(50 * intensity)
        if alpha > 0:
            glow_color = self.display.get_color(color)
            glow_color = (*glow_color, alpha)
            pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect())
            self.display.screen.blit(glow_surface, glow_rect)
    
    def _calculate_segment_color_variation(self, segment_index: int, total_segments: int) -> float:
        """Calculate color variation for a segment."""
        if total_segments <= 1:
            return 0.0
        
        # Create a wave pattern along the snake
        normalized_position = segment_index / (total_segments - 1)
        wave = math.sin(normalized_position * math.pi * 2 + self.animation_timer * 3)
        return (wave + 1) / 2  # Normalize to 0-1
    
    def _blend_colors(self, color1: str, color2: str, factor: float) -> str:
        """Blend two colors based on a factor (0-1)."""
        # For now, return the first color
        # In a more advanced implementation, we could blend RGB values
        return color1 if factor < 0.5 else color2
    
    def set_wave_effect(self, enabled: bool) -> None:
        """Enable or disable the wave effect."""
        self.wave_effect = enabled
    
    def set_growth_effect(self, enabled: bool) -> None:
        """Enable or disable the growth effect."""
        self.growth_effect = enabled
    
    def set_glow_effect(self, enabled: bool) -> None:
        """Enable or disable the glow effect."""
        self.glow_effect = enabled
    
    def set_shadow_effect(self, enabled: bool) -> None:
        """Enable or disable the shadow effect."""
        self.shadow_effect = enabled
    
    def set_animation_speed(self, speed: float) -> None:
        """Set the animation speed multiplier."""
        self.animation_speed = speed
    
    def set_movement_speed(self, speed: float) -> None:
        """Set the movement wave speed."""
        self.movement_speed = speed
    
    def set_wave_amplitude(self, amplitude: float) -> None:
        """Set the wave amplitude in pixels."""
        self.wave_amplitude = amplitude
