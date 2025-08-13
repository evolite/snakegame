"""
Menu Manager for Snake Game

Handles all menu-related functionality:
- Start menu with navigation
- Game over screen with options
- Menu state management
- Keyboard navigation and selection
- Smooth transitions between screens
"""

import pygame
from typing import List, Dict, Optional, Callable
from enum import Enum
from dataclasses import dataclass
from .input_manager import InputManager, InputAction


class MenuState(Enum):
    """Available menu states."""
    START_MENU = "start_menu"
    GAME_OVER = "game_over"
    PAUSE_MENU = "pause_menu"
    SETTINGS_MENU = "settings_menu"
    DIFFICULTY_SELECTION = "difficulty_selection"
    HIGH_SCORES = "high_scores"
    GAME_MODE_SELECTION = "game_mode_selection"
    IN_GAME = "in_game"


@dataclass
class MenuOption:
    """Represents a menu option."""
    text: str
    action: str
    enabled: bool = True
    callback: Optional[Callable] = None


class MenuManager:
    """
    Manages all menu functionality for the Snake game.
    
    Features:
    - Start menu with game logo/title
    - Game over screen with score summary
    - Keyboard navigation and selection
    - Smooth transitions between screens
    - Menu state management
    - Background animations and effects
    """
    
    def __init__(self, input_manager: InputManager):
        """Initialize the menu manager."""
        self.input_manager = input_manager
        self.current_state = MenuState.START_MENU
        self.selected_index = 0
        
        # Menu options for different states
        self.menu_options = self._setup_menu_options()
        
        # Menu state and navigation
        self.menu_active = True
        self.transition_timer = 0.0
        self.transition_duration = 0.2  # seconds
        
        # Background animation
        self.background_animation_timer = 0.0
        self.background_animation_speed = 2.0
        
        # Menu callbacks
        self.menu_callbacks: Dict[str, Callable] = {}
        
        # Setup input callbacks
        self._setup_input_callbacks()
        
        # Menu styling
        self.menu_colors = {
            'title': 'white',
            'option_normal': 'white',
            'option_selected': 'yellow',
            'option_disabled': 'gray',
            'background': 'black',
            'overlay': 'navy'
        }
    
    def _setup_menu_options(self) -> Dict[MenuState, List[MenuOption]]:
        """Set up menu options for different states."""
        return {
                    MenuState.START_MENU: [
            MenuOption("New Game", "new_game"),
            MenuOption("Game Mode", "game_mode"),
            MenuOption("High Scores", "high_scores"),
            MenuOption("Settings", "settings"),
            MenuOption("Quit", "quit")
        ],
            MenuState.GAME_OVER: [
                MenuOption("Retry", "retry"),
                MenuOption("Main Menu", "main_menu"),
                MenuOption("Quit", "quit")
            ],
            MenuState.PAUSE_MENU: [
                MenuOption("Resume", "resume"),
                MenuOption("Restart", "restart"),
                MenuOption("Main Menu", "main_menu"),
                MenuOption("Quit", "quit")
            ],
            MenuState.SETTINGS_MENU: [
                MenuOption("Difficulty Level", "difficulty_level"),
                MenuOption("Control Scheme", "control_scheme"),
                MenuOption("Sound Volume", "sound_volume"),
                MenuOption("Back", "back")
            ],
            MenuState.DIFFICULTY_SELECTION: [
                MenuOption("Easy", "difficulty_easy"),
                MenuOption("Medium", "difficulty_medium"),
                MenuOption("Hard", "difficulty_hard"),
                MenuOption("Back", "back")
            ],
                    MenuState.HIGH_SCORES: [
            MenuOption("Back to Menu", "back_to_menu")
        ],
        MenuState.GAME_MODE_SELECTION: [
            MenuOption("Classic Mode", "mode_classic"),
            MenuOption("Time Attack", "mode_time_attack"),
            MenuOption("Survival Mode", "mode_survival"),
            MenuOption("Speed Mode", "mode_speed"),
            MenuOption("Back to Menu", "back_to_menu")
        ]
        }
    
    def _setup_input_callbacks(self):
        """Set up input callbacks for menu navigation."""
        self.input_manager.register_callback(InputAction.MOVE_UP, self._handle_navigate_up)
        self.input_manager.register_callback(InputAction.MOVE_DOWN, self._handle_navigate_down)
        self.input_manager.register_callback(InputAction.CONFIRM, self._handle_select)
        self.input_manager.register_callback(InputAction.CANCEL, self._handle_cancel)
    
    def _handle_navigate_up(self, action: InputAction, key: int):
        """Handle navigation up in menu."""
        if not self.menu_active:
            return
        
        current_options = self.menu_options.get(self.current_state, [])
        if current_options:
            self.selected_index = (self.selected_index - 1) % len(current_options)
            # Skip disabled options
            while not current_options[self.selected_index].enabled:
                self.selected_index = (self.selected_index - 1) % len(current_options)
    
    def _handle_navigate_down(self, action: InputAction, key: int):
        """Handle navigation down in menu."""
        if not self.menu_active:
            return
        
        current_options = self.menu_options.get(self.current_state, [])
        if current_options:
            self.selected_index = (self.selected_index + 1) % len(current_options)
            # Skip disabled options
            while not current_options[self.selected_index].enabled:
                self.selected_index = (self.selected_index + 1) % len(current_options)
    
    def _handle_select(self, action: InputAction, key: int):
        """Handle menu option selection."""
        if not self.menu_active:
            return
        
        current_options = self.menu_options.get(self.current_state, [])
        if current_options and 0 <= self.selected_index < len(current_options):
            selected_option = current_options[self.selected_index]
            if selected_option.enabled:
                self._execute_menu_action(selected_option.action)
    
    def _handle_cancel(self, action: InputAction, key: int):
        """Handle cancel/back action."""
        if not self.menu_active:
            return
        
        if self.current_state == MenuState.START_MENU:
            # In start menu, cancel quits the game
            self._execute_menu_action("quit")
        elif self.current_state == MenuState.GAME_OVER:
            # In game over, cancel goes to main menu
            self._execute_menu_action("main_menu")
        elif self.current_state == MenuState.PAUSE_MENU:
            # In pause menu, cancel resumes the game
            self._execute_menu_action("resume")
        elif self.current_state == MenuState.SETTINGS_MENU:
            # In settings, cancel goes back
            self._execute_menu_action("back")
        elif self.current_state == MenuState.DIFFICULTY_SELECTION:
            # In difficulty selection, cancel goes back to settings
            self._execute_menu_action("back")
        elif self.current_state == MenuState.HIGH_SCORES:
            # In high scores, cancel goes back to main menu
            self._execute_menu_action("back_to_menu")
    
    def _execute_menu_action(self, action: str):
        """Execute a menu action."""
        if action in self.menu_callbacks:
            try:
                self.menu_callbacks[action]()
            except Exception as e:
                print(f"Error executing menu action {action}: {e}")
        else:
            print(f"No callback registered for menu action: {action}")
    
    def register_callback(self, action: str, callback: Callable):
        """Register a callback for a menu action."""
        self.menu_callbacks[action] = callback
    
    def set_menu_callback(self, action: str, callback: Callable):
        """Set a callback for a specific menu action (alias for register_callback)."""
        self.register_callback(action, callback)
    
    def unregister_callback(self, action: str):
        """Unregister a callback for a menu action."""
        if action in self.menu_callbacks:
            del self.menu_callbacks[action]
    
    def set_menu_state(self, state: MenuState):
        """Change the current menu state."""
        if state != self.current_state:
            self.current_state = state
            self.selected_index = 0
            self.transition_timer = 0.0
    
    def get_current_state(self) -> MenuState:
        """Get the current menu state."""
        return self.current_state
    
    def get_current_options(self) -> List[MenuOption]:
        """Get the current menu options."""
        return self.menu_options.get(self.current_state, [])
    
    def get_selected_index(self) -> int:
        """Get the currently selected option index."""
        return self.selected_index
    
    def get_selected_option(self) -> Optional[MenuOption]:
        """Get the currently selected option."""
        current_options = self.get_current_options()
        if current_options and 0 <= self.selected_index < len(current_options):
            return current_options[self.selected_index]
        return None
    
    def set_option_enabled(self, state: MenuState, option_index: int, enabled: bool):
        """Enable or disable a specific menu option."""
        if state in self.menu_options and 0 <= option_index < len(self.menu_options[state]):
            self.menu_options[state][option_index].enabled = enabled
    
    def add_menu_option(self, state: MenuState, option: MenuOption):
        """Add a new menu option to a specific state."""
        if state not in self.menu_options:
            self.menu_options[state] = []
        self.menu_options[state].append(option)
    
    def remove_menu_option(self, state: MenuState, option_index: int):
        """Remove a menu option from a specific state."""
        if state in self.menu_options and 0 <= option_index < len(self.menu_options[state]):
            del self.menu_options[state][option_index]
    
    def enable_menu(self):
        """Enable menu functionality."""
        self.menu_active = True
    
    def disable_menu(self):
        """Disable menu functionality."""
        self.menu_active = False
    
    def is_menu_active(self) -> bool:
        """Check if the menu is active."""
        return self.menu_active
    
    def update(self, delta_time: float):
        """Update the menu manager (call once per frame)."""
        # Update transition timer
        if self.transition_timer > 0:
            self.transition_timer = max(0, self.transition_timer - delta_time)
        
        # Update background animation
        self.background_animation_timer += delta_time * self.background_animation_speed
    
    def get_transition_progress(self) -> float:
        """Get the current transition progress (0.0 to 1.0)."""
        if self.transition_duration <= 0:
            return 1.0
        return 1.0 - (self.transition_timer / self.transition_duration)
    
    def get_background_animation_value(self) -> float:
        """Get the current background animation value for effects."""
        return self.background_animation_timer
    
    def reset_selection(self):
        """Reset the menu selection to the first option."""
        self.selected_index = 0
    
    def get_menu_title(self) -> str:
        """Get the title for the current menu state."""
        title_map = {
            MenuState.START_MENU: "🐍 SNAKE GAME",
            MenuState.GAME_OVER: "GAME OVER",
            MenuState.PAUSE_MENU: "PAUSED",
            MenuState.SETTINGS_MENU: "SETTINGS",
            MenuState.DIFFICULTY_SELECTION: "DIFFICULTY",
            MenuState.HIGH_SCORES: "🏆 HIGH SCORES"
        }
        return title_map.get(self.current_state, "")
    
    def get_menu_instructions(self) -> str:
        """Get the instructions for the current menu state."""
        instruction_map = {
            MenuState.START_MENU: "Use ↑↓ to navigate, Enter to select",
            MenuState.GAME_OVER: "Use ↑↓ to navigate, Enter to select",
            MenuState.PAUSE_MENU: "Use ↑↓ to navigate, Enter to select",
            MenuState.SETTINGS_MENU: "Use ↑↓ to navigate, Enter to select, Esc to go back",
            MenuState.DIFFICULTY_SELECTION: "Use ↑↓ to navigate, Enter to select, Esc to go back",
            MenuState.HIGH_SCORES: "Press Enter or Esc to return to menu"
        }
        return instruction_map.get(self.current_state, "")
    
    def get_menu_colors(self) -> Dict[str, str]:
        """Get the current menu colors."""
        return self.menu_colors.copy()
    
    def set_menu_colors(self, colors: Dict[str, str]):
        """Set custom menu colors."""
        self.menu_colors.update(colors)
    
    def get_menu_stats(self) -> Dict:
        """Get menu statistics for debugging."""
        return {
            "current_state": self.current_state.value,
            "selected_index": self.selected_index,
            "menu_active": self.menu_active,
            "transition_progress": self.get_transition_progress(),
            "background_animation": self.background_animation_timer,
            "current_options_count": len(self.get_current_options())
        }
