"""
Game Loop

This module contains the main game loop that handles:
- Frame timing and delta time calculation
- Game state updates
- Frame rate management
- Game loop control
"""

import time
from typing import Optional, Callable
from .game_logic import GameLogic


class GameLoop:
    """
    Main game loop controller.
    
    Manages the game's main loop, timing, and update frequency.
    """
    
    def __init__(self, game_logic: GameLogic, target_fps: int = 60):
        """Initialize the game loop."""
        self.game_logic = game_logic
        self.target_fps = target_fps
        self.target_frame_time = 1.0 / target_fps
        
        # Loop control
        self.running = False
        self.paused = False
        
        # Timing variables
        self.last_frame_time = 0.0
        self.delta_time = 0.0
        self.frame_count = 0
        self.fps_counter = 0
        self.fps_timer = 0.0
        self.current_fps = 0.0
        
        # Callbacks
        self.update_callback: Optional[Callable[[float], None]] = None
        self.render_callback: Optional[Callable[[], None]] = None
        self.pre_update_callback: Optional[Callable[[float], None]] = None
        self.post_update_callback: Optional[Callable[[float], None]] = None
    
    def start(self) -> None:
        """Start the game loop."""
        self.running = True
        self.last_frame_time = time.time()
        # Don't run the loop here - let the main game loop call update methods
        # self._run_loop()  # This was causing the conflict
    
    def stop(self) -> None:
        """Stop the game loop."""
        self.running = False
    
    def pause(self) -> None:
        """Pause the game loop."""
        self.paused = True
    
    def resume(self) -> None:
        """Resume the game loop."""
        self.paused = False
    
    def set_update_callback(self, callback: Callable[[float], None]) -> None:
        """Set the update callback function."""
        self.update_callback = callback
    
    def set_render_callback(self, callback: Callable[[], None]) -> None:
        """Set the render callback function."""
        self.render_callback = callback
    
    def set_pre_update_callback(self, callback: Callable[[float], None]) -> None:
        """Set the pre-update callback function."""
        self.pre_update_callback = callback
    
    def set_post_update_callback(self, callback: Callable[[float], None]) -> None:
        """Set the post-update callback function."""
        self.post_update_callback = callback
    
    def update(self) -> None:
        """Update the game loop (called from main game loop)."""
        if not self.running:
            return
            
        # Calculate delta time
        current_time = time.time()
        self.delta_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        
        # Cap delta time to prevent spiral of death
        if self.delta_time > 0.1:  # Max 100ms
            self.delta_time = 0.1
        
        # Update FPS counter
        self._update_fps_counter()
        
        if not self.paused:
            # Pre-update phase
            if self.pre_update_callback:
                self.pre_update_callback(self.delta_time)
            
            # Update game logic
            self.game_logic.update(self.delta_time)
            
            # Update callback
            if self.update_callback:
                self.update_callback(self.delta_time)
            
            # Post-update phase
            if self.post_update_callback:
                self.post_update_callback(self.delta_time)
        
        # Render callback
        if self.render_callback:
            self.render_callback()
        
        # Frame rate limiting
        self._limit_frame_rate()
        
        # Increment frame counter
        self.frame_count += 1
    
    def physics_update(self) -> None:
        """Update physics at fixed timestep (called from main game loop)."""
        if not self.running or self.paused:
            return

        # Use accumulator/timestep if available (FixedTimestepGameLoop),
        # otherwise fall back to target frame timing.
        physics_accumulator = getattr(self, "physics_accumulator", 0.0) + self.delta_time
        physics_timestep = getattr(self, "physics_timestep", self.target_frame_time)

        # Step physics in fixed increments
        while physics_accumulator >= physics_timestep:
            # Prefer callback if provided (FixedTimestepGameLoop)
            physics_cb = getattr(self, "physics_update_callback", None)
            if physics_cb:
                physics_cb(physics_timestep)

            # Advance game logic at fixed timestep
            self.game_logic.update(physics_timestep)

            physics_accumulator -= physics_timestep

        # Persist accumulator back if attribute exists
        if hasattr(self, "physics_accumulator"):
            self.physics_accumulator = physics_accumulator
    
    def _run_loop(self) -> None:
        """Main game loop."""
        while self.running:
            # Calculate delta time
            current_time = time.time()
            self.delta_time = current_time - self.last_frame_time
            self.last_frame_time = current_time
            
            # Cap delta time to prevent spiral of death
            if self.delta_time > 0.1:  # Max 100ms
                self.delta_time = 0.1
            
            # Update FPS counter
            self._update_fps_counter()
            
            if not self.paused:
                # Pre-update phase
                if self.pre_update_callback:
                    self.pre_update_callback(self.delta_time)
                
                # Update game logic
                self.game_logic.update(self.delta_time)
                
                # Update callback
                if self.update_callback:
                    self.update_callback(self.delta_time)
                
                # Post-update phase
                if self.post_update_callback:
                    self.post_update_callback(self.delta_time)
            
            # Render callback
            if self.render_callback:
                self.render_callback()
            
            # Frame rate limiting
            self._limit_frame_rate()
            
            # Increment frame counter
            self.frame_count += 1
    
    def _update_fps_counter(self) -> None:
        """Update FPS counter and timer."""
        self.fps_counter += 1
        self.fps_timer += self.delta_time
        
        # Update FPS every second
        if self.fps_timer >= 1.0:
            self.current_fps = self.fps_counter / self.fps_timer
            self.fps_counter = 0
            self.fps_timer = 0.0
    
    def _limit_frame_rate(self) -> None:
        """Limit frame rate to target FPS."""
        frame_time = time.time() - self.last_frame_time
        sleep_time = max(0, self.target_frame_time - frame_time)
        
        if sleep_time > 0:
            time.sleep(sleep_time)
    
    def get_delta_time(self) -> float:
        """Get the time elapsed since last frame."""
        return self.delta_time
    
    def get_current_fps(self) -> float:
        """Get the current frame rate."""
        return self.current_fps
    
    def get_frame_count(self) -> int:
        """Get the total number of frames rendered."""
        return self.frame_count
    
    def get_target_fps(self) -> int:
        """Get the target frame rate."""
        return self.target_fps
    
    def set_target_fps(self, fps: int) -> None:
        """Set the target frame rate."""
        self.target_fps = fps
        self.target_frame_time = 1.0 / fps
    
    def is_running(self) -> bool:
        """Check if the game loop is running."""
        return self.running
    
    def is_paused(self) -> bool:
        """Check if the game loop is paused."""
        return self.paused
    
    def get_performance_stats(self) -> dict:
        """Get performance statistics."""
        return {
            "current_fps": self.current_fps,
            "target_fps": self.target_fps,
            "frame_count": self.frame_count,
            "delta_time": self.delta_time,
            "running": self.running,
            "paused": self.paused
        }


class FixedTimestepGameLoop(GameLoop):
    """
    Fixed timestep game loop for consistent physics updates.
    
    This loop separates physics updates from rendering updates,
    ensuring consistent game behavior regardless of frame rate.
    """
    
    def __init__(self, game_logic: GameLogic, target_fps: int = 60, physics_fps: int = 60):
        """Initialize the fixed timestep game loop."""
        super().__init__(game_logic, target_fps)
        self.physics_fps = physics_fps
        self.physics_timestep = 1.0 / physics_fps
        self.physics_accumulator = 0.0
        
        # Physics update callback
        self.physics_update_callback: Optional[Callable[[float], None]] = None
    
    def set_physics_update_callback(self, callback: Callable[[float], None]) -> None:
        """Set the physics update callback function."""
        self.physics_update_callback = callback
    
    def _run_loop(self) -> None:
        """Main game loop with fixed physics timestep."""
        while self.running:
            # Calculate delta time
            current_time = time.time()
            self.delta_time = current_time - self.last_frame_time
            self.last_frame_time = current_time
            
            # Cap delta time to prevent spiral of death
            if self.delta_time > 0.1:  # Max 100ms
                self.delta_time = 0.1
            
            # Update FPS counter
            self._update_fps_counter()
            
            if not self.paused:
                # Accumulate time for physics updates
                self.physics_accumulator += self.delta_time
                
                # Update physics at fixed timestep
                while self.physics_accumulator >= self.physics_timestep:
                    if self.physics_update_callback:
                        self.physics_update_callback(self.physics_timestep)
                    
                    # Update game logic
                    self.game_logic.update(self.physics_timestep)
                    
                    self.physics_accumulator -= self.physics_timestep
                
                # Pre-update phase
                if self.pre_update_callback:
                    self.pre_update_callback(self.delta_time)
                
                # Update callback
                if self.update_callback:
                    self.update_callback(self.delta_time)
                
                # Post-update phase
                if self.post_update_callback:
                    self.post_update_callback(self.delta_time)
            
            # Render callback
            if self.render_callback:
                self.render_callback()
            
            # Frame rate limiting
            self._limit_frame_rate()
            
            # Increment frame counter
            self.frame_count += 1
    
    def get_physics_fps(self) -> int:
        """Get the physics update frequency."""
        return self.physics_fps
    
    def set_physics_fps(self, fps: int) -> None:
        """Set the physics update frequency."""
        self.physics_fps = fps
        self.physics_timestep = 1.0 / fps
    
    def get_performance_stats(self) -> dict:
        """Get performance statistics including physics info."""
        stats = super().get_performance_stats()
        stats.update({
            "physics_fps": self.physics_fps,
            "physics_timestep": self.physics_timestep,
            "physics_accumulator": self.physics_accumulator
        })
        return stats
