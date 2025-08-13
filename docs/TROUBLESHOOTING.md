# 🐛 Troubleshooting Guide

This guide helps you resolve common issues when setting up and running the Snake Game.

## 📋 Quick Diagnosis

### Check These First
1. **Python Version**: `python --version` (should be 3.8+)
2. **Pygame Installation**: `python -c "import pygame"`
3. **Virtual Environment**: Make sure it's activated
4. **Dependencies**: `pip list | grep pygame`

## 🚨 Common Issues & Solutions

### Installation Issues

#### ❌ Python Not Found
**Error**: `'python' is not recognized as an internal or external command`

**Solutions**:
```bash
# Windows - Try these commands:
py --version
python3 --version

# macOS/Linux:
python3 --version

# If Python is not installed:
# Windows: Download from python.org
# macOS: brew install python@3.9
# Linux: sudo apt install python3.9
```

#### ❌ pip Not Found
**Error**: `'pip' is not recognized as an internal or external command`

**Solutions**:
```bash
# Windows:
py -m pip --version
python -m pip --version

# macOS/Linux:
python3 -m pip --version

# Install pip if missing:
python -m ensurepip --upgrade
```

#### ❌ Pygame Installation Fails
**Error**: `ERROR: Could not build wheels for pygame`

**Solutions**:
```bash
# Update pip first
python -m pip install --upgrade pip

# Try pre-built wheels
pip install pygame --pre

# Windows - Install Visual C++ Redistributable
# Download from Microsoft's website

# Linux - Install system dependencies
sudo apt-get install python3-dev python3-pip
sudo apt-get install libgl1-mesa-dev libasound2-dev

# macOS - Install Xcode tools
xcode-select --install
```

#### ❌ Virtual Environment Issues
**Error**: Virtual environment not activating or not found

**Solutions**:
```bash
# Windows - Try these activation methods:
venv\Scripts\activate
venv\Scripts\activate.bat
.\venv\Scripts\Activate.ps1

# macOS/Linux:
source venv/bin/activate

# Check if activated:
which python  # Should point to venv directory
echo $VIRTUAL_ENV  # Should show venv path

# Recreate if corrupted:
rm -rf venv
python -m venv venv
```

### Runtime Issues

#### ❌ Game Won't Start
**Error**: Game crashes on startup or shows error messages

**Solutions**:
1. **Check Python and Pygame**:
   ```bash
   python --version
   python -c "import pygame; print(pygame.version.ver)"
   ```

2. **Verify Dependencies**:
   ```bash
   pip list | grep -E "(pygame|pytest)"
   ```

3. **Run with Debug Mode**:
   ```bash
   SNAKE_GAME_DEBUG=true python src/main.py
   ```

4. **Check System Requirements**:
   - Graphics drivers up to date
   - Sufficient RAM (4GB+)
   - Python 3.8+ installed

#### ❌ Performance Issues
**Problem**: Low frame rate, lag, or slow gameplay

**Solutions**:
1. **Close Other Applications**:
   - Browser tabs
   - Resource-intensive programs
   - Background processes

2. **Check System Settings**:
   - Power plan (set to High Performance)
   - Graphics settings (set to Performance)
   - Disable unnecessary startup programs

3. **Game Settings**:
   - Reduce graphics quality
   - Lower frame rate limit
   - Disable particle effects

4. **Update Drivers**:
   - Graphics drivers
   - Audio drivers
   - System updates

#### ❌ Audio Issues
**Problem**: No sound, distorted audio, or audio crashes

**Solutions**:
1. **Check System Audio**:
   - Volume settings
   - Audio output device
   - Audio drivers

2. **Game Audio Settings**:
   - Check in-game volume settings
   - Try different audio devices
   - Restart the game

3. **Platform-Specific**:
   - **Windows**: Check Windows Audio service
   - **macOS**: Check Audio MIDI Setup
   - **Linux**: Check ALSA/PulseAudio

#### ❌ Control Issues
**Problem**: Controls not responding or behaving unexpectedly

**Solutions**:
1. **Check Game Focus**:
   - Click on game window
   - Ensure game is in foreground
   - Check if another app captures input

2. **Control Schemes**:
   - Try different control methods
   - Check key bindings in settings
   - Restart the game

3. **Input Device Issues**:
   - Test keyboard in other applications
   - Check for stuck keys
   - Try different input devices

### Platform-Specific Issues

#### Windows Issues

##### Missing Visual C++ Redistributable
**Error**: `The program can't start because MSVCP140.dll is missing`

**Solution**:
1. Download Visual C++ Redistributable 2015-2022 from Microsoft
2. Install both x86 and x64 versions
3. Restart computer

##### Graphics Driver Issues
**Problem**: Game crashes or shows graphics errors

**Solutions**:
1. Update graphics drivers from manufacturer website
2. Check Windows Update for driver updates
3. Rollback to previous driver if issues persist

##### Permission Issues
**Error**: Access denied or permission errors

**Solutions**:
1. Run as Administrator
2. Check folder permissions
3. Disable antivirus temporarily

#### macOS Issues

##### Missing Xcode Tools
**Error**: `clang: error: no input files`

**Solution**:
```bash
xcode-select --install
```

##### Security Issues
**Problem**: Python blocked by security settings

**Solution**:
1. Go to System Preferences > Security & Privacy
2. Allow Python in "Allow apps downloaded from"
3. Restart Python/terminal

##### Graphics Issues
**Problem**: Game won't start or graphics errors

**Solutions**:
1. Update macOS to latest version
2. Check graphics compatibility
3. Try different display settings

#### Linux Issues

##### Missing Libraries
**Error**: `ImportError: No module named 'pygame'`

**Solutions**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev python3-pip
sudo apt-get install libgl1-mesa-dev libasound2-dev
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

# Fedora/RHEL
sudo dnf install python3-devel python3-pip
sudo dnf install mesa-libGL-devel alsa-lib-devel
sudo dnf install SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel

# Arch Linux
sudo pacman -S python-pip
sudo pacman -S mesa lib32-mesa
sudo pacman -S sdl2 sdl2_image sdl2_mixer sdl2_ttf
```

##### Display Issues
**Problem**: Game won't start or display errors

**Solutions**:
1. Check X11/Wayland configuration
2. Install display drivers
3. Check DISPLAY environment variable

##### Audio Issues
**Problem**: No sound or audio errors

**Solutions**:
```bash
# Install audio libraries
sudo apt-get install libasound2-dev
sudo apt-get install pulseaudio pulseaudio-utils

# Check audio service
pulseaudio --start
```

### Dependency Issues

#### ❌ Version Conflicts
**Error**: `VersionConflict: package conflicts`

**Solutions**:
```bash
# Check installed versions
pip list

# Upgrade conflicting packages
pip install --upgrade package_name

# Use virtual environment to avoid conflicts
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### ❌ Missing Dependencies
**Error**: `ModuleNotFoundError: No module named 'module_name'`

**Solutions**:
```bash
# Install missing module
pip install module_name

# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall

# Check requirements file
cat requirements.txt
```

### Testing Issues

#### ❌ Tests Fail
**Error**: `pytest: command not found` or test failures

**Solutions**:
```bash
# Install pytest
pip install pytest

# Run tests with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_game_logic.py -v

# Check test dependencies
pip install pytest-cov pytest-mock
```

#### ❌ Coverage Issues
**Error**: Coverage report not generated

**Solutions**:
```bash
# Install coverage
pip install coverage

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Check coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

## 🔍 Debug Mode

Enable debug mode to get more information:

```bash
# Set debug environment variable
export SNAKE_GAME_DEBUG=true

# Run game with debug
python src/main.py

# Check debug output in console
```

## 📊 System Information

Collect this information when reporting issues:

```bash
# Python version
python --version

# Pygame version
python -c "import pygame; print(pygame.version.ver)"

# System info
# Windows: systeminfo
# macOS: system_profiler SPHardwareDataType
# Linux: uname -a && lscpu

# Installed packages
pip list

# Error logs
# Check console output for error messages
```

## 🆘 Getting Help

### Before Asking for Help
1. ✅ Check this troubleshooting guide
2. ✅ Search existing issues
3. ✅ Try the solutions above
4. ✅ Collect system information

### When Reporting Issues
Include:
- **Error Message**: Exact error text
- **System Info**: OS, Python version, hardware
- **Steps to Reproduce**: What you did before the error
- **Expected vs Actual**: What should happen vs what happened
- **Screenshots/Logs**: Visual evidence of the issue

### Where to Get Help
1. **GitHub Issues**: [Create a new issue](https://github.com/your-repo/snake-game/issues)
2. **Community**: Join our Discord/forum
3. **Documentation**: Check other guides in the docs folder
4. **Search**: Look for similar issues online

## 🎯 Prevention Tips

### Best Practices
1. **Use Virtual Environments**: Always create a new venv for projects
2. **Update Regularly**: Keep Python, pip, and dependencies updated
3. **Check Requirements**: Verify system requirements before installation
4. **Backup Configs**: Save your configuration files
5. **Test Incrementally**: Test after each major change

### Regular Maintenance
```bash
# Update pip monthly
python -m pip install --upgrade pip

# Update dependencies quarterly
pip install -r requirements.txt --upgrade

# Clean up old packages
pip list --outdated
pip uninstall package_name  # Remove unused packages
```

---

**Still having issues?** Don't worry! We're here to help. Create an issue with the information above and we'll get you sorted out. 🚀
