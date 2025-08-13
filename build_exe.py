#!/usr/bin/env python3
"""
Build script for creating Snake Game executable.
This script automates the process of packaging the game using PyInstaller.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    try:
        import pygame
        print(f"✓ Pygame {pygame.version.ver} found")
    except ImportError:
        print("✗ Pygame not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])

def clean_build_dirs():
    """Clean previous build artifacts."""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Clean .spec files (except our main one)
    for spec_file in Path('.').glob('*.spec'):
        if spec_file.name != 'snake_game.spec':
            spec_file.unlink()
            print(f"Removed {spec_file}")

def create_icon():
    """Create a simple icon if none exists."""
    # Skip icon creation for now to avoid build issues
    print("Note: No icon file created. The executable will use the default Windows icon.")

def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable...")
    
    # Use our spec file
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "snake_game.spec"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✓ Build completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed with error code {e.returncode}")
        return False
    
    return True

def verify_build():
    """Verify the build output."""
    exe_path = Path('dist/SnakeGame/SnakeGame.exe')
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✓ Executable created: {exe_path}")
        print(f"  Size: {size_mb:.1f} MB")
        print(f"  Location: {exe_path.absolute()}")
        return True
    else:
        print("✗ Executable not found in expected location")
        return False

def main():
    """Main build process."""
    print("🐍 Snake Game Executable Builder")
    print("=" * 40)
    
    # Check and install dependencies
    check_dependencies()
    
    # Clean previous builds
    clean_build_dirs()
    
    # Create icon if needed
    create_icon()
    
    # Build the executable
    if build_executable():
        if verify_build():
            print("\n🎉 Build successful!")
            print("\nYou can now run the game by double-clicking:")
            print("  dist/SnakeGame/SnakeGame.exe")
            print("\nOr distribute the entire 'dist/SnakeGame' folder.")
        else:
            print("\n❌ Build verification failed!")
            sys.exit(1)
    else:
        print("\n❌ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
