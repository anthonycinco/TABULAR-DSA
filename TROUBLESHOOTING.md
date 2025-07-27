# RF Learning System - Troubleshooting Guide

This guide provides solutions to common issues encountered when installing and running the RF Learning System.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Runtime Issues](#runtime-issues)
3. [Hardware Issues](#hardware-issues)
4. [Performance Issues](#performance-issues)
5. [Platform-Specific Issues](#platform-specific-issues)
6. [Getting Help](#getting-help)

## Installation Issues

### Python Version Problems

#### Issue: Python version too old
```
ERROR: Python 3.7+ is required. Current version: 3.6.x
```

**Solution:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.9 python3.9-pip python3.9-venv

# macOS
brew install python@3.9

# Windows
# Download from https://www.python.org/downloads/
```

#### Issue: Python not found in PATH
```
'python' is not recognized as an internal or external command
```

**Solution:**
```bash
# Check Python installation
python3 --version
python --version

# Add Python to PATH (Windows)
# Reinstall Python with "Add to PATH" option checked

# Ubuntu/Debian
sudo apt install python3-is-python3
```

### Package Installation Issues

#### Issue: pip installation fails
```
ERROR: Could not find a version that satisfies the requirement
```

**Solution:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install packages individually
pip install numpy
pip install matplotlib
pip install pandas
pip install scipy
pip install seaborn

# Check for conflicts
pip check
```

#### Issue: Permission denied during installation
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Use user installation
pip install --user -r requirements.txt

# Or use virtual environment
python -m venv rf_learning_env
source rf_learning_env/bin/activate  # Linux/macOS
rf_learning_env\Scripts\activate     # Windows
pip install -r requirements.txt
```

### GNU Radio Issues

#### Issue: GNU Radio not found
```
gnuradio-companion: command not found
```

**Solution:**
```bash
# Ubuntu/Debian
sudo add-apt-repository ppa:gnuradio/gnuradio-releases
sudo apt update
sudo apt install gnuradio gnuradio-dev

# macOS
brew install gnuradio

# Verify installation
gnuradio-companion --version
```

#### Issue: GNU Radio fails to start
```
ImportError: No module named 'gnuradio'
```

**Solution:**
```bash
# Reinstall GNU Radio
sudo apt remove gnuradio
sudo apt install gnuradio

# Check Qt dependencies
sudo apt install qt5-default python3-pyqt5
```

### NS3 Issues

#### Issue: NS3 not found
```
ns3: command not found
```

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install ns3-dev

# macOS
brew install ns3

# Manual installation
cd /tmp
wget https://www.nsnam.org/releases/ns-allinone-3.37.tar.bz2
tar xjf ns-allinone-3.37.tar.bz2
cd ns-allinone-3.37
./build.py --enable-examples --enable-tests
```

#### Issue: NS3 compilation fails
```
make: *** [all] Error 2
```

**Solution:**
```bash
# Install dependencies
sudo apt install build-essential libsqlite3-dev libboost-all-dev libssl-dev
sudo apt install libxml2-dev libgtk-3-dev libgsl-dev

# Clean and rebuild
cd /tmp/ns-allinone-3.37
./build.py --clean
./build.py --enable-examples --enable-tests
```

## Runtime Issues

### Import Errors

#### Issue: Module not found
```
ModuleNotFoundError: No module named 'numpy'
```

**Solution:**
```bash
# Install missing module
pip install numpy

# Check all requirements
pip install -r requirements.txt

# Verify installation
python -c "import numpy; print(numpy.__version__)"
```

#### Issue: Version conflicts
```
ImportError: numpy.core.multiarray failed to import
```

**Solution:**
```bash
# Reinstall numpy
pip uninstall numpy
pip install numpy

# Or upgrade all packages
pip install --upgrade numpy matplotlib pandas scipy seaborn
```

### Test Failures

#### Issue: System tests fail
```
Test failed: [specific error message]
```

**Solution:**
```bash
# Run individual tests
python test_system.py
python test_ns3_integration.py

# Check Python version
python --version

# Verify all dependencies
pip list | grep -E "(numpy|matplotlib|pandas|scipy|seaborn)"
```

#### Issue: NS3 integration tests fail
```
NS3 compilation failed: [error message]
```

**Solution:**
```bash
# NS3 is optional - system works without it
# Check if NS3 is properly installed
ns3 --version

# If NS3 is not needed, the system will use fallback simulation
```

### Memory Issues

#### Issue: Out of memory
```
MemoryError: Unable to allocate array
```

**Solution:**
```bash
# Reduce simulation size
python main_system.py --simulate --episodes 50  # Instead of 1000

# Close other applications
# Increase system RAM if possible
```

## Hardware Issues

### USRP Detection Problems

#### Issue: USRP not detected
```
No USRP devices found
```

**Solution:**
```bash
# Check USB connection
lsusb | grep Ettus

# Check UHD installation
uhd_usrp_probe

# Try with sudo
sudo uhd_usrp_probe

# Add user to usb group
sudo usermod -a -G usb $USER
sudo reboot
```

#### Issue: USRP permission denied
```
RuntimeError: USRP: No devices found
```

**Solution:**
```bash
# Check USB permissions
ls -la /dev/bus/usb/

# Add udev rules
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="2500", MODE="0666"' | sudo tee /etc/udev/rules.d/99-usrp.rules

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

#### Issue: USRP network connection fails
```
RuntimeError: USRP: No devices found
```

**Solution:**
```bash
# Check network configuration
ifconfig eth0 192.168.10.1 netmask 255.255.255.0

# Test connectivity
ping 192.168.10.2

# Check USRP IP address
uhd_usrp_probe --args="addr=192.168.10.2"
```

### Antenna Issues

#### Issue: No signal detected
```
Power levels consistently low
```

**Solution:**
```bash
# Check antenna connection
# Ensure antenna is suitable for 2.4 GHz
# Adjust USRP gain in config.py
USRP_GAIN = 30  # Increase gain
```

## Performance Issues

### Slow Learning

#### Issue: Q-agent not learning
```
Q-agent performance same as random agent
```

**Solution:**
```python
# Adjust learning parameters in config.py
LEARNING_RATE = 0.2      # Increase from 0.1
EPSILON_DECAY = 0.99     # Decrease from 0.995
MIN_EPSILON = 0.05       # Increase from 0.01
```

#### Issue: High collision rate
```
Collision rate not decreasing
```

**Solution:**
```python
# Adjust power threshold in config.py
POWER_THRESHOLD = -50    # Increase threshold for noisy environments
POWER_THRESHOLD = -70    # Decrease threshold for quiet environments
```

### Visualization Issues

#### Issue: Plots not updating
```
Matplotlib plots frozen
```

**Solution:**
```bash
# Use non-interactive backend
export MPLBACKEND=Agg

# Or set in Python
import matplotlib
matplotlib.use('Agg')
```

#### Issue: Plot window not appearing
```
No plot window shown
```

**Solution:**
```bash
# Install display dependencies
sudo apt install python3-tk

# Or use headless mode
python main_system.py --simulate --episodes 50 --no-display
```

## Platform-Specific Issues

### Windows Issues

#### Issue: WSL2 not working
```
WSL2 installation failed
```

**Solution:**
```powershell
# Enable WSL feature
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Enable Virtual Machine feature
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart computer
# Install WSL2
wsl --install -d Ubuntu
```

#### Issue: Python path problems
```
'python' is not recognized
```

**Solution:**
```cmd
# Check Python installation
python --version
py --version

# Reinstall Python with "Add to PATH" option
# Or add manually to PATH environment variable
```

### macOS Issues

#### Issue: Homebrew not found
```
brew: command not found
```

**Solution:**
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add to PATH
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

#### Issue: Permission denied
```
Permission denied: /usr/local/bin
```

**Solution:**
```bash
# Fix permissions
sudo chown -R $(whoami) /usr/local/bin
sudo chown -R $(whoami) /usr/local/lib

# Or use Homebrew
brew install python3
```

### Linux Issues

#### Issue: Package repository errors
```
E: Unable to locate package
```

**Solution:**
```bash
# Update package lists
sudo apt update

# Add missing repositories
sudo add-apt-repository ppa:gnuradio/gnuradio-releases

# Update again
sudo apt update
```

#### Issue: Qt dependencies missing
```
ImportError: No module named 'PyQt5'
```

**Solution:**
```bash
# Install Qt dependencies
sudo apt install qt5-default python3-pyqt5

# Or use PySide2
pip install PySide2
```

## Getting Help

### Before Asking for Help

1. **Check the logs**: Look at `system_log.txt` for detailed error messages
2. **Run tests**: Execute `python test_system.py` to verify installation
3. **Check versions**: Verify Python, GNU Radio, and other dependencies
4. **Search documentation**: Check README.md, INSTALLATION_GUIDE.md, and this file

### Information to Provide

When reporting issues, include:

1. **Operating System**: Ubuntu 20.04, Windows 10, macOS 12, etc.
2. **Python Version**: `python --version`
3. **Error Message**: Complete error traceback
4. **Steps to Reproduce**: Exact commands run
5. **System Information**: RAM, CPU, available disk space
6. **Hardware**: USRP model (if applicable)

### Common Solutions Summary

| Issue | Quick Fix |
|-------|-----------|
| Python not found | Install Python 3.7+ and add to PATH |
| Package installation fails | Upgrade pip and install individually |
| GNU Radio not working | Install via PPA (Ubuntu) or Homebrew (macOS) |
| USRP not detected | Check USB connection and permissions |
| Tests failing | Verify all dependencies are installed |
| Performance poor | Adjust learning parameters in config.py |

### Additional Resources

- **Documentation**: README.md, INSTALLATION_GUIDE.md, SYSTEM_SUMMARY.md
- **Configuration**: Edit config.py for environment-specific settings
- **Examples**: Run simulation mode for testing without hardware
- **Logs**: Check system_log.txt for detailed error information

The system is designed to be robust and provide fallback options when hardware or software is not available. Most issues can be resolved by following the troubleshooting steps above. 