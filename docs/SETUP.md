# 🚀 Setup Guide

This guide provides comprehensive setup instructions for the Python Snake Game project.

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Prerequisites](#prerequisites)
3. [Installation Methods](#installation-methods)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Development Setup](#development-setup)

## 🖥️ System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14, or Ubuntu 18.04+
- **Python**: Version 3.8.0 or higher
- **Memory**: 4GB RAM
- **Graphics**: Any graphics card with OpenGL 2.1+ support
- **Storage**: 100MB available disk space
- **Display**: 1024x768 resolution

### Recommended Requirements
- **Operating System**: Windows 11, macOS 12+, or Ubuntu 20.04+
- **Python**: Version 3.9+ or 3.11+
- **Memory**: 8GB RAM or higher
- **Graphics**: Modern graphics card with OpenGL 3.3+ support
- **Storage**: 500MB available disk space
- **Display**: 1920x1080 resolution or higher

### Platform-Specific Requirements

#### Windows
- Windows 10 (version 1903) or later
- Microsoft Visual C++ Redistributable 2015-2022
- DirectX 11 compatible graphics card

#### macOS
- macOS 10.14 (Mojave) or later
- Metal-compatible graphics card
- Xcode Command Line Tools (for development)

#### Linux
- Ubuntu 18.04+ or equivalent
- OpenGL libraries: `libgl1-mesa-dev`
- Audio libraries: `libasound2-dev`
- Development tools: `build-essential`

## 🔧 Prerequisites

### Required Software

1. **Python 3.8+**
   ```bash
   # Check Python version
   python --version
   # or
   python3 --version
   ```

2. **pip (Python Package Installer)**
   ```bash
   # Check pip version
   pip --version
   # or
   pip3 --version
   ```

3. **Git (for cloning repository)**
   ```bash
   # Check Git version
   git --version
   ```

4. **Virtual Environment Tool**
   - Built into Python 3.3+
   - Alternative: `virtualenv` package

### Optional Software

1. **Code Editor/IDE**
   - VS Code with Python extension (recommended)
   - PyCharm Community Edition
   - Vim/Emacs with Python support

2. **Version Control GUI**
   - GitHub Desktop
   - GitKraken
   - SourceTree

## 📦 Installation Methods

### Method 1: Standard Installation (Recommended)

#### Step 1: Clone Repository
```bash
# Clone the repository
git clone https://github.com/your-username/snake-game.git

# Navigate to project directory
cd snake-game
```

#### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

#### Step 4: Verify Installation
```bash
# Check pygame installation
python -c "import pygame; print(f'Pygame {pygame.version.ver} installed successfully')"

# Run tests to verify everything works
python -m pytest tests/ -v
```

### Method 2: Development Installation

#### Step 1: Clone and Setup
```bash
# Clone repository
git clone https://github.com/your-username/snake-game.git
cd snake-game

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### Step 2: Install Development Dependencies
```bash
# Install in editable mode with development dependencies
pip install -e ".[dev]"

# Install additional development tools
pip install pre-commit
pip install coverage
```

#### Step 3: Setup Development Tools
```bash
# Install pre-commit hooks
pre-commit install

# Verify development setup
python -m pytest tests/ --cov=src --cov-report=html
```

### Method 3: Docker Installation

#### Step 1: Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Run the game
CMD ["python", "src/main.py"]
```

#### Step 2: Build and Run
```bash
# Build Docker image
docker build -t snake-game .

# Run the game
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix snake-game
```

## ⚙️ Configuration

### Environment Variables

The game can be configured using environment variables:

```bash
# Display settings
export SNAKE_GAME_FULLSCREEN=false
export SNAKE_GAME_RESOLUTION=1920x1080
export SNAKE_GAME_FPS=60

# Audio settings
export SNAKE_GAME_VOLUME=0.8
export SNAKE_GAME_MUSIC=true
export SNAKE_GAME_SOUND_EFFECTS=true

# Game settings
export SNAKE_GAME_DIFFICULTY=medium
export SNAKE_GAME_SPEED=normal
export SNAKE_GAME_CONTROLS=keyboard

# Debug settings
export SNAKE_GAME_DEBUG=false
export SNAKE_GAME_LOG_LEVEL=INFO
```

### Configuration Files

#### Game Settings File
Create `config/settings.json`:
```json
{
  "display": {
    "fullscreen": false,
    "resolution": "1920x1080",
    "fps": 60,
    "vsync": true
  },
  "audio": {
    "master_volume": 0.8,
    "music_volume": 0.7,
    "sfx_volume": 0.9,
    "enable_music": true,
    "enable_sfx": true
  },
  "game": {
    "difficulty": "medium",
    "starting_speed": "normal",
    "speed_progression": true,
    "power_ups": true,
    "obstacles": true
  },
  "controls": {
    "keyboard": true,
    "mouse": false,
    "gamepad": false,
    "key_bindings": {
      "up": ["UP", "W"],
      "down": ["DOWN", "S"],
      "left": ["LEFT", "A"],
      "right": ["RIGHT", "D"],
      "pause": ["SPACE", "P"],
      "restart": ["R"],
      "quit": ["Q", "ESCAPE"]
    }
  }
}
```

#### User Preferences File
The game automatically creates `config/user_preferences.json`:
```json
{
  "last_difficulty": "medium",
  "last_game_mode": "classic",
  "high_scores": [],
  "audio_settings": {
    "master_volume": 0.8,
    "music_volume": 0.7,
    "sfx_volume": 0.9
  },
  "display_settings": {
    "fullscreen": false,
    "resolution": "1920x1080"
  }
}
```

## ✅ Verification

### Basic Verification

1. **Check Python Installation**
   ```bash
   python --version
   pip --version
   ```

2. **Verify Dependencies**
   ```bash
   python -c "import pygame; print('Pygame OK')"
   python -c "import pytest; print('Pytest OK')"
   ```

3. **Run Test Suite**
   ```bash
   python -m pytest tests/ -v
   ```

4. **Launch Game**
   ```bash
   python src/main.py
   ```

### Advanced Verification

1. **Check Game Assets**
   ```bash
   # Verify assets directory structure
   ls -la src/assets/
   ```

2. **Test Game Functionality**
   ```bash
   # Run specific test categories
   python -m pytest tests/test_game_logic.py -v
   python -m pytest tests/test_ui_components.py -v
   ```

3. **Performance Testing**
   ```bash
   # Run performance benchmarks
   python -m pytest tests/test_performance.py -v
   ```

## 🐛 Troubleshooting

### Common Installation Issues

#### Python Version Issues
**Problem**: "Python version not supported" error
**Solution**: 
```bash
# Check Python version
python --version

# Install Python 3.8+ if needed
# Windows: Download from python.org
# macOS: brew install python@3.9
# Linux: sudo apt install python3.9
```

#### Pygame Installation Issues
**Problem**: Pygame fails to install
**Solution**:
```bash
# Update pip first
python -m pip install --upgrade pip

# Install system dependencies (Linux)
sudo apt-get install python3-dev python3-pip python3-venv
sudo apt-get install libgl1-mesa-dev libasound2-dev

# Try alternative installation
pip install pygame --pre
```

#### Virtual Environment Issues
**Problem**: Virtual environment not activating
**Solution**:
```bash
# Windows
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate

# Check if activated
which python  # Should point to venv directory
```

### Runtime Issues

#### Game Won't Start
**Problem**: Game crashes on startup
**Solutions**:
1. Check Python and Pygame versions
2. Verify all dependencies are installed
3. Check system graphics drivers
4. Run with debug mode: `SNAKE_GAME_DEBUG=true python src/main.py`

#### Performance Issues
**Problem**: Low frame rate or lag
**Solutions**:
1. Close other applications
2. Reduce graphics quality in settings
3. Update graphics drivers
4. Check system power settings

#### Audio Issues
**Problem**: No sound or distorted audio
**Solutions**:
1. Check system audio settings
2. Verify audio drivers
3. Try different audio output devices
4. Check game audio settings

### Platform-Specific Issues

#### Windows Issues
- **Missing Visual C++ Redistributable**: Download and install from Microsoft
- **Graphics Driver Issues**: Update graphics drivers
- **Permission Issues**: Run as administrator

#### macOS Issues
- **Missing Xcode Tools**: Install with `xcode-select --install`
- **Security Issues**: Allow Python in Security & Privacy settings
- **Graphics Issues**: Update macOS and graphics drivers

#### Linux Issues
- **Missing Libraries**: Install with package manager
- **Display Issues**: Check X11/Wayland configuration
- **Audio Issues**: Install ALSA/PulseAudio packages

## 🛠️ Development Setup

### Setting Up Development Environment

1. **Install Development Tools**
   ```bash
   pip install -e ".[dev]"
   pip install pre-commit coverage black flake8 mypy
   ```

2. **Configure Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

3. **Setup IDE/Editor**
   - VS Code: Install Python extension
   - PyCharm: Configure virtual environment
   - Vim: Install Python language server

### Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes and Test**
   ```bash
   # Run quality checks
   black src/ tests/
   flake8 src/ tests/
   mypy src/
   
   # Run tests
   pytest tests/ -v
   ```

3. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add your feature"
   git push origin feature/your-feature-name
   ```

### Code Quality Tools

- **Black**: Code formatting
- **Flake8**: Linting and style checking
- **MyPy**: Type checking
- **Pytest**: Testing framework
- **Coverage**: Code coverage reporting

### Testing Strategy

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test component interactions
3. **System Tests**: Test complete game functionality
4. **Performance Tests**: Test game performance and frame rates

## 📚 Additional Resources

### Documentation
- [Python Official Documentation](https://docs.python.org/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Pytest Documentation](https://docs.pytest.org/)

### Community Support
- [Python Discord](https://discord.gg/python)
- [Pygame Community](https://www.pygame.org/community)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/python+pygame)

### Learning Resources
- [Real Python Tutorials](https://realpython.com/)
- [Game Development Patterns](https://gameprogrammingpatterns.com/)
- [Python Game Development](https://realpython.com/pygame-a-primer/)

---

**Need Help?** If you encounter issues not covered in this guide, please:
1. Check the [Issues](https://github.com/your-repo/snake-game/issues) page
2. Search existing discussions
3. Create a new issue with detailed information
4. Join our community channels for support
