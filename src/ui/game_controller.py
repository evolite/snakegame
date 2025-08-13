"""
Game Controller for Snake Game

Integrates input handling with game logic to provide responsive controls.
Manages game state transitions and input processing for smooth gameplay.
"""

from typing import Optional, Callable
from ..game.game_logic import GameLogic
from ..game.grid import Direction
from .input_manager import InputManager, InputAction, ControlScheme


class GameController:
    """
    Controls the game by integrating input handling with game logic.
    
    Features:
    - Seamless input integration
    - Game state management
    - Smooth movement controls
    - Pause/resume functionality
    - Game restart controls
    - Input buffering for responsive gameplay
    """
    
    def __init__(self, game_logic: GameLogic, input_manager: InputManager):
        """Initialize the game controller."""
        self.game_logic = game_logic
        self.input_manager = input_manager
        
        # Game control state
        self.game_running = False
        self.input_processing_enabled = True
        
        # Movement control
        self.movement_delay = 0.15  # seconds between movement updates
        self.last_movement_time = 0.0
        
        # Setup input callbacks
        self._setup_input_callbacks()
        
        # Input buffering for smooth movement
        self.pending_movement = None
        self.movement_buffer_timeout = 0.1  # seconds
        
    def _setup_input_callbacks(self):
        """Set up callback functions for input actions."""
        # Movement controls
        self.input_manager.register_callback(InputAction.MOVE_UP, self._handle_move_up)
        self.input_manager.register_callback(InputAction.MOVE_DOWN, self._handle_move_down)
        self.input_manager.register_callback(InputAction.MOVE_LEFT, self._handle_move_left)
        self.input_manager.register_callback(InputAction.MOVE_RIGHT, self._handle_move_right)
        
        # Game control
        self.input_manager.register_callback(InputAction.PAUSE, self._handle_pause)
        self.input_manager.register_callback(InputAction.RESUME, self._handle_resume)
        self.input_manager.register_callback(InputAction.RESTART, self._handle_restart)
        self.input_manager.register_callback(InputAction.QUIT, self._handle_quit)
        
        # Menu controls
        self.input_manager.register_callback(InputAction.MENU, self._handle_menu)
        self.input_manager.register_callback(InputAction.CONFIRM, self._handle_confirm)
        self.input_manager.register_callback(InputAction.CANCEL, self._handle_cancel)
    
    def start_game(self):
        """Start the game and enable input processing."""
        self.game_running = True
        self.input_manager.enable_input()
        self.input_manager.enable_movement()
        self.game_logic.restart_game()
    
    def stop_game(self):
        """Stop the game and disable input processing."""
        self.game_running = False
        self.input_manager.disable_input()
        self.input_manager.disable_movement()
    
    def pause_game(self):
        """Pause the game."""
        if self.game_logic.is_game_active() and not self.game_logic.is_game_paused():
            self.game_logic.pause_game()
            self.input_manager.disable_movement()
    
    def resume_game(self):
        """Resume the game."""
        if self.game_logic.is_game_paused():
            self.game_logic.resume_game()
            self.input_manager.enable_movement()
    
    def restart_game(self):
        """Restart the game."""
        self.game_logic.restart_game()
        self.input_manager.reset_input_state()
        self.input_manager.enable_movement()
        self.pending_movement = None
        self.last_movement_time = 0.0
    
    def update(self, delta_time: float):
        """Update the game controller (call once per frame)."""
        if not self.game_running:
            return
        
        # Update input manager
        self.input_manager.update()
        
        # Process buffered movement input
        self._process_movement_input(delta_time)
        
        # Update game logic
        self.game_logic.update(delta_time)
        
        # Update movement direction in input manager
        self._update_movement_direction()
    
    def _process_movement_input(self, delta_time: float):
        """Process movement input with timing and buffering."""
        if not self.game_logic.is_game_active() or self.game_logic.is_game_paused():
            return
        
        current_time = self.game_logic.get_game_time()
        
        # Check if it's time for movement update
        if current_time - self.last_movement_time >= self.movement_delay:
            # Get buffered input
            buffered_input = self.input_manager.get_buffered_input()
            
            if buffered_input:
                # Process the buffered movement
                self._execute_movement(buffered_input)
                self.last_movement_time = current_time
                self.pending_movement = None
            elif self.pending_movement:
                # Execute pending movement if no new input
                self._execute_movement(self.pending_movement)
                self.last_movement_time = current_time
                self.pending_movement = None
    
    def _execute_movement(self, movement_action: InputAction):
        """Execute a movement action."""
        if not self.game_logic.is_game_active():
            return
        
        # Convert input action to direction
        direction = self._input_action_to_direction(movement_action)
        if direction:
            # Check if the movement is valid
            if self._is_movement_valid(direction):
                self.game_logic.change_snake_direction(direction)
                # Update the input manager's movement direction
                self.input_manager.set_movement_direction(movement_action)
    
    def _input_action_to_direction(self, action: InputAction) -> Optional[Direction]:
        """Convert input action to grid direction."""
        direction_map = {
            InputAction.MOVE_UP: Direction.UP,
            InputAction.MOVE_DOWN: Direction.DOWN,
            InputAction.MOVE_LEFT: Direction.LEFT,
            InputAction.MOVE_RIGHT: Direction.RIGHT
        }
        return direction_map.get(action)
    
    def _is_movement_valid(self, direction: Direction) -> bool:
        """Check if a movement direction is valid for the snake."""
        # Get current snake direction
        snake_body = self.game_logic.get_snake_body()
        if not snake_body or len(snake_body) < 2:
            return True
        
        # Get current direction from snake body
        head = snake_body[0]
        neck = snake_body[1]
        
        # Calculate current direction
        current_direction = None
        if head.x > neck.x:
            current_direction = Direction.RIGHT
        elif head.x < neck.x:
            current_direction = Direction.LEFT
        elif head.y > neck.y:
            current_direction = Direction.DOWN
        elif head.y < neck.y:
            current_direction = Direction.UP
        
        # Prevent 180° turns
        if current_direction:
            opposite_directions = {
                Direction.UP: Direction.DOWN,
                Direction.DOWN: Direction.UP,
                Direction.LEFT: Direction.RIGHT,
                Direction.RIGHT: Direction.LEFT
            }
            if direction == opposite_directions.get(current_direction):
                return False
        
        return True
    
    def _update_movement_direction(self):
        """Update the input manager with current movement direction."""
        if not self.game_logic.is_game_active():
            return
        
        snake_body = self.game_logic.get_snake_body()
        if len(snake_body) < 2:
            return
        
        # Calculate current direction from snake body
        head = snake_body[0]
        neck = snake_body[1]
        
        if head.x > neck.x:
            self.input_manager.set_movement_direction(InputAction.MOVE_RIGHT)
        elif head.x < neck.x:
            self.input_manager.set_movement_direction(InputAction.MOVE_LEFT)
        elif head.y > neck.y:
            self.input_manager.set_movement_direction(InputAction.MOVE_DOWN)
        elif head.y < neck.y:
            self.input_manager.set_movement_direction(InputAction.MOVE_UP)
    
    def _handle_move_up(self, action: InputAction, key: int):
        """Handle move up input."""
        if self.game_logic.is_game_active() and not self.game_logic.is_game_paused():
            self.pending_movement = InputAction.MOVE_UP
    
    def _handle_move_down(self, action: InputAction, key: int):
        """Handle move down input."""
        if self.game_logic.is_game_active() and not self.game_logic.is_game_paused():
            self.pending_movement = InputAction.MOVE_DOWN
    
    def _handle_move_left(self, action: InputAction, key: int):
        """Handle move left input."""
        if self.game_logic.is_game_active() and not self.game_logic.is_game_paused():
            self.pending_movement = InputAction.MOVE_LEFT
    
    def _handle_move_right(self, action: InputAction, key: int):
        """Handle move right input."""
        if self.game_logic.is_game_active() and not self.game_logic.is_game_paused():
            self.pending_movement = InputAction.MOVE_RIGHT
    
    def _handle_pause(self, action: InputAction, key: int):
        """Handle pause input."""
        if self.game_logic.is_game_active() and not self.game_logic.is_game_paused():
            self.pause_game()
    
    def _handle_resume(self, action: InputAction, key: int):
        """Handle resume input."""
        if self.game_logic.is_game_paused():
            self.resume_game()
    
    def _handle_restart(self, action: InputAction, key: int):
        """Handle restart input."""
        self.restart_game()
    
    def _handle_quit(self, action: InputAction, key: int):
        """Handle quit input."""
        self.stop_game()
        # This would typically trigger a quit event in the main game loop
    
    def _handle_menu(self, action: InputAction, key: int):
        """Handle menu input."""
        if self.game_logic.is_game_active():
            self.pause_game()
        # This would typically open a menu system
    
    def _handle_confirm(self, action: InputAction, key: int):
        """Handle confirm input."""
        # This would typically confirm menu selections
        pass
    
    def _handle_cancel(self, action: InputAction, key: int):
        """Handle cancel input."""
        if self.game_logic.is_game_paused():
            self.resume_game()
        # This would typically cancel menu selections
    
    def set_control_scheme(self, scheme: ControlScheme):
        """Change the control scheme."""
        self.input_manager.set_control_scheme(scheme)
    
    def get_control_scheme(self) -> ControlScheme:
        """Get the current control scheme."""
        return self.input_manager.get_control_scheme()
    
    def set_movement_delay(self, delay: float):
        """Set the movement delay between updates."""
        self.movement_delay = max(0.05, delay)
    
    def get_movement_delay(self) -> float:
        """Get the current movement delay."""
        return self.movement_delay
    
    def enable_input_processing(self):
        """Enable input processing."""
        self.input_processing_enabled = True
        self.input_manager.enable_input()
    
    def disable_input_processing(self):
        """Disable input processing."""
        self.input_processing_enabled = False
        self.input_manager.disable_input()
    
    def is_input_processing_enabled(self) -> bool:
        """Check if input processing is enabled."""
        return self.input_processing_enabled
    
    def get_game_status(self):
        """Get the current game status."""
        return self.game_logic.get_game_status()
    
    def get_game_stats(self):
        """Get current game statistics."""
        return self.game_logic.get_game_stats()
    
    def get_input_stats(self):
        """Get input statistics for debugging."""
        return self.input_manager.get_input_stats()
    
    def reset_controller(self):
        """Reset the controller state."""
        self.input_manager.reset_input_state()
        self.pending_movement = None
        self.last_movement_time = 0.0
        self.game_running = False
        self.input_processing_enabled = True
    
    def handle_event(self, event):
        """Handle a pygame event."""
        if self.input_processing_enabled:
            self.input_manager.handle_event(event)
    
    def get_available_control_schemes(self):
        """Get all available control schemes."""
        return self.input_manager.get_available_control_schemes()
    
    def get_key_bindings(self):
        """Get current key bindings."""
        return self.input_manager.get_key_bindings()
