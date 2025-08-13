"""
Food Renderer

This module provides specialized rendering for food items with:
- Animated food sprites
- Visual effects for different food types
- Collection animations
- Particle effects
- Enhanced visual feedback
"""

import pygame
import math
import random
from typing import List, Tuple, Dict, Optional
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
                'glow': False,
                'collection_effect': 'simple_explosion'
            },
            FoodType.BONUS: {
                'color': 'gold',
                'animation': 'rotate',
                'particles': True,
                'glow': True,
                'collection_effect': 'golden_burst'
            },
            FoodType.SPEED_UP: {
                'color': 'blue',
                'animation': 'flash',
                'particles': True,
                'glow': True,
                'collection_effect': 'lightning_burst'
            },
            FoodType.SPEED_DOWN: {
                'color': 'purple',
                'animation': 'slow_pulse',
                'particles': False,
                'glow': False,
                'collection_effect': 'slow_motion'
            },
            FoodType.DOUBLE_POINTS: {
                'color': 'green',
                'animation': 'bounce',
                'particles': True,
                'glow': True,
                'collection_effect': 'multiplier_burst'
            },
            FoodType.INVINCIBILITY: {
                'color': 'white',
                'animation': 'sparkle',
                'particles': True,
                'glow': True,
                'collection_effect': 'invincibility_shield'
            }
        }
        
        # Particle system
        self.particles = []
        self.particle_lifetime = 2.0  # seconds
        
        # Collection animation
        self.collection_animations = []
        
        # Enhanced visual effects
        self.enable_particles = True
        self.enable_glow = True
        self.enable_collection_effects = True
        self.enable_food_animations = True
    
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
        
        # Get food properties
        properties = self.food_effects.get(food_type, self.food_effects[FoodType.NORMAL])
        color = properties['color']
        animation = properties['animation']
        
        # Calculate center position
        rect = self.display.get_grid_rect(position.x, position.y)
        center = rect.center
        
        # Apply animation effects
        if self.enable_food_animations:
            center = self._apply_food_animation(center, animation, food_type)
        
        # Draw food based on type
        if food_type == FoodType.NORMAL:
            self._render_normal_food(center, color)
        elif food_type == FoodType.BONUS:
            self._render_bonus_food(center, color)
        elif food_type == FoodType.SPEED_UP:
            self._render_speed_up_food(center, color)
        elif food_type == FoodType.SPEED_DOWN:
            self._render_speed_down_food(center, color)
        elif food_type == FoodType.DOUBLE_POINTS:
            self._render_double_points_food(center, color)
        elif food_type == FoodType.INVINCIBILITY:
            self._render_invincibility_food(center, color)
        else:
            self._render_normal_food(center, color)
        
        # Add glow effect if enabled
        if self.enable_glow and properties['glow']:
            self._add_food_glow(center, color, food_type)
        
        # Add particles if enabled
        if self.enable_particles and properties['particles']:
            self._add_food_particles(center, food_type)
    
    def _apply_food_animation(self, center: Tuple[int, int], animation: str, food_type: FoodType) -> Tuple[int, int]:
        """Apply animation effects to food position."""
        x, y = center
        
        if animation == 'pulse':
            # Simple pulse effect
            pulse_factor = (math.sin(self.animation_timer * 8) + 1) / 2
            scale = 0.8 + 0.2 * pulse_factor
            return center
        
        elif animation == 'rotate':
            # Rotation effect
            angle = self.animation_timer * 4
            radius = 3
            offset_x = math.cos(angle) * radius
            offset_y = math.sin(angle) * radius
            return (int(x + offset_x), int(y + offset_y))
        
        elif animation == 'flash':
            # Flash effect
            flash_factor = (math.sin(self.animation_timer * 12) + 1) / 2
            if flash_factor > 0.7:
                return center
            else:
                return center
        
        elif animation == 'slow_pulse':
            # Slow pulse effect
            pulse_factor = (math.sin(self.animation_timer * 3) + 1) / 2
            scale = 0.7 + 0.3 * pulse_factor
            return center
        
        elif animation == 'bounce':
            # Bounce effect
            bounce_factor = abs(math.sin(self.animation_timer * 6))
            offset_y = int(bounce_factor * 4)
            return (x, y - offset_y)
        
        elif animation == 'sparkle':
            # Sparkle effect
            sparkle_factor = (math.sin(self.animation_timer * 10) + 1) / 2
            if sparkle_factor > 0.8:
                return center
            else:
                return center
        
        return center
    
    def _render_normal_food(self, center: Tuple[int, int], color: str) -> None:
        """Render normal food item."""
        radius = max(3, self.cell_size // 6)
        self.display.draw_circle(center, radius, color)
    
    def _render_bonus_food(self, center: Tuple[int, int], color: str) -> None:
        """Render bonus food with star shape."""
        size = self.cell_size // 4
        points = []
        
        # Create star points
        for i in range(10):
            angle = i * 36 * math.pi / 180
            if i % 2 == 0:
                radius = size
            else:
                radius = size // 2
            
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))
        
        # Draw star
        if len(points) >= 3:
            self.display.draw_polygon(points, color)
    
    def _render_speed_up_food(self, center: Tuple[int, int], color: str) -> None:
        """Render speed up food with lightning bolt."""
        size = self.cell_size // 4
        points = [
            (center[0], center[1] - size),
            (center[0] - size//2, center[1] - size//4),
            (center[0] + size//2, center[1] + size//4),
            (center[0], center[1] + size)
        ]
        
        self.display.draw_polygon(points, color)
    
    def _render_speed_down_food(self, center: Tuple[int, int], color: str) -> None:
        """Render speed down food with snail symbol."""
        size = self.cell_size // 4
        
        # Draw snail shell (spiral)
        self.display.draw_circle(center, size, color)
        self.display.draw_circle(center, size//2, self.display.get_color('black'))
    
    def _render_double_points_food(self, center: Tuple[int, int], color: str) -> None:
        """Render double points food with 2x symbol."""
        text = "2×"
        self.display.draw_text(text, center, self.display.large_font, color, True)
    
    def _render_invincibility_food(self, center: Tuple[int, int], color: str) -> None:
        """Render invincibility food with shield symbol."""
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
    
    def _add_food_glow(self, center: Tuple[int, int], color: str, food_type: FoodType) -> None:
        """Add a glow effect around the food."""
        if not self.enable_glow:
            return
        
        # Create glow surface
        glow_size = self.cell_size // 2
        glow_rect = pygame.Rect(center[0] - glow_size, center[1] - glow_size, 
                               glow_size * 2, glow_size * 2)
        glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        
        # Add multiple glow layers
        for i in range(3):
            alpha = 60 - i * 20
            if alpha > 0:
                glow_color = self.display.get_color(color)
                glow_color = (*glow_color, alpha)
                pygame.draw.circle(glow_surface, glow_color, 
                                 (glow_size, glow_size), glow_size - i * 2)
        
        self.display.screen.blit(glow_surface, glow_rect)
    
    def _add_food_particles(self, center: Tuple[int, int], food_type: FoodType) -> None:
        """Add particles around the food."""
        if not self.enable_particles:
            return
        
        # Create particles based on food type
        particle_count = 3
        for _ in range(particle_count):
            # Random position around food
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(5, 15)
            x = center[0] + math.cos(angle) * distance
            y = center[1] + math.sin(angle) * distance
            
            # Random velocity
            vx = random.uniform(-20, 20)
            vy = random.uniform(-20, 20)
            
            # Random life
            life = random.uniform(0.5, 1.5)
            
            # Color based on food type
            if food_type == FoodType.BONUS:
                color = (255, 215, 0)  # Gold
            elif food_type == FoodType.SPEED_UP:
                color = (0, 0, 255)    # Blue
            elif food_type == FoodType.DOUBLE_POINTS:
                color = (0, 255, 0)    # Green
            elif food_type == FoodType.INVINCIBILITY:
                color = (255, 255, 255)  # White
            else:
                color = (255, 255, 0)    # Yellow
            
            # Create particle
            particle = {
                'x': x, 'y': y, 'vx': vx, 'vy': vy,
                'life': life, 'max_life': life,
                'color': color, 'size': random.uniform(1, 3)
            }
            self.particles.append(particle)
    
    def _update_particles(self, delta_time: float) -> None:
        """Update particle positions and life."""
        alive_particles = []
        
        for particle in self.particles:
            # Update position
            particle['x'] += particle['vx'] * delta_time
            particle['y'] += particle['vy'] * delta_time
            
            # Update life
            particle['life'] -= delta_time
            
            # Keep alive particles
            if particle['life'] > 0:
                alive_particles.append(particle)
        
        self.particles = alive_particles
    
    def _render_particles(self) -> None:
        """Render all particles."""
        for particle in self.particles:
            if particle['life'] > 0:
                # Calculate alpha based on remaining life
                alpha = int(255 * (particle['life'] / particle['max_life']))
                
                # Create particle surface with alpha
                size = int(particle['size'] * 2)
                particle_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, (*particle['color'], alpha), 
                                 (size//2, size//2), int(particle['size']))
                
                # Draw particle
                self.display.screen.blit(particle_surface, 
                                       (int(particle['x'] - particle['size']), 
                                        int(particle['y'] - particle['size'])))
    
    def create_collection_effect(self, food: Food, position: Tuple[int, int]) -> None:
        """Create a collection effect when food is eaten."""
        if not self.enable_collection_effects:
            return
        
        food_type = food.get_effect_type()
        properties = self.food_effects.get(food_type, self.food_effects[FoodType.NORMAL])
        effect_type = properties['collection_effect']
        
        # Create collection animation
        animation = {
            'type': effect_type,
            'position': position,
            'elapsed': 0.0,
            'duration': 1.0,
            'particles': []
        }
        
        # Add effect-specific particles
        if effect_type == 'golden_burst':
            self._add_golden_burst_particles(animation)
        elif effect_type == 'lightning_burst':
            self._add_lightning_burst_particles(animation)
        elif effect_type == 'multiplier_burst':
            self._add_multiplier_burst_particles(animation)
        elif effect_type == 'invincibility_shield':
            self._add_invincibility_shield_particles(animation)
        else:
            self._add_simple_explosion_particles(animation)
        
        self.collection_animations.append(animation)
    
    def _add_golden_burst_particles(self, animation: Dict) -> None:
        """Add golden burst particles."""
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            particle = {
                'x': animation['position'][0], 'y': animation['position'][1],
                'vx': vx, 'vy': vy, 'life': 1.0, 'max_life': 1.0,
                'color': (255, 215, 0), 'size': random.uniform(2, 5)
            }
            animation['particles'].append(particle)
    
    def _add_lightning_burst_particles(self, animation: Dict) -> None:
        """Add lightning burst particles."""
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 200)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            particle = {
                'x': animation['position'][0], 'y': animation['position'][1],
                'vx': vx, 'vy': vy, 'life': 0.8, 'max_life': 0.8,
                'color': (0, 255, 255), 'size': random.uniform(1, 4)
            }
            animation['particles'].append(particle)
    
    def _add_multiplier_burst_particles(self, animation: Dict) -> None:
        """Add multiplier burst particles."""
        for _ in range(25):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(60, 180)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            particle = {
                'x': animation['position'][0], 'y': animation['position'][1],
                'vx': vx, 'vy': vy, 'life': 1.2, 'max_life': 1.2,
                'color': (0, 255, 0), 'size': random.uniform(2, 6)
            }
            animation['particles'].append(particle)
    
    def _add_invincibility_shield_particles(self, animation: Dict) -> None:
        """Add invincibility shield particles."""
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(40, 120)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            particle = {
                'x': animation['position'][0], 'y': animation['position'][1],
                'vx': vx, 'vy': vy, 'life': 1.5, 'max_life': 1.5,
                'color': (255, 255, 255), 'size': random.uniform(1, 3)
            }
            animation['particles'].append(particle)
    
    def _add_simple_explosion_particles(self, animation: Dict) -> None:
        """Add simple explosion particles."""
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(30, 100)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            particle = {
                'x': animation['position'][0], 'y': animation['position'][1],
                'vx': vx, 'vy': vy, 'life': 0.8, 'max_life': 0.8,
                'color': (255, 255, 0), 'size': random.uniform(1, 3)
            }
            animation['particles'].append(particle)
    
    def _update_collection_animations(self, delta_time: float) -> None:
        """Update collection animations."""
        alive_animations = []
        
        for animation in self.collection_animations:
            animation['elapsed'] += delta_time
            
            if animation['elapsed'] < animation['duration']:
                # Update particles
                alive_particles = []
                for particle in animation['particles']:
                    particle['x'] += particle['vx'] * delta_time
                    particle['y'] += particle['vy'] * delta_time
                    particle['life'] -= delta_time
                    
                    if particle['life'] > 0:
                        alive_particles.append(particle)
                
                animation['particles'] = alive_particles
                alive_animations.append(animation)
        
        self.collection_animations = alive_animations
    
    def _render_collection_animations(self) -> None:
        """Render collection animations."""
        for animation in self.collection_animations:
            for particle in animation['particles']:
                if particle['life'] > 0:
                    # Calculate alpha based on remaining life
                    alpha = int(255 * (particle['life'] / particle['max_life']))
                    
                    # Create particle surface with alpha
                    size = int(particle['size'] * 2)
                    particle_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, (*particle['color'], alpha), 
                                     (size//2, size//2), int(particle['size']))
                    
                    # Draw particle
                    self.display.screen.blit(particle_surface, 
                                           (int(particle['x'] - particle['size']), 
                                            int(particle['y'] - particle['size'])))
    
    def set_effects_enabled(self, particles: bool = None, glow: bool = None, 
                           collection_effects: bool = None, animations: bool = None) -> None:
        """Enable or disable visual effects."""
        if particles is not None:
            self.enable_particles = particles
        if glow is not None:
            self.enable_glow = glow
        if collection_effects is not None:
            self.enable_collection_effects = collection_effects
        if animations is not None:
            self.enable_food_animations = animations
    
    def clear_all_effects(self) -> None:
        """Clear all particles and animations."""
        self.particles.clear()
        self.collection_animations.clear()
