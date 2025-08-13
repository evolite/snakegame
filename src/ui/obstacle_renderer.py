"""
Obstacle Renderer

This module provides specialized rendering for obstacles and walls with:
- Visual differentiation between obstacle types
- Animations and effects for moving obstacles
- Visual feedback for obstacle states
- Integration with the visual effects system
"""

import pygame
import math
from typing import List, Dict, Any, Tuple
from ..game.obstacles import Obstacle, ObstacleType, ObstacleBehavior
from .display import DisplayManager
import random


class ObstacleRenderer:
    """
    Specialized renderer for obstacle visualization.
    
    Provides visual feedback for different obstacle types and states.
    """
    
    def __init__(self, display_manager: DisplayManager):
        """Initialize the obstacle renderer."""
        self.display = display_manager
        
        # Obstacle rendering settings
        self.obstacle_size = self.display.get_cell_size()
        self.show_obstacle_info = True
        
        # Color schemes for different obstacle types
        self.obstacle_colors = {
            ObstacleType.STATIC_WALL: 'gray',
            ObstacleType.BREAKABLE_WALL: 'brown',
            ObstacleType.MOVING_OBSTACLE: 'orange',
            ObstacleType.SPIKE_TRAP: 'red',
            ObstacleType.TELEPORTER: 'purple',
            ObstacleType.SPEED_PAD: 'blue',
            ObstacleType.SCORE_MULTIPLIER: 'gold',
            ObstacleType.SAFE_ZONE: 'green'
        }
        
        # Visual effects for different behaviors
        self.behavior_effects = {
            ObstacleBehavior.SOLID: ['solid'],
            ObstacleBehavior.BREAKABLE: ['breakable', 'cracked'],
            ObstacleBehavior.MOVING: ['moving', 'pulse'],
            ObstacleBehavior.HAZARDOUS: ['hazardous', 'warning'],
            ObstacleBehavior.BENEFICIAL: ['beneficial', 'glow'],
            ObstacleBehavior.TELEPORTING: ['teleporting', 'swirl']
        }
        
        # Animation properties
        self.animation_timer = 0.0
        self.animation_speed = 2.0  # seconds per cycle
    
    def render_obstacles(self, obstacles: List[Obstacle], surface: pygame.Surface) -> None:
        """
        Render all obstacles on the specified surface.
        
        Args:
            obstacles: List of obstacles to render
            surface: Surface to render on
        """
        for obstacle in obstacles:
            if obstacle.is_active():
                self._render_single_obstacle(obstacle, surface)
    
    def _render_single_obstacle(self, obstacle: Obstacle, surface: pygame.Surface) -> None:
        """Render a single obstacle with appropriate styling."""
        position = obstacle.get_position()
        obstacle_type = obstacle.get_type()
        behavior = obstacle.get_behavior()
        visual_state = obstacle.get_visual_state()
        
        # Get base color for obstacle type
        base_color = self.obstacle_colors.get(obstacle_type, 'white')
        
        # Calculate screen position
        screen_x = position.x * self.obstacle_size
        screen_y = position.y * self.obstacle_size
        
        # Create obstacle rectangle
        obstacle_rect = pygame.Rect(screen_x, screen_y, self.obstacle_size, self.obstacle_size)
        
        # Render based on obstacle type
        if obstacle_type == ObstacleType.STATIC_WALL:
            self._render_static_wall(obstacle, obstacle_rect, surface, base_color)
        elif obstacle_type == ObstacleType.BREAKABLE_WALL:
            self._render_breakable_wall(obstacle, obstacle_rect, surface, base_color)
        elif obstacle_type == ObstacleType.MOVING_OBSTACLE:
            self._render_moving_obstacle(obstacle, obstacle_rect, surface, base_color)
        elif obstacle_type == ObstacleType.SPIKE_TRAP:
            self._render_spike_trap(obstacle, obstacle_rect, surface, base_color)
        elif obstacle_type == ObstacleType.TELEPORTER:
            self._render_teleporter(obstacle, obstacle_rect, surface, base_color)
        elif obstacle_type == ObstacleType.SPEED_PAD:
            self._render_speed_pad(obstacle, obstacle_rect, surface, base_color)
        elif obstacle_type == ObstacleType.SCORE_MULTIPLIER:
            self._render_score_multiplier(obstacle, obstacle_rect, surface, base_color)
        elif obstacle_type == ObstacleType.SAFE_ZONE:
            self._render_safe_zone(obstacle, obstacle_rect, surface, base_color)
        else:
            # Default rendering
            self._render_default_obstacle(obstacle, obstacle_rect, surface, base_color)
        
        # Add visual effects based on behavior
        self._add_behavior_effects(obstacle, obstacle_rect, surface, behavior)
        
        # Add state-specific effects
        self._add_state_effects(obstacle, obstacle_rect, surface, visual_state)
    
    def _render_static_wall(self, obstacle: Obstacle, rect: pygame.Rect, 
                           surface: pygame.Surface, color: str) -> None:
        """Render a static wall obstacle."""
        # Draw main wall
        pygame.draw.rect(surface, self.display.get_color(color), rect)
        pygame.draw.rect(surface, self.display.get_color('dark_gray'), rect, 2)
        
        # Add brick pattern
        self._add_brick_pattern(surface, rect, color)
    
    def _render_breakable_wall(self, obstacle: Obstacle, rect: pygame.Rect, 
                              surface: pygame.Surface, color: str) -> None:
        """Render a breakable wall obstacle."""
        # Draw main wall
        pygame.draw.rect(surface, self.display.get_color(color), rect)
        pygame.draw.rect(surface, self.display.get_color('dark_brown'), rect, 2)
        
        # Add cracks based on health
        health = obstacle.get_health()
        max_health = obstacle.properties.health
        crack_intensity = 1.0 - (health / max_health)
        
        if crack_intensity > 0:
            self._add_crack_pattern(surface, rect, crack_intensity)
        
        # Add health indicator
        if self.show_obstacle_info:
            self._render_health_indicator(obstacle, rect, surface)
    
    def _render_moving_obstacle(self, obstacle: Obstacle, rect: pygame.Rect, 
                               surface: pygame.Surface, color: str) -> None:
        """Render a moving obstacle."""
        # Draw main obstacle
        pygame.draw.rect(surface, self.display.get_color(color), rect)
        pygame.draw.rect(surface, self.display.get_color('dark_orange'), rect, 2)
        
        # Add movement indicator
        if obstacle.is_moving():
            self._add_movement_indicator(surface, rect, obstacle)
        
        # Add direction arrow
        self._add_direction_arrow(surface, rect, obstacle.movement_direction)
    
    def _render_spike_trap(self, obstacle: Obstacle, rect: pygame.Rect, 
                          surface: pygame.Surface, color: str) -> None:
        """Render a spike trap obstacle."""
        # Draw base
        pygame.draw.rect(surface, self.display.get_color('dark_red'), rect)
        
        # Draw spikes
        self._add_spike_pattern(surface, rect, color)
        
        # Add warning effect
        if obstacle.get_visual_state() == "normal":
            self._add_warning_effect(surface, rect)
    
    def _render_teleporter(self, obstacle: Obstacle, rect: pygame.Rect, 
                          surface: pygame.Surface, color: str) -> None:
        """Render a teleporter obstacle."""
        # Draw base
        pygame.draw.rect(surface, self.display.get_color(color), rect)
        pygame.draw.rect(surface, self.display.get_color('white'), rect, 2)
        
        # Add teleporter symbol
        self._add_teleporter_symbol(surface, rect)
        
        # Add swirling effect
        self._add_swirling_effect(surface, rect, obstacle)
    
    def _render_speed_pad(self, obstacle: Obstacle, rect: pygame.Rect, 
                         surface: pygame.Surface, color: str) -> None:
        """Render a speed pad obstacle."""
        # Draw base
        pygame.draw.rect(surface, self.display.get_color(color), rect)
        pygame.draw.rect(surface, self.display.get_color('white'), rect, 2)
        
        # Add speed symbol
        self._add_speed_symbol(surface, rect)
        
        # Add activation effect if active
        if obstacle.effect_active:
            self._add_activation_effect(surface, rect)
    
    def _render_score_multiplier(self, obstacle: Obstacle, rect: pygame.Rect, 
                                surface: pygame.Surface, color: str) -> None:
        """Render a score multiplier obstacle."""
        # Draw base
        pygame.draw.rect(surface, self.display.get_color(color), rect)
        pygame.draw.rect(surface, self.display.get_color('white'), rect, 2)
        
        # Add multiplier symbol
        self._add_multiplier_symbol(surface, rect)
        
        # Add glow effect
        self._add_glow_effect(surface, rect, obstacle)
    
    def _render_safe_zone(self, obstacle: Obstacle, rect: pygame.Rect, 
                         surface: pygame.Surface, color: str) -> None:
        """Render a safe zone obstacle."""
        # Draw base with transparency effect
        safe_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(safe_surface, (*self.display.get_color(color), 128), safe_surface.get_rect())
        surface.blit(safe_surface, rect)
        
        # Add border
        pygame.draw.rect(surface, self.display.get_color('white'), rect, 2)
        
        # Add safe zone symbol
        self._add_safe_zone_symbol(surface, rect)
        
        # Add protection effect if active
        if obstacle.effect_active:
            self._add_protection_effect(surface, rect)
    
    def _render_default_obstacle(self, obstacle: Obstacle, rect: pygame.Rect, 
                                surface: pygame.Surface, color: str) -> None:
        """Render a default obstacle."""
        pygame.draw.rect(surface, self.display.get_color(color), rect)
        pygame.draw.rect(surface, self.display.get_color('black'), rect, 1)
    
    def _add_brick_pattern(self, surface: pygame.Surface, rect: pygame.Rect, color: str) -> None:
        """Add brick pattern to walls."""
        brick_size = max(2, self.obstacle_size // 8)
        
        for x in range(rect.left, rect.right, brick_size):
            for y in range(rect.top, rect.bottom, brick_size):
                if (x + y) % (brick_size * 2) == 0:
                    brick_rect = pygame.Rect(x, y, brick_size, brick_size)
                    pygame.draw.rect(surface, self.display.get_color('dark_gray'), brick_rect)
    
    def _add_crack_pattern(self, surface: pygame.Surface, rect: pygame.Rect, intensity: float) -> None:
        """Add crack pattern to breakable walls."""
        if intensity < 0.3:
            return
        
        # Draw cracks based on intensity
        num_cracks = int(intensity * 5) + 1
        
        for _ in range(num_cracks):
            start_x = rect.left + random.randint(0, rect.width)
            start_y = rect.top + random.randint(0, rect.height)
            end_x = start_x + random.randint(-rect.width//2, rect.width//2)
            end_y = start_y + random.randint(-rect.height//2, rect.height//2)
            
            pygame.draw.line(surface, self.display.get_color('black'), 
                           (start_x, start_y), (end_x, end_y), 2)
    
    def _add_movement_indicator(self, surface: pygame.Surface, rect: pygame.Rect, 
                               obstacle: Obstacle) -> None:
        """Add movement indicator for moving obstacles."""
        # Draw movement trail
        if hasattr(obstacle, 'patrol_points') and obstacle.patrol_points:
            trail_color = self.display.get_color('light_orange')
            trail_alpha = 64
            
            trail_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            pygame.draw.rect(trail_surface, (*trail_color, trail_alpha), trail_surface.get_rect())
            
            # Draw trail at previous positions
            for i in range(len(obstacle.patrol_points)):
                if i != obstacle.current_patrol_index:
                    point = obstacle.patrol_points[i]
                    trail_x = point.x * self.obstacle_size
                    trail_y = point.y * self.obstacle_size
                    trail_rect = pygame.Rect(trail_x, trail_y, self.obstacle_size, self.obstacle_size)
                    surface.blit(trail_surface, trail_rect)
    
    def _add_direction_arrow(self, surface: pygame.Surface, rect: pygame.Rect, 
                            direction: Tuple[int, int]) -> None:
        """Add direction arrow for moving obstacles."""
        center_x = rect.centerx
        center_y = rect.centery
        arrow_size = max(3, self.obstacle_size // 6)
        
        # Calculate arrow points
        if direction == (1, 0):  # Right
            points = [(center_x - arrow_size, center_y - arrow_size),
                     (center_x + arrow_size, center_y),
                     (center_x - arrow_size, center_y + arrow_size)]
        elif direction == (-1, 0):  # Left
            points = [(center_x + arrow_size, center_y - arrow_size),
                     (center_x - arrow_size, center_y),
                     (center_x + arrow_size, center_y + arrow_size)]
        elif direction == (0, 1):  # Down
            points = [(center_x - arrow_size, center_y - arrow_size),
                     (center_x, center_y + arrow_size),
                     (center_x + arrow_size, center_y - arrow_size)]
        else:  # Up
            points = [(center_x - arrow_size, center_y + arrow_size),
                     (center_x, center_y - arrow_size),
                     (center_x + arrow_size, center_y + arrow_size)]
        
        pygame.draw.polygon(surface, self.display.get_color('white'), points)
    
    def _add_spike_pattern(self, surface: pygame.Surface, rect: pygame.Rect, color: str) -> None:
        """Add spike pattern to spike traps."""
        spike_color = self.display.get_color(color)
        spike_size = max(2, self.obstacle_size // 4)
        
        # Draw spikes in a grid pattern
        for x in range(rect.left + spike_size, rect.right - spike_size, spike_size * 2):
            for y in range(rect.top + spike_size, rect.bottom - spike_size, spike_size * 2):
                # Triangle spike pointing up
                points = [(x, y + spike_size), (x - spike_size//2, y), (x + spike_size//2, y)]
                pygame.draw.polygon(surface, spike_color, points)
    
    def _add_warning_effect(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Add warning effect to hazardous obstacles."""
        # Pulsing border effect
        pulse_alpha = int(128 * (1 + math.sin(self.animation_timer * 4) * 0.5))
        warning_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(warning_surface, (*self.display.get_color('yellow'), pulse_alpha), 
                        warning_surface.get_rect(), 3)
        surface.blit(warning_surface, rect)
    
    def _add_teleporter_symbol(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Add teleporter symbol."""
        center_x = rect.centerx
        center_y = rect.centery
        symbol_size = max(4, self.obstacle_size // 5)
        
        # Draw teleporter symbol (infinity symbol)
        points = [
            (center_x - symbol_size, center_y),
            (center_x - symbol_size//2, center_y - symbol_size//2),
            (center_x + symbol_size//2, center_y - symbol_size//2),
            (center_x + symbol_size, center_y),
            (center_x + symbol_size//2, center_y + symbol_size//2),
            (center_x - symbol_size//2, center_y + symbol_size//2)
        ]
        
        pygame.draw.lines(surface, self.display.get_color('white'), True, points, 2)
    
    def _add_swirling_effect(self, surface: pygame.Surface, rect: pygame.Rect, 
                            obstacle: Obstacle) -> None:
        """Add swirling effect to teleporters."""
        # Rotating swirl effect
        angle = self.animation_timer * 3.0  # 3 radians per second
        swirl_radius = max(2, self.obstacle_size // 8)
        
        center_x = rect.centerx
        center_y = rect.centery
        
        for i in range(8):
            swirl_angle = angle + (i * math.pi / 4)
            x = center_x + int(swirl_radius * math.cos(swirl_angle))
            y = center_y + int(swirl_radius * math.sin(swirl_angle))
            
            pygame.draw.circle(surface, self.display.get_color('white'), (x, y), 1)
    
    def _add_speed_symbol(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Add speed symbol to speed pads."""
        center_x = rect.centerx
        center_y = rect.centery
        symbol_size = max(3, self.obstacle_size // 6)
        
        # Draw lightning bolt symbol
        points = [
            (center_x, center_y - symbol_size),
            (center_x - symbol_size//2, center_y - symbol_size//4),
            (center_x + symbol_size//2, center_y + symbol_size//4),
            (center_x, center_y + symbol_size)
        ]
        
        pygame.draw.polygon(surface, self.display.get_color('white'), points)
    
    def _add_multiplier_symbol(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Add multiplier symbol to score multipliers."""
        center_x = rect.centerx
        center_y = rect.centery
        
        # Draw "×" symbol
        symbol_size = max(4, self.obstacle_size // 5)
        
        # Horizontal line
        pygame.draw.line(surface, self.display.get_color('white'),
                        (center_x - symbol_size, center_y),
                        (center_x + symbol_size, center_y), 2)
        
        # Vertical line
        pygame.draw.line(surface, self.display.get_color('white'),
                        (center_x, center_y - symbol_size),
                        (center_x, center_y + symbol_size), 2)
    
    def _add_glow_effect(self, surface: pygame.Surface, rect: pygame.Rect, 
                         obstacle: Obstacle) -> None:
        """Add glow effect to beneficial obstacles."""
        # Pulsing glow effect
        glow_alpha = int(64 * (1 + math.sin(self.animation_timer * 3) * 0.5))
        glow_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (*self.display.get_color('yellow'), glow_alpha), 
                        glow_surface.get_rect())
        surface.blit(glow_surface, rect)
    
    def _add_safe_zone_symbol(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Add safe zone symbol."""
        center_x = rect.centerx
        center_y = rect.centery
        symbol_size = max(3, self.obstacle_size // 6)
        
        # Draw shield symbol
        pygame.draw.circle(surface, self.display.get_color('white'), 
                         (center_x, center_y), symbol_size, 2)
        
        # Draw cross in center
        cross_size = symbol_size // 2
        pygame.draw.line(surface, self.display.get_color('white'),
                        (center_x - cross_size, center_y),
                        (center_x + cross_size, center_y), 2)
        pygame.draw.line(surface, self.display.get_color('white'),
                        (center_x, center_y - cross_size),
                        (center_x, center_y + cross_size), 2)
    
    def _add_protection_effect(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Add protection effect to active safe zones."""
        # Rotating protection ring
        angle = self.animation_timer * 2.0  # 2 radians per second
        ring_radius = max(4, self.obstacle_size // 3)
        
        center_x = rect.centerx
        center_y = rect.centery
        
        # Draw rotating protection dots
        for i in range(6):
            dot_angle = angle + (i * math.pi / 3)
            x = center_x + int(ring_radius * math.cos(dot_angle))
            y = center_y + int(ring_radius * math.sin(dot_angle))
            
            pygame.draw.circle(surface, self.display.get_color('white'), (x, y), 2)
    
    def _add_behavior_effects(self, obstacle: Obstacle, rect: pygame.Rect, 
                             surface: pygame.Surface, behavior: ObstacleBehavior) -> None:
        """Add visual effects based on obstacle behavior."""
        if behavior == ObstacleBehavior.MOVING:
            # Add movement trail effect
            pass
        elif behavior == ObstacleBehavior.HAZARDOUS:
            # Add warning effects
            pass
        elif behavior == ObstacleBehavior.BENEFICIAL:
            # Add beneficial effects
            pass
    
    def _add_state_effects(self, obstacle: Obstacle, rect: pygame.Rect, 
                          surface: pygame.Surface, visual_state: str) -> None:
        """Add visual effects based on obstacle state."""
        if visual_state == "destroyed":
            # Add destruction effects
            self._add_destruction_effect(surface, rect)
        elif visual_state == "active":
            # Add activation effects
            self._add_activation_effect(surface, rect)
        elif visual_state == "moving":
            # Add movement effects
            pass
    
    def _add_destruction_effect(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Add destruction effect for destroyed obstacles."""
        # Particle effect simulation
        for _ in range(5):
            x = rect.centerx + random.randint(-rect.width//2, rect.width//2)
            y = rect.centery + random.randint(-rect.height//2, rect.height//2)
            
            pygame.draw.circle(surface, self.display.get_color('gray'), (x, y), 1)
    
    def _add_activation_effect(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Add activation effect for active obstacles."""
        # Bright border effect
        activation_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(activation_surface, (*self.display.get_color('yellow'), 128), 
                        activation_surface.get_rect(), 3)
        surface.blit(activation_surface, rect)
    
    def _render_health_indicator(self, obstacle: Obstacle, rect: pygame.Rect, 
                                surface: pygame.Surface) -> None:
        """Render health indicator for breakable obstacles."""
        if not obstacle.is_breakable():
            return
        
        health = obstacle.get_health()
        max_health = obstacle.properties.health
        
        if health < max_health:
            # Draw health bar
            bar_width = rect.width - 4
            bar_height = 3
            bar_x = rect.x + 2
            bar_y = rect.y + 2
            
            # Background
            pygame.draw.rect(surface, self.display.get_color('dark_red'),
                           (bar_x, bar_y, bar_width, bar_height))
            
            # Health fill
            health_width = int((health / max_health) * bar_width)
            if health_width > 0:
                health_color = 'green' if health > max_health // 2 else 'yellow'
                pygame.draw.rect(surface, self.display.get_color(health_color),
                               (bar_x, bar_y, health_width, bar_height))
    
    def update_animation(self, delta_time: float) -> None:
        """Update animation timer for visual effects."""
        self.animation_timer += delta_time
        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0.0
    
    def set_show_obstacle_info(self, show: bool) -> None:
        """Set whether to show obstacle information."""
        self.show_obstacle_info = show
    
    def get_obstacle_color(self, obstacle_type: ObstacleType) -> str:
        """Get the color for a specific obstacle type."""
        return self.obstacle_colors.get(obstacle_type, 'white')
