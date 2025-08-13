# Testing Guide for Snake Game

This document provides comprehensive information about the automated testing framework for the Snake Game project.

## 🧪 Testing Framework Overview

The project uses **pytest** as the primary testing framework, along with several supporting tools for code quality and coverage reporting.

### Key Components

- **pytest**: Main testing framework
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking utilities
- **GitHub Actions**: CI/CD pipeline
- **Code Quality Tools**: black, flake8, mypy

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run All Tests

```bash
python -m pytest tests/ -v
```

### 3. Run Tests with Coverage

```bash
python -m pytest tests/ --cov=src --cov-report=html
```

### 4. Use the Test Runner Script

```bash
python run_tests.py --all
```

## 📁 Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and configuration
├── test_core_engine.py      # Core game engine tests
├── test_game_state.py       # Game state management tests
├── test_grid.py             # Grid system tests
├── test_input_controls.py   # Input handling tests
├── test_snake.py            # Snake object tests
└── test_ui_components.py    # UI component tests
```

## 🎯 Test Categories

### Unit Tests (`-m unit`)
- Test individual components in isolation
- Fast execution
- Use mocks for external dependencies

### Integration Tests (`-m integration`)
- Test component interactions
- Verify system boundaries
- May be slower than unit tests

### UI Tests (`-m ui`)
- Test rendering and display components
- Mock pygame for headless execution
- Verify UI behavior and state

### Game Logic Tests (`-m game_logic`)
- Test game mechanics and rules
- Verify game state transitions
- Test scoring and difficulty systems

## 🔧 Test Configuration

### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers = slow, integration, unit, ui, game_logic
```

### conftest.py
- **Mock pygame**: Prevents display initialization during testing
- **Common fixtures**: Reusable test objects and mocks
- **Path configuration**: Ensures proper import resolution

## 🎭 Mocking Strategy

### Why Mock pygame?
- **Headless execution**: Tests run without display
- **CI/CD compatibility**: Works in automated environments
- **Faster execution**: No graphics initialization overhead
- **Isolated testing**: Tests don't depend on system graphics

### Mock Objects Available
- `mock_display`: Display manager mock
- `mock_grid`: Grid system mock
- `mock_snake`: Snake object mock
- `mock_food_manager`: Food management mock
- `mock_power_ups_manager`: Power-ups system mock
- `mock_scoring_system`: Scoring system mock
- `mock_speed_system`: Speed system mock
- `mock_difficulty_manager`: Difficulty system mock

## 📊 Coverage Reporting

### Generate Coverage Report
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

### Coverage Reports Generated
- **Terminal**: Shows missing lines
- **HTML**: Interactive web report (`htmlcov/index.html`)
- **XML**: Machine-readable format for CI tools

### Coverage Targets
- **Minimum**: 70% (configured in pytest.ini)
- **Goal**: 85%+ for production code
- **UI Components**: 80%+ target

## 🚀 CI/CD Pipeline

### GitHub Actions Workflow
- **Triggers**: Push to main/develop, Pull Requests
- **Matrix Testing**: Python 3.8, 3.9, 3.10, 3.11
- **Quality Checks**: Formatting, linting, type checking
- **Coverage Upload**: Results sent to Codecov

### Workflow Jobs
1. **Test**: Run tests on multiple Python versions
2. **Quality**: Code formatting, linting, type checking
3. **Coverage**: Generate and upload coverage reports

## 🛠️ Test Runner Script

### Usage Examples

```bash
# Install dependencies
python run_tests.py --install

# Run unit tests only
python run_tests.py --unit

# Run with coverage
python run_tests.py --coverage

# Run code quality checks
python run_tests.py --quality

# Run everything
python run_tests.py --all

# Run specific test file
python run_tests.py --file tests/test_snake.py
```

### Available Commands
- `--unit`: Unit tests only
- `--integration`: Integration tests only
- `--ui`: UI tests only
- `--coverage`: Tests with coverage reporting
- `--quality`: Code quality checks
- `--install`: Install dependencies
- `--file`: Run specific test file
- `--all`: Run everything

## 📝 Writing Tests

### Test File Naming
- Files must start with `test_` or end with `_test.py`
- Classes must start with `Test`
- Functions must start with `test_`

### Example Test Structure
```python
import pytest
from src.game.snake import Snake
from src.game.grid import Position

class TestSnake:
    """Test the snake game object."""
    
    def test_snake_creation(self, sample_position):
        """Test snake creation."""
        snake = Snake(sample_position)
        assert snake.get_head() == sample_position
        assert snake.get_length() == 3
    
    @pytest.mark.slow
    def test_snake_movement(self, mock_grid):
        """Test snake movement (marked as slow)."""
        snake = Snake(Position(5, 5))
        result = snake.move(mock_grid)
        assert result is True
```

### Using Fixtures
```python
def test_with_mocks(self, mock_display, mock_grid, mock_snake):
    """Test using multiple mock fixtures."""
    # Your test code here
    pass
```

### Test Markers
```python
@pytest.mark.slow          # Marks test as slow
@pytest.mark.integration   # Marks test as integration test
@pytest.mark.unit          # Marks test as unit test
@pytest.mark.ui            # Marks test as UI test
@pytest.mark.game_logic    # Marks test as game logic test
```

## 🔍 Debugging Tests

### Verbose Output
```bash
python -m pytest tests/ -v -s
```

### Stop on First Failure
```bash
python -m pytest tests/ -x
```

### Show Local Variables on Failure
```bash
python -m pytest tests/ -l
```

### Run Specific Test
```bash
python -m pytest tests/test_snake.py::TestSnake::test_snake_creation
```

## 📈 Performance Testing

### Slow Test Detection
```bash
# Run only fast tests
python -m pytest tests/ -m "not slow"

# Run only slow tests
python -m pytest tests/ -m "slow"
```

### Test Timing
```bash
python -m pytest tests/ --durations=10
```

## 🚨 Common Issues and Solutions

### Import Errors
- **Problem**: Module not found
- **Solution**: Check `conftest.py` path configuration
- **Verify**: `sys.path` includes `src/` directory

### Mock Issues
- **Problem**: Mock not behaving as expected
- **Solution**: Check fixture setup in `conftest.py`
- **Verify**: Mock return values and method calls

### Coverage Issues
- **Problem**: Coverage not generating
- **Solution**: Install `pytest-cov`
- **Verify**: Check `--cov=src` parameter

### CI/CD Failures
- **Problem**: Tests pass locally but fail in CI
- **Solution**: Check Python version compatibility
- **Verify**: Run tests with same Python version locally

## 📚 Additional Resources

### pytest Documentation
- [pytest.org](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [pytest-mock](https://pytest-mock.readthedocs.io/)

### Testing Best Practices
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
- [Mocking in Python](https://docs.python.org/3/library/unittest.mock.html)
- [Coverage.py](https://coverage.readthedocs.io/)

### Project-Specific
- Check `tests/` directory for examples
- Review `conftest.py` for available fixtures
- See GitHub Actions workflow for CI configuration

## 🤝 Contributing to Tests

### Adding New Tests
1. Create test file following naming convention
2. Use appropriate test markers
3. Leverage existing fixtures when possible
4. Ensure good test coverage

### Updating Fixtures
1. Add new fixtures to `conftest.py`
2. Document fixture purpose and usage
3. Ensure fixtures are reusable across test modules

### Test Maintenance
- Keep tests up to date with code changes
- Remove obsolete tests
- Update fixtures as needed
- Maintain good test documentation

---

**Happy Testing! 🐍🧪**
