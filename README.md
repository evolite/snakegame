# 🐍 Python Snake Game

A modern, feature-rich Snake game built with Python and Pygame, featuring smooth gameplay, multiple difficulty levels, power-ups, and an engaging user experience.

## 🎮 Game Features

- **Classic Snake Gameplay**: Smooth snake movement with intuitive controls
- **Multiple Difficulty Levels**: Easy, Medium, and Hard modes with progressive challenge
- **Dynamic Speed Progression**: Snake speed increases as it grows for added challenge
- **High Score Tracking**: Persistent high score system with player names
- **Power-ups System**: Speed boost, invincibility, and score multiplier power-ups
- **Special Food Types**: Different food types with unique effects and scoring
- **Multiple Game Modes**: Classic, Time Attack, and Survival modes
- **Obstacles and Walls**: Strategic gameplay elements for enhanced challenge
- **Visual Effects**: Smooth animations and particle effects
- **Audio System**: Sound effects and background music
- **Modern UI**: Clean, intuitive user interface with responsive controls

## 🚀 Quick Start

### System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher (3.9+ recommended)
- **Memory**: Minimum 4GB RAM (8GB+ recommended)
- **Graphics**: Any modern graphics card with OpenGL support
- **Storage**: 100MB available disk space
- **Display**: 1024x768 minimum resolution (1920x1080 recommended)

### 🎯 Two Ways to Run

#### Option 1: Python Script (Development)
Run the game directly with Python (requires Python installation)

#### Option 2: Executable (.exe) (Distribution)
Run the standalone executable (no Python required)

### Prerequisites

- Python 3.8+ with pip package manager
- Git for cloning the repository
- Virtual environment tool (built into Python 3.3+)

### Installation

#### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd snake-game
```

#### Step 2: Set Up Python Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
# Install all dependencies including development tools
pip install -r requirements.txt

# Or install with development dependencies
pip install -e ".[dev]"
```

#### Step 4: Verify Installation
```bash
# Check if pygame is properly installed
python -c "import pygame; print(f'Pygame version: {pygame.version.ver}')"

# Run a quick test
python -m pytest tests/ -v
```

#### Step 5: Launch the Game
```bash
python src/main.py
```

## 📦 Creating Executable (.exe)

### Quick Build (Windows)
```bash
# Double-click the batch file
build_exe.bat
```

### Manual Build
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build_exe.py

# Or use PyInstaller directly
pyinstaller snake_game.spec
```

### Build Output
After successful build, you'll find:
- **Executable**: `dist/SnakeGame/SnakeGame.exe`
- **Distribution Folder**: `dist/SnakeGame/` (contains everything needed)

### Running the Executable
- **Double-click** `SnakeGame.exe` to run
- **No Python installation required** on target machine
- **Portable**: Copy the entire `dist/SnakeGame` folder to any Windows machine

## 🎯 Game Controls

### Movement Controls
- **Arrow Keys** or **WASD**: Control snake direction
- **Mouse**: Alternative control method (if enabled)

### Game Controls
- **P** or **Space**: Pause/Resume game
- **R**: Restart current game
- **M**: Mute/Unmute audio
- **Q** or **ESC**: Quit to main menu or exit game

### Menu Navigation
- **Enter**: Select menu option
- **Arrow Keys**: Navigate menu items
- **Tab**: Switch between input fields

## 🏗️ Project Structure

```
snake-game/
├── src/                    # Source code directory
│   ├── main.py            # Main game entry point and initialization
│   ├── game/               # Core game engine components
│   │   ├── __init__.py     # Game module initialization
│   │   ├── collision.py    # Collision detection system
│   │   ├── food.py         # Food spawning and management
│   │   ├── game_logic.py   # Main game logic and rules
│   │   ├── game_loop.py    # Game loop and timing
│   │   ├── game_state.py   # Game state management
│   │   ├── grid.py         # Game grid and coordinate system
│   │   ├── scoring.py      # Score calculation and tracking
│   │   └── snake.py        # Snake movement and behavior
│   ├── ui/                 # User interface components
│   │   ├── __init__.py     # UI module initialization
│   │   ├── display.py      # Main display and window management
│   │   ├── food_renderer.py # Food rendering and effects
│   │   ├── game_controller.py # Game input and control handling
│   │   ├── game_renderer.py # Main game rendering engine
│   │   ├── input_manager.py # Input processing and management
│   │   └── snake_renderer.py # Snake rendering and animations
│   ├── utils/              # Utility functions and helpers
│   │   └── __init__.py     # Utils module initialization
│   └── assets/             # Game assets (images, sounds, fonts)
├── tests/                  # Test suite and test files
│   ├── __init__.py         # Test module initialization
│   ├── test_core_engine.py # Core engine functionality tests
│   ├── test_game_state.py  # Game state management tests
│   ├── test_grid.py        # Grid system tests
│   ├── test_input_controls.py # Input system tests
│   ├── test_snake.py       # Snake behavior tests
│   └── test_ui_components.py # UI component tests
├── docs/                   # Project documentation
├── requirements.txt         # Python package dependencies
├── pyproject.toml          # Project configuration and build settings
├── .gitignore             # Git ignore rules
└── README.md              # This documentation file
```

## 🧪 Testing and Quality Assurance

### Running Tests
```bash
# Run all tests
pytest tests/

# Run tests with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_game_logic.py

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html
```

### Code Quality Tools
This project uses several tools to maintain code quality:

- **Black**: Automatic code formatting
- **Flake8**: Linting and style checking
- **MyPy**: Static type checking
- **Pytest**: Testing framework

### Code Quality Commands
```bash
# Format code with Black
black src/ tests/

# Check code style with Flake8
flake8 src/ tests/

# Run type checking with MyPy
mypy src/

# Run all quality checks
black src/ tests/ && flake8 src/ tests/ && mypy src/
```

## 🔧 Configuration

### Game Settings
The game can be configured through various settings files and environment variables:

- **Display Settings**: Resolution, fullscreen mode, frame rate
- **Audio Settings**: Volume levels, sound effects, music
- **Game Settings**: Difficulty, speed, controls
- **Performance Settings**: Graphics quality, particle effects

### Environment Variables
```bash
# Set game display mode
export SNAKE_GAME_FULLSCREEN=true

# Set audio volume
export SNAKE_GAME_VOLUME=0.8

# Enable debug mode
export SNAKE_GAME_DEBUG=true
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Game Won't Start
**Problem**: Game crashes on startup or shows error messages
**Solutions**:
1. Verify Python version: `python --version` (should be 3.8+)
2. Check pygame installation: `python -c "import pygame"`
3. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
4. Check system graphics drivers are up to date

#### Performance Issues
**Problem**: Game runs slowly or has low frame rates
**Solutions**:
1. Close other applications to free up system resources
2. Reduce graphics quality in game settings
3. Update graphics drivers
4. Check if running in power-saving mode

#### Audio Issues
**Problem**: No sound or distorted audio
**Solutions**:
1. Check system audio settings and volume
2. Verify audio drivers are installed and working
3. Try different audio output devices
4. Check game audio settings in the menu

#### Control Issues
**Problem**: Controls not responding or behaving unexpectedly
**Solutions**:
1. Check if another application is capturing keyboard input
2. Verify game is in focus (click on game window)
3. Try different control schemes
4. Restart the game

#### Installation Issues
**Problem**: Dependencies fail to install
**Solutions**:
1. Update pip: `python -m pip install --upgrade pip`
2. Use virtual environment: `python -m venv venv`
3. Install system dependencies (Linux): `sudo apt-get install python3-dev python3-pip`
4. Check internet connection and firewall settings

### Getting Help

If you encounter issues not covered here:

1. Check the [Issues](https://github.com/your-repo/snake-game/issues) page
2. Search existing discussions for similar problems
3. Create a new issue with detailed information:
   - Operating system and version
   - Python version
   - Error messages or logs
   - Steps to reproduce the issue

## 🎨 Development

### Setting Up Development Environment

1. **Clone and Setup**:
   ```bash
   git clone <repository-url>
   cd snake-game
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -e ".[dev]"
   ```

2. **Pre-commit Setup**:
   ```bash
   # Install pre-commit hooks
   pre-commit install
   ```

3. **IDE Configuration**:
   - Recommended: VS Code with Python extension
   - Alternative: PyCharm Community Edition
   - Configure your IDE to use the virtual environment

### Development Workflow

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**: Implement your feature or fix

3. **Run Quality Checks**:
   ```bash
   black src/ tests/
   flake8 src/ tests/
   mypy src/
   pytest tests/
   ```

4. **Commit Changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and Create PR**:
   ```bash
   git push origin feature/your-feature-name
   # Create Pull Request on GitHub
   ```

### Code Standards

- **Python Style**: Follow PEP 8 guidelines
- **Documentation**: Use docstrings for all public functions
- **Type Hints**: Include type hints for function parameters and returns
- **Testing**: Write tests for new functionality
- **Commits**: Use conventional commit messages

## 📚 Additional Resources

### Documentation
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python Game Development Guide](https://realpython.com/pygame-a-primer/)
- [Game Development Patterns](https://gameprogrammingpatterns.com/)

### Learning Resources
- [Python Game Development Tutorials](https://realpython.com/tutorials/game-dev/)
- [Pygame Examples](https://github.com/pygame/pygame/tree/main/examples)
- [Game Development Concepts](https://gamedev.net/)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests for new functionality**
5. **Ensure all tests pass**
6. **Submit a pull request**

### Contribution Areas

- **Bug Fixes**: Report and fix bugs
- **New Features**: Implement new game features
- **Documentation**: Improve documentation
- **Testing**: Add more test coverage
- **Performance**: Optimize game performance
- **UI/UX**: Improve user interface and experience

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Pygame Community**: For the excellent game development library
- **Python Community**: For the amazing programming language
- **Open Source Contributors**: For inspiration and code examples
- **Classic Snake Game**: For the timeless gameplay concept

## 📊 Project Status

- **Current Version**: 0.1.0 (Alpha)
- **Development Status**: Active Development
- **Last Updated**: August 2025
- **Next Milestone**: Beta Release with Enhanced Features

---

**Happy Gaming! 🎮**

For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/your-repo/snake-game).
