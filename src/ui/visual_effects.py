"""
Visual Effects and Animations

This module handles all visual effects and animations in the game:
- Particle effects for food collection
- Snake movement animations
- Screen transition effects
- Visual feedback for power-ups
- Score popup animations
- Background visual effects
- Game over screen animations
"""

import pygame
import random
import math
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class EffectType(Enum):
    """Types of visual effects."""
    PARTICLE_EXPLOSION = "particle_explosion"
    SCORE_POPUP = "score_popup"
    POWER_UP_ACTIVATION = "power_up_activation"
    SCREEN_TRANSITION = "screen_transition"
    BACKGROUND_EFFECT = "background_effect"
    GAME_OVER_ANIMATION = "game_over_animation"


class AnimationState(Enum):
    """Animation states."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    STOPPED = "stopped"


@dataclass
class Particle:
    """Represents a single particle in a particle system."""
    x: float
    y: float
    vx: float
    vy: float
    life: float
    max_life: float
    color: Tuple[int, int, int]
    size: float
    alpha: int = 255
    
    def update(self, dt: float) -> bool:
        """
        Update particle position and life.
        
        Args:
            dt: Delta time in seconds
            
        Returns:
            True if particle is still alive, False if dead
        """
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        
        # Fade out as particle ages
        if self.life > 0:
            self.alpha = int(255 * (self.life / self.max_life))
            return True
        return False
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the particle on the given surface."""
        if self.alpha > 0:
            # Create a surface with alpha for the particle
            particle_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*self.color, self.alpha), 
                             (int(self.size), int(self.size)), int(self.size))
            surface.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))


@dataclass
class Animation:
    """Base class for animations."""
    effect_type: EffectType
    state: AnimationState
    duration: float
    elapsed: float
    position: Tuple[float, float]
    
    def update(self, dt: float) -> bool:
        """
        Update animation state.
        
        Args:
            dt: Delta time in seconds
            
        Returns:
            True if animation is still active, False if completed
        """
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.state = AnimationState.COMPLETED
            return False
        return True
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the animation. Override in subclasses."""
        pass


class ParticleSystem(Animation):
    """Manages a collection of particles for effects like explosions."""
    
    def __init__(self, effect_type: EffectType, position: Tuple[float, float], 
                 particle_count: int = 20, duration: float = 1.0):
        super().__init__(effect_type, AnimationState.ACTIVE, duration, 0.0, position)
        self.particles: List[Particle] = []
        self.particle_count = particle_count
        self._create_particles()
    
    def _create_particles(self) -> None:
        """Create initial particles for the effect."""
        for _ in range(self.particle_count):
            # Random velocity in all directions
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # Random life span
            life = random.uniform(0.5, 1.5)
            
            # Random size
            size = random.uniform(2, 6)
            
            # Color based on effect type
            if self.effect_type == EffectType.PARTICLE_EXPLOSION:
                color = random.choice([
                    (255, 255, 0),   # Yellow
                    (255, 165, 0),   # Orange
                    (255, 69, 0),    # Red-orange
                    (255, 215, 0)    # Gold
                ])
            elif self.effect_type == EffectType.POWER_UP_ACTIVATION:
                color = random.choice([
                    (0, 255, 255),   # Cyan
                    (255, 0, 255),   # Magenta
                    (255, 255, 0),   # Yellow
                    (0, 255, 0)      # Green
                ])
            else:
                color = (255, 255, 255)  # White
            
            particle = Particle(
                x=self.position[0],
                y=self.position[1],
                vx=vx,
                vy=vy,
                life=life,
                max_life=life,
                color=color,
                size=size
            )
            self.particles.append(particle)
    
    def update(self, dt: float) -> bool:
        """Update all particles in the system."""
        if not super().update(dt):
            return False
        
        # Update particles
        alive_particles = []
        for particle in self.particles:
            if particle.update(dt):
                alive_particles.append(particle)
        
        self.particles = alive_particles
        
        # Check if all particles are dead
        if not self.particles:
            self.state = AnimationState.COMPLETED
            return False
        
        return True
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw all particles in the system."""
        for particle in self.particles:
            particle.draw(surface)


class ScorePopup(Animation):
    """Animated score popup that appears when food is collected."""
    
    def __init__(self, position: Tuple[float, float], score: int, 
                 duration: float = 1.0):
        super().__init__(EffectType.SCORE_POPUP, AnimationState.ACTIVE, duration, 0.0, position)
        self.score = score
        self.initial_y = position[1]
        self.font = pygame.font.Font(None, 24)
        self.color = (255, 255, 0)  # Yellow
    
    def update(self, dt: float) -> bool:
        """Update score popup position and alpha."""
        if not super().update(dt):
            return False
        
        # Move upward
        progress = self.elapsed / self.duration
        self.position = (self.position[0], self.initial_y - progress * 50)
        
        return True
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the score popup."""
        if self.elapsed < self.duration:
            # Calculate alpha based on remaining time
            alpha = int(255 * (1 - self.elapsed / self.duration))
            
            # Create text surface with alpha
            text_surface = self.font.render(f"+{self.score}", True, self.color)
            text_surface.set_alpha(alpha)
            
            # Draw text
            text_rect = text_surface.get_rect(center=self.position)
            surface.blit(text_surface, text_rect)


class ScreenTransition(Animation):
    """Handles screen transitions and fades."""
    
    def __init__(self, effect_type: EffectType, duration: float = 0.5):
        super().__init__(effect_type, AnimationState.ACTIVE, duration, 0.0, (0, 0))
        self.transition_surface = None
        self.transition_type = effect_type
    
    def update(self, dt: float) -> bool:
        """Update transition animation."""
        return super().update(dt)
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the screen transition effect."""
        if self.transition_surface is None:
            self.transition_surface = pygame.Surface(surface.get_size())
            self.transition_surface.fill((0, 0, 0))
        
        if self.transition_type == EffectType.SCREEN_TRANSITION:
            # Fade effect
            progress = self.elapsed / self.duration
            if progress <= 0.5:
                # Fade to black
                alpha = int(255 * (progress * 2))
                self.transition_surface.set_alpha(alpha)
                surface.blit(self.transition_surface, (0, 0))
            else:
                # Fade from black
                alpha = int(255 * ((1 - progress) * 2))
                self.transition_surface.set_alpha(alpha)
                surface.blit(self.transition_surface, (0, 0))


class BackgroundEffect(Animation):
    """Creates subtle background visual effects."""
    
    def __init__(self, effect_type: EffectType, duration: float = 2.0):
        super().__init__(effect_type, AnimationState.ACTIVE, duration, 0.0, (0, 0))
        self.particles: List[Particle] = []
        self._create_background_particles()
    
    def _create_background_particles(self) -> None:
        """Create subtle background particles."""
        for _ in range(15):
            x = random.uniform(0, 800)  # Assuming 800x600 window
            y = random.uniform(0, 600)
            vx = random.uniform(-10, 10)
            vy = random.uniform(-10, 10)
            life = random.uniform(2.0, 4.0)
            size = random.uniform(1, 3)
            color = (100, 100, 100)  # Subtle gray
            
            particle = Particle(x, y, vx, vy, life, life, color, size)
            self.particles.append(particle)
    
    def update(self, dt: float) -> bool:
        """Update background particles."""
        if not super().update(dt):
            return False
        
        # Update particles
        alive_particles = []
        for particle in self.particles:
            if particle.update(dt):
                alive_particles.append(particle)
        
        self.particles = alive_particles
        
        # Replenish particles if needed
        while len(self.particles) < 15:
            self._create_background_particles()
        
        return True
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw background particles."""
        for particle in self.particles:
            particle.draw(surface)


class VisualEffectsManager:
    """Manages all visual effects and animations in the game."""
    
    def __init__(self):
        """Initialize the visual effects manager."""
        self.active_effects: List[Animation] = []
        self.effect_templates: Dict[EffectType, Dict[str, Any]] = {
            EffectType.PARTICLE_EXPLOSION: {
                'particle_count': 25,
                'duration': 1.2,
                'colors': [(255, 255, 0), (255, 165, 0), (255, 69, 0)]
            },
            EffectType.POWER_UP_ACTIVATION: {
                'particle_count': 30,
                'duration': 1.5,
                'colors': [(0, 255, 255), (255, 0, 255), (255, 255, 0)]
            },
            EffectType.SCORE_POPUP: {
                'duration': 1.0,
                'color': (255, 255, 0)
            }
        }
    
    def create_food_collection_effect(self, position: Tuple[float, float]) -> None:
        """Create a particle explosion effect when food is collected."""
        effect = ParticleSystem(
            EffectType.PARTICLE_EXPLOSION,
            position,
            particle_count=25,
            duration=1.2
        )
        self.active_effects.append(effect)
    
    def create_power_up_effect(self, position: Tuple[float, float]) -> None:
        """Create a power-up activation effect."""
        effect = ParticleSystem(
            EffectType.POWER_UP_ACTIVATION,
            position,
            particle_count=30,
            duration=1.5
        )
        self.active_effects.append(effect)
    
    def create_score_popup(self, position: Tuple[float, float], score: int) -> None:
        """Create a score popup animation."""
        effect = ScorePopup(position, score, duration=1.0)
        self.active_effects.append(effect)
    
    def create_screen_transition(self, effect_type: EffectType = EffectType.SCREEN_TRANSITION) -> None:
        """Create a screen transition effect."""
        effect = ScreenTransition(effect_type, duration=0.5)
        self.active_effects.append(effect)
    
    def create_background_effect(self) -> None:
        """Create a subtle background effect."""
        effect = BackgroundEffect(EffectType.BACKGROUND_EFFECT, duration=2.0)
        self.active_effects.append(effect)
    
    def update(self, dt: float) -> None:
        """Update all active effects."""
        # Update effects
        active_effects = []
        for effect in self.active_effects:
            if effect.update(dt):
                active_effects.append(effect)
        
        self.active_effects = active_effects
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw all active effects."""
        for effect in self.active_effects:
            effect.draw(surface)
    
    def clear_all_effects(self) -> None:
        """Clear all active effects."""
        self.active_effects.clear()
    
    def get_active_effect_count(self) -> int:
        """Get the number of currently active effects."""
        return len(self.active_effects)
    
    def pause_effects(self) -> None:
        """Pause all active effects."""
        for effect in self.active_effects:
            if effect.state == AnimationState.ACTIVE:
                effect.state = AnimationState.PAUSED
    
    def resume_effects(self) -> None:
        """Resume all paused effects."""
        for effect in self.active_effects:
            if effect.state == AnimationState.PAUSED:
                effect.state = AnimationState.ACTIVE
