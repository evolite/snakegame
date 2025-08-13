"""
Food Renderer

This module provides specialized rendering for food items with:
- Animated food sprites
- Visual effects for different food types
- Collection animations
- Particle effects
"""

import pygame
import math
from typing import List, Tuple, Dict
from ..game.grid import Position
from ..game.food import Food, FoodType
from .display import DisplayManager


class FoodRenderer:
    """
    Specialized renderer for food visualization.
    
    Provides animated and visually appealing food rendering.
    """
    
    def __init__(self, display_manager: DisplayManager):
        """Initialize the food renderer."""
        self.display = display_manager
        self.cell_size = display_manager.get_cell_size()
        
        # Animation properties
        self.animation_timer = 0.0
        self.animation_speed = 1.0  # seconds per cycle
        
        # Food visual properties
        self.food_effects = {
            FoodType.NORMAL: {
                'color': 'red',
                'animation': 'pulse',
                'particles': False,
                'glow': False
            },
            FoodType.BONUS: {
                'color': 'gold',
                'animation': 'rotate',
                'particles': True,
                'glow': True
            },
            FoodType.SPEED_UP: {
                'color': 'blue',
                'animation': 'flash',
                'particles': True,
                'glow': True
            },
            FoodType.SPEED_DOWN: {
                'color': 'purple',
                'animation': 'slow_pulse',
                'particles': False,
                'glow': False
            },
            FoodType.DOUBLE_POINTS: {
                'color': 'green',
                'animation': 'bounce',
                'particles': True,
                'glow': True
            },
            FoodType.INVINCIBILITY: {
                'color': 'white',
                'animation': 'sparkle',
                'particles': True,
                'glow': True
            }
        }
        
        # Particle system
        self.particles = []
        self.particle_lifetime = 2.0  # seconds
        
        # Collection animation
        self.collection_animations = []
    
    def update(self, delta_time: float) -> None:
        """Update the food renderer."""
        self.animation_timer += delta_time
        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0.0
        
        # Update particles
        self._update_particles(delta_time)
        
        # Update collection animations
        self._update_collection_animations(delta_time)
    
    def render_food(self, food_list: List[Food]) -> None:
        """Render all food items."""
        for food in food_list:
            if not food.is_collected():
                self._render_food_item(food)
        
        # Render particles
        self._render_particles()
        
        # Render collection animations
        self._render_collection_animations()
    
    def _render_food_item(self, food: Food) -> None:
        """Render a single food item with animations."""
        position = food.get_position()
        food_type = food.get_effect_type()
        effects = self.food_effects[food_type]
        
        # Get base color
        color = effects['color']
        
        # Calculate center position
        rect = self.display.get_grid_rect(position.x, position.y)
        center = rect.center
        
        # Apply animation based on food type
        if effects['animation'] == 'pulse':
            self._render_pulsing_food(center, color, food_type)
        elif effects['animation'] == 'rotate':
            self._render_rotating_food(center, color, food_type)
        elif effects['animation'] == 'flash':
            self._render_flashing_food(center, color, food_type)
        elif effects['animation'] == 'slow_pulse':
            self._render_slow_pulsing_food(center, color, food_type)
        elif effects['animation'] == 'bounce':
            self._render_bouncing_food(center, color, food_type)
        elif effects['animation'] == 'sparkle':
            self._render_sparkling_food(center, color, food_type)
        else:
            self._render_static_food(center, color, food_type)
        
        # Add glow effect if enabled
        if effects['glow']:
            self._add_food_glow(center, color)
        
        # Add particles if enabled
        if effects['particles']:
            self._add_food_particles(center, color)
    
    def _render_pulsing_food(self, center: Tuple[int, int], color: str, food_type: FoodType) -> None:
        """Render food with a pulsing animation."""
        # Calculate pulse size
        pulse_factor = (math.sin(self.animation_timer * 8) + 1) / 2
        base_size = self.cell_size // 6
        pulse_size = int(base_size * (0.8 + 0.4 * pulse_factor))
        
        # Draw pulsing circle
        self.display.draw_circle(center, pulse_size, color, True)
        
        # Add outline
        self.display.draw_circle(center, pulse_size, 'white', False, 1)
    
    def _render_rotating_food(self, center: Tuple[int, int], color: str, food_type: FoodType) -> None:
        """Render food with a rotating animation."""
        # Calculate rotation angle
        rotation_angle = self.animation_timer * 360  # degrees per second
        
        # Draw star shape with rotation
        self._render_rotating_star(center, color, rotation_angle)
    
    def _render_rotating_star(self, center: Tuple[int, int], color: str, angle: float) -> None:
        """Render a rotating star."""
        size = self.cell_size // 4
        points = []
        
        # Create star points with rotation
        for i in range(10):
            point_angle = (i * 36 + angle) * math.pi / 180
            if i % 2 == 0:
                radius = size
            else:
                radius = size // 2
            
            x = center[0] + radius * math.cos(point_angle)
            y = center[1] + radius * math.sin(point_angle)
            points.append((x, y))
        
        # Draw rotating star
        if len(points) >= 3:
            self.display.draw_polygon(points, color)
    
    def _render_flashing_food(self, center: Tuple[int, int], color: str, food_type: FoodType) -> None:
        """Render food with a flashing animation."""
        # Calculate flash intensity
        flash_factor = (math.sin(self.animation_timer * 12) + 1) / 2
        
        # Alternate between color and white
        if flash_factor > 0.5:
            draw_color = 'white'
        else:
            draw_color = color
        
        # Draw lightning bolt
        self._render_lightning_bolt(center, draw_color)
    
    def _render_lightning_bolt(self, center: Tuple[int, int], color: str) -> None:
        """Render a lightning bolt shape."""
        size = self.cell_size // 4
        points = [
            (center[0], center[1] - size),
            (center[0] - size//2, center[1] - size//4),
            (center[0] + size//2, center[1] + size//4),
            (center[0], center[1] + size)
        ]
        
        self.display.draw_polygon(points, color)
    
    def _render_slow_pulsing_food(self, center: Tuple[int, int], color: str, food_type: FoodType) -> None:
        """Render food with a slow pulsing animation."""
        # Calculate slow pulse size
        pulse_factor = (math.sin(self.animation_timer * 2) + 1) / 2
        base_size = self.cell_size // 6
        pulse_size = int(base_size * (0.7 + 0.6 * pulse_factor))
        
        # Draw slow pulsing circle
        self.display.draw_circle(center, pulse_size, color, True)
        
        # Add spiral pattern
        self._render_spiral_pattern(center, color, pulse_size)
    
    def _render_spiral_pattern(self, center: Tuple[int, int], color: str, size: int) -> None:
        """Render a spiral pattern."""
        # Draw concentric circles
        for i in range(3):
            circle_size = size - (i * 2)
            if circle_size > 0:
                self.display.draw_circle(center, circle_size, 'white', False, 1)
    
    def _render_bouncing_food(self, center: Tuple[int, int], color: str, food_type: FoodType) -> None:
        """Render food with a bouncing animation."""
        # Calculate bounce offset
        bounce_factor = abs(math.sin(self.animation_timer * 6))
        bounce_offset = int(bounce_factor * 4)
        
        # Draw bouncing 2x symbol
        bounce_center = (center[0], center[1] - bounce_offset)
        self.display.draw_text("2×", bounce_center, self.display.large_font, color, True)
    
    def _render_sparkling_food(self, center: Tuple[int, int], color: str, food_type: FoodType) -> None:
        """Render food with a sparkling animation."""
        # Draw base shield
        self._render_shield(center, color)
        
        # Add sparkles
        self._add_sparkles(center, color)
    
    def _render_shield(self, center: Tuple[int, int], color: str) -> None:
        """Render a shield shape."""
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
    
    def _add_sparkles(self, center: Tuple[int, int], color: str) -> None:
        """Add sparkle effects around the food."""
        sparkle_count = 6
        sparkle_size = 2
        
        for i in range(sparkle_count):
            angle = (i * 360 / sparkle_count + self.animation_timer * 180) * math.pi / 180
            distance = self.cell_size // 3
            
            sparkle_x = center[0] + distance * math.cos(angle)
            sparkle_y = center[1] + distance * math.sin(angle)
            sparkle_pos = (int(sparkle_x), int(sparkle_y))
            
            # Alternate sparkle colors
            sparkle_color = 'yellow' if i % 2 == 0 else 'white'
            self.display.draw_circle(sparkle_pos, sparkle_size, sparkle_color)
    
    def _render_static_food(self, center: Tuple[int, int], color: str, food_type: FoodType) -> None:
        """Render static food (fallback)."""
        radius = self.cell_size // 6
        self.display.draw_circle(center, radius, color, True)
        self.display.draw_circle(center, radius, 'white', False, 1)
    
    def _add_food_glow(self, center: Tuple[int, int], color: str) -> None:
        """Add a glow effect around the food."""
        # Create glow surface
        glow_size = self.cell_size // 2
        glow_rect = pygame.Rect(
            center[0] - glow_size, center[1] - glow_size,
            glow_size * 2, glow_size * 2
        )
        
        glow_surface = pygame.Surface(glow_rect.size)
        glow_surface.set_alpha(64)
        glow_surface.fill(self.display.get_color(color))
        
        # Draw glow
        self.display.screen.blit(glow_surface, glow_rect)
    
    def _add_food_particles(self, center: Tuple[int, int], color: str) -> None:
        """Add particle effects around the food."""
        # Create new particles occasionally
        if len(self.particles) < 10 and self.animation_timer % 0.2 < 0.016:
            particle = {
                'x': center[0],
                'y': center[1],
                'vx': (math.random() - 0.5) * 2,
                'vy': (math.random() - 0.5) * 2,
                'life': self.particle_lifetime,
                'color': color,
                'size': 1
            }
            self.particles.append(particle)
    
    def _update_particles(self, delta_time: float) -> None:
        """Update particle positions and lifetimes."""
        for particle in self.particles[:]:
            # Update position
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Update life
            particle['life'] -= delta_time
            
            # Remove dead particles
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def _render_particles(self) -> None:
        """Render all particles."""
        for particle in self.particles:
            # Calculate alpha based on remaining life
            alpha = int(255 * (particle['life'] / self.particle_lifetime))
            
            # Create particle surface
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2))
            particle_surface.set_alpha(alpha)
            particle_surface.fill(self.display.get_color(particle['color']))
            
            # Draw particle
            pos = (int(particle['x'] - particle['size']), int(particle['y'] - particle['size']))
            self.display.screen.blit(particle_surface, pos)
    
    def add_collection_animation(self, position: Position, food_type: FoodType) -> None:
        """Add a collection animation when food is eaten."""
        animation = {
            'position': position,
            'food_type': food_type,
            'timer': 0.0,
            'duration': 0.5,
            'particles': []
        }
        
        # Create collection particles
        for _ in range(8):
            particle = {
                'x': position.x * self.cell_size + self.cell_size // 2,
                'y': position.y * self.cell_size + self.cell_size // 2,
                'vx': (math.random() - 0.5) * 4,
                'vy': (math.random() - 0.5) * 4,
                'life': 0.5,
                'color': self.food_effects[food_type]['color'],
                'size': 2
            }
            animation['particles'].append(particle)
        
        self.collection_animations.append(animation)
    
    def _update_collection_animations(self, delta_time: float) -> None:
        """Update collection animation timers."""
        for animation in self.collection_animations[:]:
            animation['timer'] += delta_time
            
            # Update particles
            for particle in animation['particles']:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['life'] -= delta_time
            
            # Remove dead animations
            if animation['timer'] >= animation['duration']:
                self.collection_animations.remove(animation)
    
    def _render_collection_animations(self) -> None:
        """Render collection animations."""
        for animation in self.collection_animations:
            # Calculate animation progress
            progress = animation['timer'] / animation['duration']
            
            # Render particles
            for particle in animation['particles']:
                if particle['life'] > 0:
                    # Calculate alpha based on remaining life
                    alpha = int(255 * (particle['life'] / 0.5))
                    
                    # Create particle surface
                    particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2))
                    particle_surface.set_alpha(alpha)
                    particle_surface.fill(self.display.get_color(particle['color']))
                    
                    # Draw particle
                    pos = (int(particle['x'] - particle['size']), int(particle['y'] - particle['size']))
                    self.display.screen.blit(particle_surface, pos)
    
    def set_animation_speed(self, speed: float) -> None:
        """Set the animation speed multiplier."""
        self.animation_speed = speed
    
    def enable_particles(self, enabled: bool) -> None:
        """Enable or disable particle effects."""
        for food_type in self.food_effects:
            self.food_effects[food_type]['particles'] = enabled
    
    def enable_glow(self, enabled: bool) -> None:
        """Enable or disable glow effects."""
        for food_type in self.food_effects:
            self.food_effects[food_type]['glow'] = enabled
    
    def get_food_effects(self) -> Dict[FoodType, Dict]:
        """Get the current food effects configuration."""
        return self.food_effects.copy()
    
    def set_food_effect(self, food_type: FoodType, effect: str, value: any) -> None:
        """Set a specific food effect property."""
        if food_type in self.food_effects and effect in self.food_effects[food_type]:
            self.food_effects[food_type][effect] = value
