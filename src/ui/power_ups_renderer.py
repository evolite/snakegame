"""
Power-ups Renderer

This module provides specialized rendering for power-ups with:
- Active power-up indicators
- Duration and cooldown visualization
- Visual effects and animations
- Status bar integration
"""

import pygame
import math
from typing import List, Dict, Any, Tuple
from ..game.power_ups import PowerUpsManager, PowerUpType, PowerUpState
from .display import DisplayManager


class PowerUpsRenderer:
    """
    Specialized renderer for power-ups visualization.
    
    Provides visual feedback for active power-ups, durations, and cooldowns.
    """
    
    def __init__(self, display_manager: DisplayManager):
        """Initialize the power-ups renderer."""
        self.display = display_manager
        self.cell_size = display_manager.get_cell_size()
        
        # Power-up visual settings
        self.indicator_size = 32
        self.status_bar_height = 20
        self.icon_size = 24
        self.spacing = 8
        
        # Animation properties
        self.animation_timer = 0.0
        self.animation_speed = 2.0  # seconds per cycle
        
        # Visual effects
        self.enable_glow = True
        self.enable_animations = True
        self.enable_pulse = True
        
        # Color schemes for different power-up states
        self.state_colors = {
            PowerUpState.ACTIVE: 'green',
            PowerUpState.COOLDOWN: 'red',
            PowerUpState.INACTIVE: 'gray',
            PowerUpState.EXPIRED: 'orange'
        }
    
    def render_power_ups_hud(self, power_ups_manager: PowerUpsManager, 
                            surface: pygame.Surface, position: Tuple[int, int]) -> None:
        """
        Render the power-ups HUD at the specified position.
        
        Args:
            power_ups_manager: The power-ups manager
            surface: Surface to render on
            position: Position to render the HUD
        """
        x, y = position
        
        # Get active power-ups
        active_power_ups = power_ups_manager.get_active_power_ups()
        
        if not active_power_ups:
            return
        
        # Render power-ups container
        container_width = len(active_power_ups) * (self.indicator_size + self.spacing) - self.spacing
        container_height = self.indicator_size + self.status_bar_height + 10
        
        # Draw container background
        container_rect = pygame.Rect(x, y, container_width, container_height)
        pygame.draw.rect(surface, self.display.get_color('dark_gray'), container_rect)
        pygame.draw.rect(surface, self.display.get_color('white'), container_rect, 2)
        
        # Render each active power-up
        for i, power_up in enumerate(active_power_ups):
            power_up_x = x + i * (self.indicator_size + self.spacing)
            power_up_y = y + 5
            
            self._render_power_up_indicator(
                power_up, surface, (power_up_x, power_up_y)
            )
    
    def _render_power_up_indicator(self, power_up: Any, surface: pygame.Surface, 
                                 position: Tuple[int, int]) -> None:
        """
        Render a single power-up indicator.
        
        Args:
            power_up: The power-up to render
            surface: Surface to render on
            position: Position to render the indicator
        """
        x, y = position
        
        # Get power-up properties
        icon = power_up.effect.icon
        color = power_up.effect.color
        remaining_time = power_up.get_remaining_duration()
        total_duration = power_up.effect.duration
        
        # Calculate animation factors
        if self.enable_animations:
            self.animation_timer += 0.016  # Assuming 60 FPS
            if self.animation_timer > self.animation_speed:
                self.animation_timer = 0.0
        
        # Draw power-up icon background
        icon_rect = pygame.Rect(x, y, self.indicator_size, self.indicator_size)
        
        # Add glow effect if enabled
        if self.enable_glow:
            self._add_power_up_glow(surface, icon_rect, color)
        
        # Draw icon background
        pygame.draw.rect(surface, self.display.get_color('black'), icon_rect)
        pygame.draw.rect(surface, self.display.get_color(color), icon_rect, 3)
        
        # Draw icon
        self._render_power_up_icon(surface, icon, icon_rect, color)
        
        # Draw duration bar
        self._render_duration_bar(surface, (x, y + self.indicator_size), 
                                remaining_time, total_duration, color)
        
        # Add pulse effect for active power-ups
        if self.enable_pulse and power_up.is_active():
            self._add_pulse_effect(surface, icon_rect, color)
    
    def _render_power_up_icon(self, surface: pygame.Surface, icon: str, 
                             rect: pygame.Rect, color: str) -> None:
        """
        Render the power-up icon.
        
        Args:
            surface: Surface to render on
            icon: Icon symbol to render
            rect: Rectangle to render in
            color: Color for the icon
        """
        # For emoji icons, we'll use a simple representation
        # In a full implementation, you might use custom sprites
        
        if icon == "⚡":
            self._render_lightning_icon(surface, rect, color)
        elif icon == "🛡️":
            self._render_shield_icon(surface, rect, color)
        elif icon == "2×":
            self._render_multiplier_icon(surface, rect, color)
        elif icon == "🌱":
            self._render_growth_icon(surface, rect, color)
        elif icon == "🐌":
            self._render_slow_icon(surface, rect, color)
        elif icon == "🧲":
            self._render_magnet_icon(surface, rect, color)
        else:
            # Default icon rendering
            self._render_default_icon(surface, rect, icon, color)
    
    def _render_lightning_icon(self, surface: pygame.Surface, rect: pygame.Rect, color: str) -> None:
        """Render a lightning bolt icon."""
        center = rect.center
        size = min(rect.width, rect.height) // 3
        
        # Lightning bolt points
        points = [
            (center[0], center[1] - size),
            (center[0] - size//2, center[1] - size//4),
            (center[0] + size//2, center[1] + size//4),
            (center[0], center[1] + size)
        ]
        
        pygame.draw.polygon(surface, self.display.get_color(color), points)
    
    def _render_shield_icon(self, surface: pygame.Surface, rect: pygame.Rect, color: str) -> None:
        """Render a shield icon."""
        center = rect.center
        size = min(rect.width, rect.height) // 3
        
        # Shield points
        points = [
            (center[0], center[1] - size),
            (center[0] - size, center[1] - size//2),
            (center[0] - size, center[1] + size//2),
            (center[0], center[1] + size),
            (center[0] + size, center[1] + size//2),
            (center[0] + size, center[1] - size//2)
        ]
        
        pygame.draw.polygon(surface, self.display.get_color(color), points)
    
    def _render_multiplier_icon(self, surface: pygame.Surface, rect: pygame.Rect, color: str) -> None:
        """Render a 2x multiplier icon."""
        center = rect.center
        
        # Draw "2×" text
        font = pygame.font.Font(None, 20)
        text_surface = font.render("2×", True, self.display.get_color(color))
        text_rect = text_surface.get_rect(center=center)
        surface.blit(text_surface, text_rect)
    
    def _render_growth_icon(self, surface: pygame.Surface, rect: pygame.Rect, color: str) -> None:
        """Render a growth icon."""
        center = rect.center
        size = min(rect.width, rect.height) // 4
        
        # Draw multiple circles representing growth
        for i in range(3):
            circle_size = size - i * 2
            if circle_size > 0:
                pygame.draw.circle(surface, self.display.get_color(color), 
                                 center, circle_size)
    
    def _render_slow_icon(self, surface: pygame.Surface, rect: pygame.Rect, color: str) -> None:
        """Render a slow motion icon."""
        center = rect.center
        size = min(rect.width, rect.height) // 4
        
        # Draw spiral representing slow motion
        pygame.draw.circle(surface, self.display.get_color(color), center, size)
        pygame.draw.circle(surface, self.display.get_color('black'), center, size//2)
    
    def _render_magnet_icon(self, surface: pygame.Surface, rect: pygame.Rect, color: str) -> None:
        """Render a magnet icon."""
        center = rect.center
        size = min(rect.width, rect.height) // 4
        
        # Draw magnet poles
        left_pole = (center[0] - size, center[1])
        right_pole = (center[0] + size, center[1])
        
        pygame.draw.circle(surface, self.display.get_color(color), left_pole, size//2)
        pygame.draw.circle(surface, self.display.get_color(color), right_pole, size//2)
        
        # Draw connecting line
        pygame.draw.line(surface, self.display.get_color(color), left_pole, right_pole, 3)
    
    def _render_default_icon(self, surface: pygame.Surface, rect: pygame.Rect, 
                            icon: str, color: str) -> None:
        """Render a default icon (fallback)."""
        center = rect.center
        size = min(rect.width, rect.height) // 3
        
        # Draw a simple circle with the icon
        pygame.draw.circle(surface, self.display.get_color(color), center, size)
        
        # Try to render text if it's a simple character
        if len(icon) == 1:
            font = pygame.font.Font(None, 16)
            text_surface = font.render(icon, True, self.display.get_color('black'))
            text_rect = text_surface.get_rect(center=center)
            surface.blit(text_surface, text_rect)
    
    def _render_duration_bar(self, surface: pygame.Surface, position: Tuple[int, int], 
                           remaining_time: float, total_duration: float, color: str) -> None:
        """
        Render a duration bar showing remaining time.
        
        Args:
            surface: Surface to render on
            position: Position to render the bar
            remaining_time: Remaining time in seconds
            total_duration: Total duration in seconds
            color: Color for the bar
        """
        x, y = position
        
        # Calculate progress
        if total_duration > 0:
            progress = remaining_time / total_duration
        else:
            progress = 1.0  # Instant power-ups
        
        # Draw background bar
        bar_rect = pygame.Rect(x, y, self.indicator_size, self.status_bar_height)
        pygame.draw.rect(surface, self.display.get_color('dark_gray'), bar_rect)
        pygame.draw.rect(surface, self.display.get_color('white'), bar_rect, 1)
        
        # Draw progress bar
        if progress > 0:
            progress_width = int(self.indicator_size * progress)
            progress_rect = pygame.Rect(x, y, progress_width, self.status_bar_height)
            pygame.draw.rect(surface, self.display.get_color(color), progress_rect)
        
        # Draw time text
        time_text = f"{remaining_time:.1f}s"
        font = pygame.font.Font(None, 14)
        text_surface = font.render(time_text, True, self.display.get_color('white'))
        text_rect = text_surface.get_rect(center=bar_rect.center)
        surface.blit(text_surface, text_rect)
    
    def _add_power_up_glow(self, surface: pygame.Surface, rect: pygame.Rect, color: str) -> None:
        """Add a glow effect around the power-up indicator."""
        if not self.enable_glow:
            return
        
        # Create a larger rectangle for the glow
        glow_rect = rect.inflate(8, 8)
        glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        
        # Draw multiple layers for glow effect
        for i in range(3):
            alpha = 60 - i * 20
            if alpha > 0:
                glow_color = self.display.get_color(color)
                glow_color = (*glow_color, alpha)
                pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), border_radius=4)
        
        surface.blit(glow_surface, glow_rect)
    
    def _add_pulse_effect(self, surface: pygame.Surface, rect: pygame.Rect, color: str) -> None:
        """Add a pulse effect for active power-ups."""
        if not self.enable_pulse:
            return
        
        # Calculate pulse factor
        pulse_factor = (math.sin(self.animation_timer * 8) + 1) / 2
        pulse_alpha = int(100 * pulse_factor)
        
        if pulse_alpha > 0:
            # Create pulse surface
            pulse_rect = rect.inflate(4, 4)
            pulse_surface = pygame.Surface(pulse_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(pulse_surface, (*self.display.get_color(color), pulse_alpha), 
                           pulse_surface.get_rect(), border_radius=4)
            surface.blit(pulse_surface, pulse_rect)
    
    def render_power_ups_status(self, power_ups_manager: PowerUpsManager, 
                              surface: pygame.Surface, position: Tuple[int, int]) -> None:
        """
        Render a comprehensive power-ups status display.
        
        Args:
            power_ups_manager: The power-ups manager
            surface: Surface to render on
            position: Position to render the status
        """
        x, y = position
        
        # Get all power-up effects
        all_effects = power_ups_manager.get_all_power_up_effects()
        
        # Calculate layout
        effects_per_row = 4
        rows = (len(all_effects) + effects_per_row - 1) // effects_per_row
        
        # Draw container
        container_width = effects_per_row * (self.indicator_size + self.spacing) - self.spacing
        container_height = rows * (self.indicator_size + self.status_bar_height + 10) - 10
        
        container_rect = pygame.Rect(x, y, container_width, container_height)
        pygame.draw.rect(surface, self.display.get_color('navy'), container_rect)
        pygame.draw.rect(surface, self.display.get_color('white'), container_rect, 2)
        
        # Render title
        title_font = pygame.font.Font(None, 24)
        title_surface = title_font.render("Power-ups Status", True, self.display.get_color('white'))
        title_rect = title_surface.get_rect(centerx=container_rect.centerx, top=y-30)
        surface.blit(title_surface, title_rect)
        
        # Render each power-up effect
        for i, (power_up_type, effect) in enumerate(all_effects.items()):
            row = i // effects_per_row
            col = i % effects_per_row
            
            effect_x = x + col * (self.indicator_size + self.spacing)
            effect_y = y + row * (self.indicator_size + self.status_bar_height + 10)
            
            # Check if power-up is active or in cooldown
            status = power_ups_manager.get_power_up_status(power_up_type)
            remaining_time = power_ups_manager.get_power_up_remaining_time(power_up_type)
            
            self._render_power_up_status_indicator(
                effect, status, remaining_time, surface, (effect_x, effect_y)
            )
    
    def _render_power_up_status_indicator(self, effect: Any, status: PowerUpState, 
                                        remaining_time: float, surface: pygame.Surface, 
                                        position: Tuple[int, int]) -> None:
        """
        Render a power-up status indicator.
        
        Args:
            effect: The power-up effect
            status: Current status of the power-up
            remaining_time: Remaining time or cooldown time
            surface: Surface to render on
            position: Position to render the indicator
        """
        x, y = position
        
        # Determine color based on status
        color = self.state_colors.get(status, 'gray')
        
        # Draw indicator background
        indicator_rect = pygame.Rect(x, y, self.indicator_size, self.indicator_size)
        
        # Different background based on status
        if status == PowerUpState.ACTIVE:
            bg_color = 'green'
        elif status == PowerUpState.COOLDOWN:
            bg_color = 'red'
        elif status == PowerUpState.INACTIVE:
            bg_color = 'dark_gray'
        else:
            bg_color = 'orange'
        
        pygame.draw.rect(surface, self.display.get_color(bg_color), indicator_rect)
        pygame.draw.rect(surface, self.display.get_color(color), indicator_rect, 2)
        
        # Render icon
        self._render_power_up_icon(surface, effect.icon, indicator_rect, color)
        
        # Render status bar
        if status == PowerUpState.ACTIVE:
            self._render_duration_bar(surface, (x, y + self.indicator_size), 
                                    remaining_time, effect.duration, color)
        elif status == PowerUpState.COOLDOWN:
            self._render_cooldown_bar(surface, (x, y + self.indicator_size), 
                                    remaining_time, effect.cooldown, color)
    
    def _render_cooldown_bar(self, surface: pygame.Surface, position: Tuple[int, int], 
                            remaining_cooldown: float, total_cooldown: float, color: str) -> None:
        """
        Render a cooldown bar.
        
        Args:
            surface: Surface to render on
            position: Position to render the bar
            remaining_cooldown: Remaining cooldown time
            total_cooldown: Total cooldown time
            color: Color for the bar
        """
        x, y = position
        
        # Calculate cooldown progress
        if total_cooldown > 0:
            progress = remaining_cooldown / total_cooldown
        else:
            progress = 0.0
        
        # Draw background bar
        bar_rect = pygame.Rect(x, y, self.indicator_size, self.status_bar_height)
        pygame.draw.rect(surface, self.display.get_color('dark_gray'), bar_rect)
        pygame.draw.rect(surface, self.display.get_color('red'), bar_rect, 1)
        
        # Draw cooldown progress bar
        if progress > 0:
            progress_width = int(self.indicator_size * progress)
            progress_rect = pygame.Rect(x, y, progress_width, self.status_bar_height)
            pygame.draw.rect(surface, self.display.get_color('red'), progress_rect)
        
        # Draw cooldown text
        cooldown_text = f"CD: {remaining_cooldown:.1f}s"
        font = pygame.font.Font(None, 14)
        text_surface = font.render(cooldown_text, True, self.display.get_color('white'))
        text_rect = text_surface.get_rect(center=bar_rect.center)
        surface.blit(text_surface, text_rect)
    
    def set_effects_enabled(self, glow: bool = None, animations: bool = None, 
                           pulse: bool = None) -> None:
        """Enable or disable visual effects."""
        if glow is not None:
            self.enable_glow = glow
        if animations is not None:
            self.enable_animations = animations
        if pulse is not None:
            self.enable_pulse = pulse
