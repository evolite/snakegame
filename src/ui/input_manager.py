"""
Input Manager

This module handles all input processing for the game:
- Keyboard input handling
- Input buffering
- Control mapping
- Input validation
"""

import pygame
from typing import Dict, List, Optional, Callable
from enum import Enum
from ..game.grid import Direction


class InputAction(Enum):
    """Enumeration of possible input actions."""
    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    PAUSE = "pause"
    RESUME = "resume"
    RESTART = "restart"
    QUIT = "quit"
    MENU_UP = "menu_up"
    MENU_DOWN = "menu_down"
    MENU_SELECT = "menu_select"
    MENU_BACK = "menu_back"


class InputManager:
    """
    Manages all input processing for the game.
    
    Handles:
    - Keyboard input detection
    - Input buffering
    - Control mapping
    - Input validation
    - Event processing
    """
    
    def __init__(self):
        """Initialize the input manager."""
        # Control mappings
        self.key_mappings = {
            # Movement controls
            pygame.K_UP: InputAction.MOVE_UP,
            pygame.K_DOWN: InputAction.MOVE_DOWN,
            pygame.K_LEFT: InputAction.MOVE_LEFT,
            pygame.K_RIGHT: InputAction.MOVE_RIGHT,
            pygame.K_w: InputAction.MOVE_UP,
            pygame.K_s: InputAction.MOVE_DOWN,
            pygame.K_a: InputAction.MOVE_LEFT,
            pygame.K_d: InputAction.MOVE_RIGHT,
            
            # Game control
            pygame.K_p: InputAction.PAUSE,
            pygame.K_SPACE: InputAction.PAUSE,
            pygame.K_r: InputAction.RESTART,
            pygame.K_q: InputAction.QUIT,
            pygame.K_ESCAPE: InputAction.QUIT,
            
            # Menu navigation
            pygame.K_RETURN: InputAction.MENU_SELECT,
            pygame.K_BACKSPACE: InputAction.MENU_BACK
        }
        
        # Input buffering
        self.input_buffer: List[InputAction] = []
        self.max_buffer_size = 3
        
        # Input state tracking
        self.pressed_keys: set = set()
        self.just_pressed_keys: set = set()
        self.just_released_keys: set = set()
        
        # Input callbacks
        self.action_callbacks: Dict[InputAction, List[Callable]] = {}
        
        # Input settings
        self.input_enabled = True
        self.buffer_enabled = True
        self.repeat_delay = 0.15  # seconds
        self.repeat_interval = 0.05  # seconds
        
        # Repeat timers
        self.repeat_timers: Dict[int, float] = {}
        self.last_repeat_time: Dict[int, float] = {}
        
        # Initialize callbacks for all actions
        for action in InputAction:
            self.action_callbacks[action] = []
    
    def process_events(self, events: List[pygame.event.Event]) -> None:
        """
        Process Pygame events and update input state.
        
        Args:
            events: List of Pygame events to process
        """
        if not self.input_enabled:
            return
        
        # Reset just pressed/released keys
        self.just_pressed_keys.clear()
        self.just_released_keys.clear()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                self._handle_key_down(event.key)
            elif event.type == pygame.KEYUP:
                self._handle_key_up(event.key)
            elif event.type == pygame.QUIT:
                # Handle window close
                self._trigger_action(InputAction.QUIT)
    
    def _handle_key_down(self, key: int) -> None:
        """Handle key press events."""
        if key not in self.pressed_keys:
            self.pressed_keys.add(key)
            self.just_pressed_keys.add(key)
            
            # Add to input buffer if it's a movement key
            if key in self.key_mappings:
                action = self.key_mappings[key]
                if self._is_movement_action(action):
                    self._add_to_buffer(action)
                
                # Trigger action callback
                self._trigger_action(action)
    
    def _handle_key_up(self, key: int) -> None:
        """Handle key release events."""
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
            self.just_released_keys.add(key)
            
            # Clear repeat timers
            if key in self.repeat_timers:
                del self.repeat_timers[key]
            if key in self.last_repeat_time:
                del self.last_repeat_time[key]
    
    def _is_movement_action(self, action: InputAction) -> bool:
        """Check if an action is a movement action."""
        return action in [
            InputAction.MOVE_UP,
            InputAction.MOVE_DOWN,
            InputAction.MOVE_LEFT,
            InputAction.MOVE_RIGHT
        ]
    
    def _add_to_buffer(self, action: InputAction) -> None:
        """Add an action to the input buffer."""
        if not self.buffer_enabled:
            return
        
        # Remove duplicate consecutive actions
        if self.input_buffer and self.input_buffer[-1] == action:
            return
        
        # Add to buffer
        self.input_buffer.append(action)
        
        # Limit buffer size
        if len(self.input_buffer) > self.max_buffer_size:
            self.input_buffer.pop(0)
    
    def get_buffered_input(self) -> Optional[InputAction]:
        """
        Get the next buffered input action.
        
        Returns:
            The next input action, or None if buffer is empty
        """
        if not self.buffer_enabled or not self.input_buffer:
            return None
        
        return self.input_buffer.pop(0)
    
    def clear_buffer(self) -> None:
        """Clear the input buffer."""
        self.input_buffer.clear()
    
    def is_key_pressed(self, key: int) -> bool:
        """Check if a key is currently pressed."""
        return key in self.pressed_keys
    
    def is_key_just_pressed(self, key: int) -> bool:
        """Check if a key was just pressed this frame."""
        return key in self.just_pressed_keys
    
    def is_key_just_released(self, key: int) -> bool:
        """Check if a key was just released this frame."""
        return key in self.just_released_keys
    
    def is_action_pressed(self, action: InputAction) -> bool:
        """Check if an action is currently active."""
        for key, mapped_action in self.key_mappings.items():
            if mapped_action == action and self.is_key_pressed(key):
                return True
        return False
    
    def is_action_just_pressed(self, action: InputAction) -> bool:
        """Check if an action was just triggered this frame."""
        for key, mapped_action in self.key_mappings.items():
            if mapped_action == action and self.is_key_just_pressed(key):
                return True
        return False
    
    def get_movement_direction(self) -> Optional[Direction]:
        """
        Get the current movement direction from pressed keys.
        
        Returns:
            Direction enum value, or None if no movement keys pressed
        """
        if self.is_action_pressed(InputAction.MOVE_UP):
            return Direction.UP
        elif self.is_action_pressed(InputAction.MOVE_DOWN):
            return Direction.DOWN
        elif self.is_action_pressed(InputAction.MOVE_LEFT):
            return Direction.LEFT
        elif self.is_action_pressed(InputAction.MOVE_RIGHT):
            return Direction.RIGHT
        
        return None
    
    def get_movement_direction_from_buffer(self) -> Optional[Direction]:
        """
        Get movement direction from the input buffer.
        
        Returns:
            Direction enum value, or None if buffer is empty
        """
        if not self.input_buffer:
            return None
        
        # Look for the first movement action in buffer
        for action in self.input_buffer:
            if action == InputAction.MOVE_UP:
                return Direction.UP
            elif action == InputAction.MOVE_DOWN:
                return Direction.DOWN
            elif action == InputAction.MOVE_LEFT:
                return Direction.LEFT
            elif action == InputAction.MOVE_RIGHT:
                return Direction.RIGHT
        
        return None
    
    def add_action_callback(self, action: InputAction, callback: Callable) -> None:
        """Add a callback function for a specific action."""
        if action not in self.action_callbacks:
            self.action_callbacks[action] = []
        
        self.action_callbacks[action].append(callback)
    
    def remove_action_callback(self, action: InputAction, callback: Callable) -> None:
        """Remove a callback function for a specific action."""
        if action in self.action_callbacks and callback in self.action_callbacks[action]:
            self.action_callbacks[action].remove(callback)
    
    def _trigger_action(self, action: InputAction) -> None:
        """Trigger callbacks for a specific action."""
        if action in self.action_callbacks:
            for callback in self.action_callbacks[action]:
                try:
                    callback()
                except Exception as e:
                    print(f"Error in action callback for {action}: {e}")
    
    def update(self, delta_time: float) -> None:
        """Update input manager (called each frame)."""
        if not self.input_enabled:
            return
        
        # Handle key repeat for held keys
        self._update_key_repeat(delta_time)
    
    def _update_key_repeat(self, delta_time: float) -> None:
        """Update key repeat timers."""
        for key in list(self.pressed_keys):
            if key not in self.repeat_timers:
                # Start repeat timer
                self.repeat_timers[key] = 0.0
                self.last_repeat_time[key] = 0.0
                continue
            
            # Update repeat timer
            self.repeat_timers[key] += delta_time
            
            # Check if it's time to repeat
            if self.repeat_timers[key] >= self.repeat_delay:
                repeat_interval = self.repeat_interval
                
                if (self.repeat_timers[key] - self.repeat_delay) >= repeat_interval:
                    # Trigger repeat
                    if key in self.key_mappings:
                        action = self.key_mappings[key]
                        if self._is_movement_action(action):
                            self._add_to_buffer(action)
                        
                        # Update last repeat time
                        self.last_repeat_time[key] = self.repeat_timers[key]
    
    def set_input_enabled(self, enabled: bool) -> None:
        """Enable or disable input processing."""
        self.input_enabled = enabled
        
        if not enabled:
            # Clear all input state
            self.pressed_keys.clear()
            self.just_pressed_keys.clear()
            self.just_released_keys.clear()
            self.clear_buffer()
    
    def set_buffer_enabled(self, enabled: bool) -> None:
        """Enable or disable input buffering."""
        self.buffer_enabled = enabled
        
        if not enabled:
            self.clear_buffer()
    
    def set_repeat_settings(self, delay: float, interval: float) -> None:
        """Set key repeat delay and interval."""
        self.repeat_delay = max(0.0, delay)
        self.repeat_interval = max(0.01, interval)
    
    def get_input_state_summary(self) -> Dict:
        """Get a summary of the current input state."""
        return {
            'pressed_keys': list(self.pressed_keys),
            'just_pressed_keys': list(self.just_pressed_keys),
            'just_released_keys': list(self.just_released_keys),
            'buffer_size': len(self.input_buffer),
            'buffer_contents': [action.value for action in self.input_buffer],
            'input_enabled': self.input_enabled,
            'buffer_enabled': self.buffer_enabled
        }
    
    def reset_input_state(self) -> None:
        """Reset all input state."""
        self.pressed_keys.clear()
        self.just_pressed_keys.clear()
        self.just_released_keys.clear()
        self.clear_buffer()
        self.repeat_timers.clear()
        self.last_repeat_time.clear()
    
    def get_available_actions(self) -> List[InputAction]:
        """Get list of all available input actions."""
        return list(InputAction)
    
    def get_key_for_action(self, action: InputAction) -> Optional[int]:
        """Get the primary key for a specific action."""
        for key, mapped_action in self.key_mappings.items():
            if mapped_action == action:
                return key
        return None
    
    def get_all_keys_for_action(self, action: InputAction) -> List[int]:
        """Get all keys that map to a specific action."""
        keys = []
        for key, mapped_action in self.key_mappings.items():
            if mapped_action == action:
                keys.append(key)
        return keys
    
    def set_key_mapping(self, key: int, action: InputAction) -> None:
        """Set a custom key mapping."""
        self.key_mappings[key] = action
    
    def remove_key_mapping(self, key: int) -> None:
        """Remove a key mapping."""
        if key in self.key_mappings:
            del self.key_mappings[key]
    
    def get_key_mappings(self) -> Dict[int, InputAction]:
        """Get all current key mappings."""
        return self.key_mappings.copy()
    
    def load_key_mappings(self, mappings: Dict[int, InputAction]) -> None:
        """Load key mappings from a dictionary."""
        self.key_mappings.clear()
        self.key_mappings.update(mappings)
    
    def save_key_mappings(self) -> Dict[int, InputAction]:
        """Save current key mappings to a dictionary."""
        return self.key_mappings.copy()
