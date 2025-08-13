"""
Audio Manager for Snake Game

This module handles all audio-related functionality:
- Sound effects for game events
- Background music system
- Audio controls and volume settings
"""

import os
import pygame
from typing import Dict, Optional
from enum import Enum
from dataclasses import dataclass
import json


class SoundEffect(Enum):
    """Available sound effects."""
    FOOD_COLLECTION = "food_collection"
    COLLISION = "collision"
    GAME_OVER = "game_over"
    POWER_UP_ACTIVATE = "power_up_activate"
    MENU_SELECT = "menu_select"
    GAME_START = "game_start"


class BackgroundMusic(Enum):
    """Available background music tracks."""
    MAIN_MENU = "main_menu"
    GAMEPLAY = "gameplay"
    GAME_OVER = "game_over"


@dataclass
class AudioSettings:
    """Audio settings configuration."""
    master_volume: float = 1.0
    sound_effects_volume: float = 0.8
    music_volume: float = 0.6
    sound_effects_enabled: bool = True
    music_enabled: bool = True


class AudioManager:
    """Manages all audio functionality for the Snake Game."""
    
    def __init__(self, audio_directory: str = "assets/audio"):
        """Initialize the audio manager."""
        self.audio_directory = audio_directory
        self.settings = AudioSettings()
        self.sound_effects: Dict[str, pygame.mixer.Sound] = {}
        self.music_tracks: Dict[str, str] = {}
        self.current_music: Optional[str] = None
        self.is_initialized = False
        
        self._initialize_mixer()
        self._load_audio_files()
        self._load_settings()
    
    def _initialize_mixer(self) -> None:
        """Initialize pygame mixer for audio playback."""
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.is_initialized = True
            print("Audio system initialized successfully")
        except Exception as e:
            print(f"Failed to initialize audio system: {e}")
            self.is_initialized = False
    
    def _load_audio_files(self) -> None:
        """Load all audio files from the audio directory."""
        if not self.is_initialized:
            return
        
        os.makedirs(self.audio_directory, exist_ok=True)
        self._load_sound_effects()
        self._load_music_tracks()
    
    def _load_sound_effects(self) -> None:
        """Load sound effect files."""
        sound_effects_dir = os.path.join(self.audio_directory, "sound_effects")
        if not os.path.exists(sound_effects_dir):
            self._create_placeholder_sounds()
            return
        
        for sound_file in os.listdir(sound_effects_dir):
            if sound_file.endswith(('.wav', '.ogg', '.mp3')):
                sound_name = os.path.splitext(sound_file)[0]
                try:
                    sound_path = os.path.join(sound_effects_dir, sound_file)
                    sound = pygame.mixer.Sound(sound_path)
                    self.sound_effects[sound_name] = sound
                except Exception as e:
                    print(f"Failed to load sound effect {sound_file}: {e}")
    
    def _load_music_tracks(self) -> None:
        """Load music track files."""
        music_dir = os.path.join(self.audio_directory, "music")
        if not os.path.exists(music_dir):
            return
        
        for music_file in os.listdir(music_dir):
            if music_file.endswith(('.wav', '.ogg', '.mp3')):
                track_name = os.path.splitext(music_file)[0]
                track_path = os.path.join(music_dir, music_file)
                self.music_tracks[track_name] = track_path
    
    def _create_placeholder_sounds(self) -> None:
        """Create placeholder sound effects for testing."""
        print("Creating placeholder sound effects...")
        sample_rate = 44100
        duration = 0.1
        
        for sound_name in [effect.value for effect in SoundEffect]:
            frequency = 800 if "food" in sound_name else 400
            samples = int(sample_rate * duration)
            sound_data = []
            for i in range(samples):
                sample = int(32767 * 0.3 * (i % 2))
                sound_data.append(sample)
            
            try:
                sound = pygame.mixer.Sound(bytes(sound_data))
                self.sound_effects[sound_name] = sound
            except Exception as e:
                print(f"Failed to create placeholder sound {sound_name}: {e}")
    
    def play_sound_effect(self, effect: SoundEffect, volume: Optional[float] = None) -> None:
        """Play a sound effect."""
        if not self.is_initialized or not self.settings.sound_effects_enabled:
            return
        
        effect_name = effect.value
        if effect_name in self.sound_effects:
            sound = self.sound_effects[effect_name]
            vol = volume or self.settings.sound_effects_volume
            sound.set_volume(vol * self.settings.master_volume)
            
            try:
                sound.play()
            except Exception as e:
                print(f"Failed to play sound effect {effect_name}: {e}")
    
    def play_background_music(self, track: BackgroundMusic, loop: bool = True) -> None:
        """Play background music."""
        if not self.is_initialized or not self.settings.music_enabled:
            return
        
        track_name = track.value
        if track_name in self.music_tracks:
            track_path = self.music_tracks[track_name]
            
            try:
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.set_volume(self.settings.music_volume)
                pygame.mixer.music.play(-1 if loop else 0)
                self.current_music = track_name
            except Exception as e:
                print(f"Failed to play music track {track_name}: {e}")
    
    def stop_background_music(self) -> None:
        """Stop the currently playing background music."""
        if self.is_initialized:
            pygame.mixer.music.stop()
            self.current_music = None
    
    def set_master_volume(self, volume: float) -> None:
        """Set the master volume (0.0 to 1.0)."""
        self.settings.master_volume = max(0.0, min(1.0, volume))
        self._apply_volume_settings()
    
    def set_sound_effects_volume(self, volume: float) -> None:
        """Set the sound effects volume (0.0 to 1.0)."""
        self.settings.sound_effects_volume = max(0.0, min(1.0, volume))
        self._apply_volume_settings()
    
    def set_music_volume(self, volume: float) -> None:
        """Set the music volume (0.0 to 1.0)."""
        self.settings.music_volume = max(0.0, min(1.0, volume))
        if self.is_initialized:
            pygame.mixer.music.set_volume(self.settings.music_volume)
    
    def enable_sound_effects(self, enabled: bool) -> None:
        """Enable or disable sound effects."""
        self.settings.sound_effects_enabled = enabled
    
    def enable_music(self, enabled: bool) -> None:
        """Enable or disable music."""
        self.settings.music_enabled = enabled
        if not enabled:
            self.stop_background_music()
    
    def _apply_volume_settings(self) -> None:
        """Apply current volume settings to all audio."""
        if not self.is_initialized:
            return
        
        for sound in self.sound_effects.values():
            sound.set_volume(self.settings.sound_effects_volume * self.settings.master_volume)
    
    def _load_settings(self) -> None:
        """Load audio settings from file."""
        settings_file = os.path.join(self.audio_directory, "audio_settings.json")
        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    data = json.load(f)
                    self.settings = AudioSettings(**data)
        except Exception as e:
            print(f"Failed to load audio settings: {e}")
    
    def save_settings(self) -> None:
        """Save audio settings to file."""
        settings_file = os.path.join(self.audio_directory, "audio_settings.json")
        try:
            os.makedirs(os.path.dirname(settings_file), exist_ok=True)
            with open(settings_file, 'w') as f:
                json.dump(self.settings.__dict__, f, indent=2)
        except Exception as e:
            print(f"Failed to save audio settings: {e}")
    
    def cleanup(self) -> None:
        """Clean up audio resources."""
        if self.is_initialized:
            self.stop_background_music()
            self.save_settings()
            pygame.mixer.quit()
            self.is_initialized = False
