"""
Power-ups System

This module implements a comprehensive power-ups system that provides:
- Multiple power-up types with different effects
- Duration and cooldown management
- Visual and audio feedback integration
- Strategic gameplay enhancement
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import time
from .grid import Position


class PowerUpType(Enum):
    """Enumeration of power-up types."""
    SPEED_BOOST = "speed_boost"
    INVINCIBILITY = "invincibility"
    SCORE_MULTIPLIER = "score_multiplier"
    GROWTH_BOOST = "growth_boost"
    SHIELD = "shield"
    DOUBLE_POINTS = "double_points"
    SLOW_MOTION = "slow_motion"
    MAGNET = "magnet"


class PowerUpState(Enum):
    """Enumeration of power-up states."""
    INACTIVE = "inactive"
    ACTIVE = "active"
    COOLDOWN = "cooldown"
    EXPIRED = "expired"


@dataclass
class PowerUpEffect:
    """Represents a power-up effect with its properties."""
    power_up_type: PowerUpType
    duration: float  # Duration in seconds
    magnitude: float  # Effect strength (e.g., speed multiplier)
    cooldown: float  # Cooldown period in seconds
    description: str  # Human-readable description
    icon: str  # Visual icon/symbol
    color: str  # Visual color
    sound_effect: str  # Audio effect name


@dataclass
class ActivePowerUp:
    """Represents an active power-up effect."""
    power_up_type: PowerUpType
    effect: PowerUpEffect
    start_time: float
    end_time: float
    state: PowerUpState = PowerUpState.ACTIVE
    remaining_duration: float = 0.0
    cooldown_end_time: float = 0.0
    
    def __post_init__(self):
        """Calculate remaining duration and cooldown end time."""
        self.remaining_duration = self.effect.duration
        self.cooldown_end_time = self.end_time + self.effect.cooldown
    
    def update(self, current_time: float) -> bool:
        """
        Update the power-up state based on current time.
        
        Args:
            current_time: Current game time in seconds
            
        Returns:
            True if power-up is still active, False if expired
        """
        if self.state == PowerUpState.ACTIVE:
            if current_time >= self.end_time:
                self.state = PowerUpState.EXPIRED
                return False
            else:
                self.remaining_duration = self.end_time - current_time
                return True
        elif self.state == PowerUpState.EXPIRED:
            if current_time >= self.cooldown_end_time:
                self.state = PowerUpState.INACTIVE
                return False
            else:
                self.state = PowerUpState.COOLDOWN
                return False
        
        return False
    
    def is_active(self) -> bool:
        """Check if the power-up is currently active."""
        return self.state == PowerUpState.ACTIVE
    
    def is_in_cooldown(self) -> bool:
        """Check if the power-up is in cooldown."""
        return self.state == PowerUpState.COOLDOWN
    
    def get_remaining_duration(self) -> float:
        """Get remaining duration in seconds."""
        return max(0.0, self.remaining_duration)
    
    def get_cooldown_remaining(self) -> float:
        """Get remaining cooldown time in seconds."""
        if self.state == PowerUpState.COOLDOWN:
            return max(0.0, self.cooldown_end_time - time.time())
        return 0.0


class PowerUpsManager:
    """
    Manages all power-ups in the game.
    
    Handles:
    - Power-up activation and deactivation
    - Duration and cooldown management
    - Effect stacking and conflicts
    - Visual and audio feedback
    """
    
    def __init__(self):
        """Initialize the power-ups manager."""
        # Define all available power-up effects
        self.power_up_effects = {
            PowerUpType.SPEED_BOOST: PowerUpEffect(
                power_up_type=PowerUpType.SPEED_BOOST,
                duration=8.0,
                magnitude=1.5,  # 1.5x speed
                cooldown=15.0,
                description="Speed Boost - Move 50% faster",
                icon="⚡",
                color="blue",
                sound_effect="speed_boost"
            ),
            PowerUpType.INVINCIBILITY: PowerUpEffect(
                power_up_type=PowerUpType.INVINCIBILITY,
                duration=6.0,
                magnitude=1.0,  # Binary effect
                cooldown=20.0,
                description="Invincibility - Immune to collisions",
                icon="🛡️",
                color="white",
                sound_effect="invincibility"
            ),
            PowerUpType.SCORE_MULTIPLIER: PowerUpEffect(
                power_up_type=PowerUpType.SCORE_MULTIPLIER,
                duration=10.0,
                magnitude=2.0,  # 2x score
                cooldown=25.0,
                description="Score Multiplier - Double points",
                icon="2×",
                color="green",
                sound_effect="score_multiplier"
            ),
            PowerUpType.GROWTH_BOOST: PowerUpEffect(
                power_up_type=PowerUpType.GROWTH_BOOST,
                duration=0.0,  # Instant effect
                magnitude=3.0,  # Grow by 3 segments
                cooldown=30.0,
                description="Growth Boost - Instant growth",
                icon="🌱",
                color="lime",
                sound_effect="growth_boost"
            ),
            PowerUpType.SHIELD: PowerUpEffect(
                power_up_type=PowerUpType.SHIELD,
                duration=5.0,
                magnitude=1.0,  # Binary effect
                cooldown=18.0,
                description="Shield - Protection from one collision",
                icon="🛡️",
                color="cyan",
                sound_effect="shield"
            ),
            PowerUpType.DOUBLE_POINTS: PowerUpEffect(
                power_up_type=PowerUpType.DOUBLE_POINTS,
                duration=12.0,
                magnitude=2.0,  # 2x points
                cooldown=30.0,
                description="Double Points - Score twice as much",
                icon="2×",
                color="gold",
                sound_effect="double_points"
            ),
            PowerUpType.SLOW_MOTION: PowerUpEffect(
                power_up_type=PowerUpType.SLOW_MOTION,
                duration=7.0,
                magnitude=0.5,  # 0.5x speed
                cooldown=20.0,
                description="Slow Motion - Time slows down",
                icon="🐌",
                color="purple",
                sound_effect="slow_motion"
            ),
            PowerUpType.MAGNET: PowerUpEffect(
                power_up_type=PowerUpType.MAGNET,
                duration=9.0,
                magnitude=1.0,  # Binary effect
                cooldown=22.0,
                description="Magnet - Attract nearby food",
                icon="🧲",
                color="orange",
                sound_effect="magnet"
            )
        }
        
        # Active power-ups
        self.active_power_ups: Dict[PowerUpType, ActivePowerUp] = {}
        
        # Power-up history for statistics
        self.power_up_history: List[ActivePowerUp] = []
        
        # Current game time
        self.current_time = 0.0
        
        # Effect multipliers (accumulated from active power-ups)
        self.effect_multipliers = {
            'speed': 1.0,
            'score': 1.0,
            'growth': 1.0
        }
        
        # Game mode configuration support
        self.spawn_frequency_multiplier = 1.0
    
    def activate_power_up(self, power_up_type: PowerUpType, current_time: float) -> bool:
        """
        Activate a power-up effect.
        
        Args:
            power_up_type: Type of power-up to activate
            current_time: Current game time
            
        Returns:
            True if power-up was activated, False if in cooldown
        """
        # Check if power-up is available
        if power_up_type in self.active_power_ups:
            active_power_up = self.active_power_ups[power_up_type]
            if active_power_up.state == PowerUpState.COOLDOWN:
                return False  # Still in cooldown
        
        # Get power-up effect
        if power_up_type not in self.power_up_effects:
            return False
        
        effect = self.power_up_effects[power_up_type]
        
        # Create new active power-up
        active_power_up = ActivePowerUp(
            power_up_type=power_up_type,
            effect=effect,
            start_time=current_time,
            end_time=current_time + effect.duration
        )
        
        # Add to active power-ups
        self.active_power_ups[power_up_type] = active_power_up
        
        # Add to history
        self.power_up_history.append(active_power_up)
        
        # Update effect multipliers
        self._update_effect_multipliers()
        
        return True
    
    def deactivate_power_up(self, power_up_type: PowerUpType) -> bool:
        """
        Deactivate a power-up effect.
        
        Args:
            power_up_type: Type of power-up to deactivate
            
        Returns:
            True if power-up was deactivated, False if not active
        """
        if power_up_type in self.active_power_ups:
            power_up = self.active_power_ups[power_up_type]
            if power_up.state == PowerUpState.ACTIVE:
                power_up.state = PowerUpState.EXPIRED
                self._update_effect_multipliers()
                return True
        return False
    
    def update(self, delta_time: float) -> None:
        """
        Update all active power-ups.
        
        Args:
            delta_time: Time elapsed since last update
        """
        self.current_time += delta_time
        
        # Update all active power-ups
        expired_power_ups = []
        
        for power_up_type, power_up in self.active_power_ups.items():
            if not power_up.update(self.current_time):
                expired_power_ups.append(power_up_type)
        
        # Remove expired power-ups
        for power_up_type in expired_power_ups:
            del self.active_power_ups[power_up_type]
        
        # Update effect multipliers
        self._update_effect_multipliers()
    
    def _update_effect_multipliers(self) -> None:
        """Update accumulated effect multipliers from active power-ups."""
        # Reset multipliers
        self.effect_multipliers = {
            'speed': 1.0,
            'score': 1.0,
            'growth': 1.0
        }
        
        # Calculate accumulated effects
        for power_up in self.active_power_ups.values():
            if power_up.is_active():
                if power_up.power_up_type == PowerUpType.SPEED_BOOST:
                    self.effect_multipliers['speed'] *= power_up.effect.magnitude
                elif power_up.power_up_type == PowerUpType.SCORE_MULTIPLIER:
                    self.effect_multipliers['score'] *= power_up.effect.magnitude
                elif power_up.power_up_type == PowerUpType.DOUBLE_POINTS:
                    self.effect_multipliers['score'] *= power_up.effect.magnitude
                elif power_up.power_up_type == PowerUpType.SLOW_MOTION:
                    self.effect_multipliers['speed'] *= power_up.effect.magnitude
    
    def get_speed_multiplier(self) -> float:
        """Get the current speed multiplier."""
        return self.effect_multipliers['speed']
    
    def get_score_multiplier(self) -> float:
        """Get the current score multiplier."""
        return self.effect_multipliers['score']
    
    def get_growth_multiplier(self) -> float:
        """Get the current growth multiplier."""
        return self.effect_multipliers['growth']
    
    def has_power_up(self, power_up_type: PowerUpType) -> bool:
        """Check if a specific power-up is currently active."""
        return (power_up_type in self.active_power_ups and 
                self.active_power_ups[power_up_type].is_active())
    
    def is_invincible(self) -> bool:
        """Check if the snake is currently invincible."""
        return (self.has_power_up(PowerUpType.INVINCIBILITY) or 
                self.has_power_up(PowerUpType.SHIELD))
    
    def has_magnet_effect(self) -> bool:
        """Check if the magnet effect is active."""
        return self.has_power_up(PowerUpType.MAGNET)
    
    def get_active_power_ups(self) -> List[ActivePowerUp]:
        """Get list of currently active power-ups."""
        return [power_up for power_up in self.active_power_ups.values() 
                if power_up.is_active()]
    
    def get_power_up_status(self, power_up_type: PowerUpType) -> Optional[PowerUpState]:
        """Get the current status of a specific power-up."""
        if power_up_type in self.active_power_ups:
            return self.active_power_ups[power_up_type].state
        return PowerUpState.INACTIVE
    
    def get_power_up_remaining_time(self, power_up_type: PowerUpType) -> float:
        """Get remaining time for a specific power-up."""
        if power_up_type in self.active_power_ups:
            power_up = self.active_power_ups[power_up_type]
            if power_up.is_active():
                return power_up.get_remaining_duration()
            elif power_up.is_in_cooldown():
                return power_up.get_cooldown_remaining()
        return 0.0
    
    def get_all_power_up_effects(self) -> Dict[PowerUpType, PowerUpEffect]:
        """Get all available power-up effects."""
        return self.power_up_effects.copy()
    
    def get_power_up_statistics(self) -> Dict[str, Any]:
        """Get statistics about power-up usage."""
        total_activated = len(self.power_up_history)
        currently_active = len(self.get_active_power_ups())
        
        # Count by type
        type_counts = {}
        for power_up in self.power_up_history:
            power_up_type = power_up.power_up_type.value
            type_counts[power_up_type] = type_counts.get(power_up_type, 0) + 1
        
        return {
            "total_activated": total_activated,
            "currently_active": currently_active,
            "type_counts": type_counts,
            "effect_multipliers": self.effect_multipliers.copy()
        }
    
    def clear_all_power_ups(self) -> None:
        """Clear all active power-ups (useful for game reset)."""
        self.active_power_ups.clear()
        self.power_up_history.clear()
        self._update_effect_multipliers()
    
    def get_visual_indicators(self) -> List[Dict[str, Any]]:
        """Get visual indicators for active power-ups."""
        indicators = []
        
        for power_up in self.get_active_power_ups():
            indicators.append({
                'type': power_up.power_up_type.value,
                'icon': power_up.effect.icon,
                'color': power_up.effect.color,
                'remaining_time': power_up.get_remaining_duration(),
                'description': power_up.effect.description
            })
        
        return indicators
    
    def set_spawn_frequency_multiplier(self, multiplier: float) -> None:
        """Set the spawn frequency multiplier for game mode configuration."""
        self.spawn_frequency_multiplier = max(0.1, min(multiplier, 5.0))  # Clamp between 0.1x and 5x
