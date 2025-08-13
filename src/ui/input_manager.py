"""
Input Manager for Snake Game

Handles keyboard input, input buffering, and control mapping.
Provides responsive and intuitive controls for the game.
"""

import pygame
from typing import Dict, List, Optional, Callable, Set
from enum import Enum
from dataclasses import dataclass
from collections import deque
import time


class InputAction(Enum):
    """Available input actions for the game."""
    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    PAUSE = "pause"
    RESUME = "resume"
    RESTART = "restart"
    QUIT = "quit"
    MENU = "menu"
    CONFIRM = "confirm"
    CANCEL = "cancel"


class ControlScheme(Enum):
    """Available control schemes."""
    ARROW_KEYS = "arrow_keys"
    WASD = "wasd"
    GAMEPAD = "gamepad"


@dataclass
class KeyBinding:
    """Represents a key binding for an input action."""
    primary_key: int
    secondary_key: Optional[int] = None
    description: str = ""
    is_modifier: bool = False


class InputManager:
    """
    Manages all input handling for the Snake game.
    
    Features:
    - Multiple control schemes (Arrow keys, WASD)
    - Input buffering for smooth movement
    - Prevent reverse direction movement
    - Responsive and lag-free input
    - Configurable key bindings
    """
    
    def __init__(self, display_manager=None):
        """Initialize the input manager."""
        self.display_manager = display_manager
        self.control_scheme = ControlScheme.ARROW_KEYS
        
        # Input state
        self.keys_pressed: Set[int] = set()
        self.keys_just_pressed: Set[int] = set()
        self.keys_just_released: Set[int] = set()
        
        # Input buffering
        self.input_buffer: deque = deque(maxlen=3)  # Buffer last 3 inputs
        self.buffer_timeout = 0.1  # seconds
        self.last_input_time = 0
        
        # Movement restrictions
        self.last_movement_direction = None
        self.prevented_directions: Set[InputAction] = set()
        
        # Key bindings for different control schemes
        self.key_bindings = self._setup_key_bindings()
        
        # Input callbacks
        self.input_callbacks: Dict[InputAction, List[Callable]] = {}
        
        # Input processing state
        self.input_enabled = True
        self.movement_enabled = True
        
    def _setup_key_bindings(self) -> Dict[InputAction, KeyBinding]:
        """Set up key bindings for all control schemes."""
        bindings = {
            InputAction.MOVE_UP: KeyBinding(
                primary_key=pygame.K_UP,
                secondary_key=pygame.K_w,
                description="Move snake up"
            ),
            InputAction.MOVE_DOWN: KeyBinding(
                primary_key=pygame.K_DOWN,
                secondary_key=pygame.K_s,
                description="Move snake down"
            ),
            InputAction.MOVE_LEFT: KeyBinding(
                primary_key=pygame.K_LEFT,
                secondary_key=pygame.K_a,
                description="Move snake left"
            ),
            InputAction.MOVE_RIGHT: KeyBinding(
                primary_key=pygame.K_RIGHT,
                secondary_key=pygame.K_d,
                description="Move snake right"
            ),
            InputAction.PAUSE: KeyBinding(
                primary_key=pygame.K_p,
                secondary_key=pygame.K_SPACE,
                description="Pause game"
            ),
            InputAction.RESUME: KeyBinding(
                primary_key=pygame.K_p,
                secondary_key=pygame.K_SPACE,
                description="Resume game"
            ),
            InputAction.RESTART: KeyBinding(
                primary_key=pygame.K_r,
                description="Restart game"
            ),
            InputAction.QUIT: KeyBinding(
                primary_key=pygame.K_q,
                secondary_key=pygame.K_ESCAPE,
                description="Quit game"
            ),
            InputAction.MENU: KeyBinding(
                primary_key=pygame.K_ESCAPE,
                secondary_key=pygame.K_m,
                description="Open menu"
            ),
            InputAction.CONFIRM: KeyBinding(
                primary_key=pygame.K_RETURN,
                secondary_key=pygame.K_SPACE,
                description="Confirm selection"
            ),
            InputAction.CANCEL: KeyBinding(
                primary_key=pygame.K_ESCAPE,
                secondary_key=pygame.K_BACKSPACE,
                description="Cancel selection"
            )
        }
        return bindings
    
    def set_control_scheme(self, scheme: ControlScheme):
        """Change the active control scheme."""
        self.control_scheme = scheme
        self._update_key_bindings_for_scheme()
    
    def _update_key_bindings_for_scheme(self):
        """Update key bindings based on the selected control scheme."""
        if self.control_scheme == ControlScheme.WASD:
            # Make WASD primary for movement
            self.key_bindings[InputAction.MOVE_UP].primary_key = pygame.K_w
            self.key_bindings[InputAction.MOVE_DOWN].primary_key = pygame.K_s
            self.key_bindings[InputAction.MOVE_LEFT].primary_key = pygame.K_a
            self.key_bindings[InputAction.MOVE_RIGHT].primary_key = pygame.K_d
            
            # Make arrow keys secondary
            self.key_bindings[InputAction.MOVE_UP].secondary_key = pygame.K_UP
            self.key_bindings[InputAction.MOVE_DOWN].secondary_key = pygame.K_DOWN
            self.key_bindings[InputAction.MOVE_LEFT].secondary_key = pygame.K_LEFT
            self.key_bindings[InputAction.MOVE_RIGHT].secondary_key = pygame.K_RIGHT
        else:
            # Default: Arrow keys primary, WASD secondary
            self.key_bindings[InputAction.MOVE_UP].primary_key = pygame.K_UP
            self.key_bindings[InputAction.MOVE_DOWN].primary_key = pygame.K_DOWN
            self.key_bindings[InputAction.MOVE_LEFT].primary_key = pygame.K_LEFT
            self.key_bindings[InputAction.MOVE_RIGHT].primary_key = pygame.K_RIGHT
            
            self.key_bindings[InputAction.MOVE_UP].secondary_key = pygame.K_w
            self.key_bindings[InputAction.MOVE_DOWN].secondary_key = pygame.K_s
            self.key_bindings[InputAction.MOVE_LEFT].secondary_key = pygame.K_a
            self.key_bindings[InputAction.MOVE_RIGHT].secondary_key = pygame.K_d
    
    def register_callback(self, action: InputAction, callback: Callable):
        """Register a callback function for a specific input action."""
        if action not in self.input_callbacks:
            self.input_callbacks[action] = []
        self.input_callbacks[action].append(callback)
    
    def unregister_callback(self, action: InputAction, callback: Callable):
        """Unregister a callback function for a specific input action."""
        if action in self.input_callbacks and callback in self.input_callbacks[action]:
            self.input_callbacks[action].remove(callback)
    
    def handle_event(self, event: pygame.event.Event):
        """Handle a single pygame event."""
        if not self.input_enabled:
            return
        
        if event.type == pygame.KEYDOWN:
            self._handle_key_down(event.key)
        elif event.type == pygame.KEYUP:
            self._handle_key_up(event.key)
    
    def _handle_key_down(self, key: int):
        """Handle a key press event."""
        if key not in self.keys_pressed:
            self.keys_pressed.add(key)
            self.keys_just_pressed.add(key)
            
            # Find the action for this key
            action = self._get_action_for_key(key)
            if action:
                self._process_input_action(action, key)
    
    def _handle_key_up(self, key: int):
        """Handle a key release event."""
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
            self.keys_just_released.add(key)
    
    def _get_action_for_key(self, key: int) -> Optional[InputAction]:
        """Get the input action for a given key."""
        for action, binding in self.key_bindings.items():
            if key == binding.primary_key or key == binding.secondary_key:
                return action
        return None
    
    def _process_input_action(self, action: InputAction, key: int):
        """Process an input action and trigger callbacks."""
        current_time = time.time()
        
        # Handle movement actions with buffering and direction prevention
        if action in [InputAction.MOVE_UP, InputAction.MOVE_DOWN, InputAction.MOVE_LEFT, InputAction.MOVE_RIGHT]:
            if not self.movement_enabled:
                return
            
            # Check if this direction is prevented (180° turn)
            if self._is_direction_prevented(action):
                return
            
            # Add to input buffer
            self._add_to_input_buffer(action, current_time)
            
            # Update prevented directions for next frame
            self._update_prevented_directions(action)
        
        # Trigger callbacks
        if action in self.input_callbacks:
            for callback in self.input_callbacks[action]:
                try:
                    callback(action, key)
                except Exception as e:
                    print(f"Error in input callback for {action}: {e}")
    
    def _is_direction_prevented(self, action: InputAction) -> bool:
        """Check if a movement direction is prevented (180° turn)."""
        if not self.last_movement_direction:
            return False
        
        # Define opposite directions
        opposites = {
            InputAction.MOVE_UP: InputAction.MOVE_DOWN,
            InputAction.MOVE_DOWN: InputAction.MOVE_UP,
            InputAction.MOVE_LEFT: InputAction.MOVE_RIGHT,
            InputAction.MOVE_RIGHT: InputAction.MOVE_LEFT
        }
        
        return opposites.get(action) == self.last_movement_direction
    
    def _add_to_input_buffer(self, action: InputAction, timestamp: float):
        """Add an input action to the buffer."""
        self.input_buffer.append((action, timestamp))
        self.last_input_time = timestamp
    
    def _update_prevented_directions(self, current_direction: InputAction):
        """Update the list of prevented directions for the next frame."""
        opposites = {
            InputAction.MOVE_UP: InputAction.MOVE_DOWN,
            InputAction.MOVE_DOWN: InputAction.MOVE_UP,
            InputAction.MOVE_LEFT: InputAction.MOVE_RIGHT,
            InputAction.MOVE_RIGHT: InputAction.MOVE_LEFT
        }
        
        self.prevented_directions.clear()
        if current_direction in opposites:
            self.prevented_directions.add(opposites[current_direction])
    
    def get_buffered_input(self) -> Optional[InputAction]:
        """Get the next buffered input action."""
        current_time = time.time()
        
        # Remove expired inputs from buffer
        while self.input_buffer and (current_time - self.input_buffer[0][1]) > self.buffer_timeout:
            self.input_buffer.popleft()
        
        if self.input_buffer:
            action, _ = self.input_buffer.popleft()
            return action
        
        return None
    
    def set_movement_direction(self, direction: InputAction):
        """Set the current movement direction (used by game logic)."""
        self.last_movement_direction = direction
    
    def clear_input_buffer(self):
        """Clear the input buffer."""
        self.input_buffer.clear()
    
    def reset_input_state(self):
        """Reset all input state."""
        self.keys_pressed.clear()
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
        self.clear_input_buffer()
        self.last_movement_direction = None
        self.prevented_directions.clear()
    
    def is_key_pressed(self, key: int) -> bool:
        """Check if a specific key is currently pressed."""
        return key in self.keys_pressed
    
    def is_key_just_pressed(self, key: int) -> bool:
        """Check if a specific key was just pressed this frame."""
        return key in self.keys_just_pressed
    
    def is_key_just_released(self, key: int) -> bool:
        """Check if a specific key was just released this frame."""
        return key in self.keys_just_released
    
    def get_pressed_keys(self) -> Set[int]:
        """Get all currently pressed keys."""
        return self.keys_pressed.copy()
    
    def update(self):
        """Update the input manager state (call once per frame)."""
        # Clear just-pressed and just-released flags
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
        
        # Clear expired inputs from buffer
        current_time = time.time()
        while self.input_buffer and (current_time - self.input_buffer[0][1]) > self.buffer_timeout:
            self.input_buffer.popleft()
    
    def enable_input(self):
        """Enable input processing."""
        self.input_enabled = True
    
    def disable_input(self):
        """Disable input processing."""
        self.input_enabled = False
    
    def enable_movement(self):
        """Enable movement input."""
        self.movement_enabled = True
    
    def disable_movement(self):
        """Disable movement input."""
        self.movement_enabled = False
    
    def get_control_scheme(self) -> ControlScheme:
        """Get the current control scheme."""
        return self.control_scheme
    
    def get_key_bindings(self) -> Dict[InputAction, KeyBinding]:
        """Get the current key bindings."""
        return self.key_bindings.copy()
    
    def get_available_control_schemes(self) -> List[ControlScheme]:
        """Get all available control schemes."""
        return list(ControlScheme)
    
    def is_input_enabled(self) -> bool:
        """Check if input processing is enabled."""
        return self.input_enabled
    
    def is_movement_enabled(self) -> bool:
        """Check if movement input is enabled."""
        return self.movement_enabled
    
    def get_input_stats(self) -> Dict:
        """Get input statistics for debugging."""
        return {
            "keys_pressed": len(self.keys_pressed),
            "input_buffer_size": len(self.input_buffer),
            "control_scheme": self.control_scheme.value,
            "input_enabled": self.input_enabled,
            "movement_enabled": self.movement_enabled,
            "last_movement_direction": self.last_movement_direction.value if self.last_movement_direction else None,
            "prevented_directions": [d.value for d in self.prevented_directions]
        }
