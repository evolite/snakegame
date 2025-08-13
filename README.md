# 🐍 Python Snake Game

A modern, feature-rich Snake game built with Python and Pygame.

## 🎮 Features

- Classic Snake gameplay with smooth controls
- Multiple difficulty levels
- High score tracking
- Modern graphics and animations
- Sound effects and music
- Power-ups and special food types
- Multiple game modes

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd snake-game
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the game:
```bash
python src/main.py
```

## 🎯 Controls

- **Arrow Keys** or **WASD**: Move the snake
- **P** or **Space**: Pause/Resume game
- **R**: Restart game
- **Q** or **ESC**: Quit game

## 🏗️ Project Structure

```
snake-game/
├── src/                    # Source code
│   ├── main.py            # Main game entry point
│   ├── game/              # Core game engine
│   ├── ui/                # User interface components
│   ├── utils/             # Utility functions
│   └── assets/            # Game assets (images, sounds)
├── tests/                 # Test files
├── docs/                  # Documentation
├── requirements.txt        # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

## 🎨 Development

### Code Style

This project uses:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

Format code:
```bash
black src/ tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Acknowledgments

- Built with Pygame
- Inspired by the classic Snake game
- Created as a learning project for Python game development
